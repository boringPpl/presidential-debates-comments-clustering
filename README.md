# Presidential Debate Youtube Comments Clustering 


At the point when we started this project, election week is coming up. There is so much excitement in the air on who is the going to be the next US president. There are thousands of articles on who is leading the polls. Being Data scientist, we wonder if it will be possible to leverage on other data sources like Youtube comments or twitter comments to understand what core ideas are more favourable for each candidate. We are aware of that there may be biased sampling since it is only limited to users of Youtube and twitter and that might be correlated to more technogically savvy users. Still it can be significant enough study to understand core issues that global citizens raise. 

This exploration is useful for many other problems. Essentially it is often difficult to get an overview of all the core ideas amounst hundreds of thousands of comments. This work can extend to other customer service chats or overview of open ended answers from large number of users. 




![](https://i.imgur.com/SJcCygI.png)
First 2020 Presidential Debate between Donald Trump and Joe Biden
https://www.youtube.com/watch?v=wW1lY5jFNcQ&t=3s


![](https://i.imgur.com/xT7G3PW.png)
Second presidential debate
https://www.youtube.com/watch?v=bPiofmZGb8o



Creating an summary of the different types of comments. For example, Youtubers who get thousands of comments a day would not be able to sift through all of the comments received on their videos. 
* These overviews are useful for them to either create another response video to address the concerns or as a next step, where they can reply to each of these "clusters" of ideas. 
* Understanding the sentiments of the commenters

For the purpose of this article, we would be focusing on creating a summary of the Youtube comments  found in the Presidential Debate between Donald Trump and Joe Biden.

### Overview of core ideas in the comments.
Exploratory overview of the comments


2 weeks ago<br>
As a non American, this is highly entertaining

2 weeks ago<br>
“i take full responsibility”<br> 
3 seconds later<br>
“its china’s fault”

6 days ago<br>
Biden when trump is talking: 😄<br>
Trump when Biden is talking: 😙

2 weeks ago<br>
I deleted my Netflix account.<br>
This is much more entertaining

1 week ago (edited)<br>
' i am the least racist person in this room '

biden trying not to laugh

1 month ago<br>
If I wanted to watch 2 elderly people argue I’d just hang out with my parents.

2 weeks ago<br>
this should be under comedy in NETFLIX

4 days ago<br>
Obama 2009: Yes we can<br>
Trump 2016:America first<br>
Biden2020: Will u shut up man

2 weeks ago<br>
i cant tell if biden is laughing or crying

9 hours ago<br>
Trump: who built the cages joe?

Biden: ignores. 



#### Enabling the Youtube API

1. Go to the GCP (Google Cloud Platform) [APIs & Services Dashboard](https://console.cloud.google.com/apis/dashboard)
2. Click the "+ENABLE APIS AND SERVICES" and search for "Youtube". Click on "YouTube Data API v3"
3. Enable the API

#### Obtaining a Youtube API key

1. Go to [https://console.cloud.google.com/apis/credentials](https://console.cloud.google.com/apis/credentials)
2. Click "+CREATE CREDENTIALS" and choose "API KEY". Click "RESTRICT KEY"
3. In the "API Restrictions" section, choose the "Restrict Key" option. Click in the "Select APIs" dropdown box, and choose "Youtube Data API v3". Click Save.
4. Copy the key that you just created and add the following line to `~/.bash_profile` or `~/.bashrc`

```bash=
export YOUTUBE_API_KEY="AIzaSyC_...p037g"
```

#### Downloading the comments

In order to extract the comments from the Youtube page, the code `get_comments_of_video_id.py` from the Github repo [github.com/XWilliamY/custom_yt_comments_dataset](https://github.com/XWilliamY/custom_yt_comments_dataset) is used as follows:

```bash=
python get_comments_of_video_id.py --video_id https://www.youtube.com/watch?v=wW1lY5jFNcQ
```

- Have different levels of abstraction: Ex:
    - Title: Coronavirus Ramps Up in the U.S. and Claims Herman Cain | The Daily Social Distancing Show
    - Comments:
         - Herman Cain survive cancer. Herman Cain didn't survive Trump stupidity. Covid-19: "I attack everyone, especially African Americans, elderly people, and people who don't wear a mask or social distance in public spaces."
                    Herman Cain (74 year old African American, with no mask on, in a Trump rally): "Masks will not be mandatory.... People are fed up."

        - **[José Gomes](https://www.youtube.com/channel/UCOzhu7x9YPjoijyzO0WV8wA)** [1 day ago](https://www.youtube.com/watch?v=yIwuzldM7HQ&lc=UgxIPbruQ-UeJx-bUCB4AaABAg)

                    Herman Cain: Coronavirus doesn’t exist
                    Coronavirus: Herman Cain doesn’t exist

                    Hermain Cain to himself after he tested positive:
                    “awwww shucky ducky...”

                    Herman Cain: There is no pandemic.
                    Pandemic: There is no Herman Cain.

                    ![https://s3-us-west-2.amazonaws.com/secure.notion-static.com/926655e0-4f75-4db4-9847-bd9e7d86b6e6/Screenshot_2020-08-02_at_9.12.37_PM.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/926655e0-4f75-4db4-9847-bd9e7d86b6e6/Screenshot_2020-08-02_at_9.12.37_PM.png)

                    ### Abstracted overview:

                    Level 1: 

                    - Hermain Cain is a african american who does not believe in covid and died from it
                    - Hermain Cain has cancer
                    - Donald Trump does not believe in covid

                    Level 2: 

                    - Hermain Cain and Trump does not believe in covid.



## Proposed solution:
## + explanation of model?
## Clustering

Text - Processing

- Remove emoji - [https://www.kaggle.com/chameleontk/v2-fine-tuning-bert-with-pre-processed-text](https://www.kaggle.com/chameleontk/v2-fine-tuning-bert-with-pre-processed-text)
- Pick a embedding:
    - Bert
    - Variants of Bert: XLA Roberta
    - Fasttext
    - TF hub: universal sentence encoder
        - [https://tfhub.dev/google/universal-sentence-encoder/4](https://tfhub.dev/google/universal-sentence-encoder/4)
- Dimension reduction
    - PCA
    - UMAP
    - T-sne

## Results

## Conclusion