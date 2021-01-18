# Youtube Comments Extraction

## Introduction

There are multiple ways to obtain the text of comments from Youtube videos. One of the easiest ways is by downloading one of the [Kaggle datasets](https://www.kaggle.com/datasnaek/youtube?select=UScomments.csv) containing those comments (note: there is [an updated version](https://www.kaggle.com/datasnaek/youtube-new?select=USvideos.csv)). However, with this method, the comments from a specific Youtube video may not necessarily be available (especially if the video is very recent). Another option is to scrape the data directly from the website, but this could become problematic if Youtube's website layout changes. A third way, which we use here, is to use the Youtube API to extract the comments.

The process to extract the comments requires a few steps, and is described as follows:

### Pulling data from Youtube API

In order to extract the Youtube comments, the [Youtube API](https://developers.google.com/youtube/v3/getting-started) was chosen over scraping the data directly from the website. The advantage of this approach is that it will continue to work, even if the website layout changes. Note however, that the API has a limitation of about 10k requests per day.

#### Enabling the Youtube API

In order to use the Youtube API, it must first be enabled as follows:

1. Go to the GCP (Google Cloud Platform) [APIs & Services Dashboard](https://console.cloud.google.com/apis/dashboard)
2. Click the "+ENABLE APIS AND SERVICES" and search for "Youtube". Click on "YouTube Data API v3"
3. Enable the API

#### Generating a Youtube API key

To use the Youtube API, a key must be generated, and saved. The steps to do this are as follows:

1. Go to [https://console.cloud.google.com/apis/credentials](https://console.cloud.google.com/apis/credentials)
2. Click "+CREATE CREDENTIALS" and choose "API KEY". Click "RESTRICT KEY"
3. In the "API Restrictions" section, choose the "Restrict Key" option. Click in the "Select APIs" dropdown box, and choose "Youtube Data API v3". Click Save.

![](https://i.imgur.com/kwJjJuQ.png)

Store the Youtube API key in a file, such as `youtube_api_key.txt`

#### Downloading the comments

In order to extract the comments from the Youtube page, the code `get_comments_of_video_id.py` from the Github repo [github.com/XWilliamY/custom_yt_comments_dataset](https://github.com/XWilliamY/custom_yt_comments_dataset) may be used as follows:

First install the dependencies:

```bash=
pip install google-api-python-client
```

Next, run the Python script as follows:

```bash=
python get_comments_of_video_id.py --video_url https://www.youtube.com/watch?v=wW1lY5jFNcQ --apikey youtube_api_key.txt
```

The Youtube comments will be stored in a `.csv` file, `{video_id}_csv.csv` which can be read in Python using `df = pd.read_csv('{video_id}_final.csv', header=None)`


