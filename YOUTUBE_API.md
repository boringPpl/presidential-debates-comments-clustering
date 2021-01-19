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

<img src="https://i.imgur.com/kwJjJuQ.png" height="700"></img>

Export your Youtube API key (in your shell environment or place it in your startup script, e.g. in `~/.bash_profile` or `~/.bashrc`) as follows:

```bash
export YOUTUBE_API_KEY="...your_Youtube_API_key_here..."
```

#### Downloading the comments

In order to extract the comments from the Youtube page, the code `get_comments_of_video_id.py` from the Github repo [github.com/XWilliamY/custom_yt_comments_dataset](https://github.com/XWilliamY/custom_yt_comments_dataset) was adapted slightly and stored in this Git repository [here](https://github.com/boringPpl/presidential_debates_comments_clustering/blob/main/src/get_comments_of_video_id.py).

To use the Python script, the dependencies must first be installed:

```bash=
pip install -r requirements.txt
```


Next, run the Python script as follows to get the comments from the first presidential debate (storing the data in `wW1lY5jFNcQ_csv_final.csv`):

```bash
python get_comments_of_video_id.py --video_url https://www.youtube.com/watch?v=wW1lY5jFNcQ
```

To get the comments for the second presidential debate:

```bash
python get_comments_of_video_id.py --video_url https://www.youtube.com/watch?v=bPiofmZGb8o
```

The data is stored in`bPiofmZGb8o_csv_final.csv`
(the Youtube comments files take the format `{video_id}_csv.csv`). This file may be read using the Python/Pandas library using `df = pd.read_csv('{video_id}_final.csv', header=None)`
