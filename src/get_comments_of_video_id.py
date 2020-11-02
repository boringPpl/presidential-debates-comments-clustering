#!/usr/bin/env python

# This code is adapted from the following Source:
# https://github.com/XWilliamY/custom_yt_comments_dataset

import argparse
import json
import pandas as pd
import os

from apiclient.discovery import build
from csv import writer
from urllib.parse import urlparse, parse_qs


DEVELOPER_KEY = os.getenv('YOUTUBE_API_KEY')


def get_keys(filename):
    global DEVELOPER_KEY
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    return {'key': DEVELOPER_KEY, 'name': 'youtube', 'version': 'v3'}

def build_service():
    global DEVELOPER_KEY

    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    return build(YOUTUBE_API_SERVICE_NAME,
                 YOUTUBE_API_VERSION,
                 developerKey=DEVELOPER_KEY)

# https://stackoverflow.com/questions/45579306/get-youtube-video-url-or-youtube-video-id-from-a-string-using-regex
def get_id(url):
    u_pars = urlparse(url)
    quer_v = parse_qs(u_pars.query).get('v')
    if quer_v:
        return quer_v[0]
    pth = u_pars.path.split('/')
    if pth:
        return pth[-1]

def get_comments(**kwargs):
    """
    ty: 
    https://python.gotrained.com/youtube-api-extracting-comments/#Cache_Credentials
    https://www.pingshiuanchua.com/blog/post/using-youtube-api-to-analyse-youtube-comments-on-python
    """

    # edit these list declarations as needed
    comments, commentsId, repliesCount, likesCount, updatedAt, viewerRating = [], [], [], [], [], []

    # clean kwargs

    # parameters needed for query
    kwargs['part'] = kwargs.get('part', 'snippet').split()
    kwargs['maxResults'] = kwargs.get('maxResults', 100)
    kwargs['textFormat'] = kwargs.get('textFormat', 'plainText')
    kwargs['order'] = kwargs.get('order', 'time')
    service = kwargs.pop('service')

    # other parameters for dealing with files
    write_lbl = kwargs.pop('write_lbl', True)
    csv_filename = kwargs.pop('csv_filename')
    token_filename = kwargs.pop('token_filename')


    # get the first page of comments
    response = service.commentThreads().list(
        **kwargs
    ).execute()

    # continue until we crash or reach the end
    page = 0
    while response:
        print(f'page {page}')
        page += 1
        index = 0
        for item in response['items']:
            print(f"comment {index}")
            index += 1

            # query different pieces of data from the JSON response
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comment_id = item['snippet']['topLevelComment']['id']
            reply_count = item['snippet']['totalReplyCount']
            like_count = item['snippet']['topLevelComment']['snippet']['likeCount']
            updated_at = item['snippet']['topLevelComment']['snippet']['updatedAt']
            viewer_rating = item['snippet']['topLevelComment']['snippet']['viewerRating']

            # append to corresponding list
            comments.append(comment)
            commentsId.append(comment_id)
            repliesCount.append(reply_count)
            likesCount.append(like_count)
            updatedAt.append(updated_at)
            viewerRating.append(viewer_rating)

            if write_lbl:
                with open(f'{csv_filename}.csv', 'a+') as f:
                    # https://thispointer.com/python-how-to-append-a-new-row-to-an-existing-csv-file/#:~:text=Open%20our%20csv%20file%20in,in%20the%20associated%20csv%20file
                    csv_writer = writer(f)
                    csv_writer.writerow([comment, comment_id, reply_count, like_count, viewer_rating, updated_at])

        # check if there's a next page
        if 'nextPageToken' in response:
            with open(f'{token_filename}.txt', 'a+') as f:
                f.write(kwargs.get('pageToken', ''))
                f.write('\n')
            kwargs['pageToken'] = response['nextPageToken']
            response = service.commentThreads().list(
                **kwargs
            ).execute()
        else:
            break

    return {
        'Comments': comments,
        'Comment ID' : commentsId,
        'Reply Count' : repliesCount,
        'Like Count' : likesCount,
        'Updated At' : updatedAt,
        'Viewer Rating': viewerRating
    }

def save_to_csv(output_dict, video_id, output_filename):
    output_df = pd.DataFrame(output_dict, columns = output_dict.keys())
    output_df.to_csv(f'{output_filename}.csv')

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--part', help='Desired properties of commentThread', default='snippet')
    parser.add_argument('--maxResults', help='Max results per page', default=100)
    parser.add_argument('--write_lbl', help="Update csv after each comment?", default=True)
    parser.add_argument('--csv_filename', default=None)
    parser.add_argument('--token_filename', default=None)
    parser.add_argument('--video_url', default='https://www.youtube.com/watch?v=wW1lY5jFNcQ')
    parser.add_argument('--order', default='time')
    parser.add_argument('--pageToken', default=None)
    args = parser.parse_args()

    # build kwargs from args
    kwargs = vars(args)

    service = build_service()
    video_id = get_id(kwargs.pop('video_url'))

    if not args.csv_filename:
        args.csv_filename = video_id + "_csv"

    if not args.token_filename:
        args.token_filename = video_id + "_page_token"

    if not kwargs.get('pageToken'):
        kwargs.pop('pageToken')

    kwargs['videoId'] = video_id
    kwargs['service'] = service
    output_dict = get_comments(**kwargs)

    args.csv_filename += "_final"
    save_to_csv(output_dict, video_id, args.csv_filename)


if __name__ == '__main__':
    main()

