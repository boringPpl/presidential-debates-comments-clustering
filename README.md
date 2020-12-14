# Presidential Debate Youtube Comments Clustering 

### Introductions
At the point when we started this project, election week is coming up. There was so much excitement in the air on who is the next US president to be elected. There were thousands of articles on who's leading the polls. The US election has been trending on most, if not all, social media platforms. Being Data scientists, we wonder if it would be possible to leverage on these different data sources to understand various topics of discussion surrounding each candidate. Of which, we have decided to focus on Youtube comments as a starting point for this project. We were aware of the possibility of biased sampling as the demographic report of users on Youtube reports the highest level of usage from people in the 18-34 age range <sup>[1](https://www.businessofapps.com/data/youtube-statistics/)</sup>. And these users in between these ages are correlated to being more technogically savvy. With that being said, there is still a significant number of people using Youtube from other age groups, and with Youtube being the number one site for web traffic worldwide (8.6 billion monthly visits)<sup>[2](https://www.businessofapps.com/data/youtube-statistics/)</sup>, it's a good representation of the global population and it would be significant to conduct an analysis on the different core ideas, specifically on the US election. 

This exploration has many use-cases. Essentially it is often difficult to get an overview of all the core ideas amongst the hundreds of thousands of Youtube comments. Youtubers and content creators would not be able to sift through every comment received on their videos. Having an overview or a summary of the different perspectives of their viewers would be useful for them to either create another response video to address their concerns or to reply to each of these "clusters" of ideas. This analysis can also be extended to customer service chats or surveys from large number of users. 




![](https://i.imgur.com/SJcCygI.png)
First 2020 Presidential Debate between Donald Trump and Joe Biden
https://www.youtube.com/watch?v=wW1lY5jFNcQ&t=3s


![](https://i.imgur.com/xT7G3PW.png)
Second presidential debate
https://www.youtube.com/watch?v=bPiofmZGb8o




For the purpose of this article, we would be focusing on creating a summary of the Youtube comments  found in the Presidential Debate between Donald Trump and Joe Biden as shown in the screenshots above.

### Overall Architecture Plan
- break down the task needed 
- the major pieces.
    - youtube api 
    - CPU/ GPU /Ram
    - Libraries needed for the task 
- flows



### Pulling comments from Youtube 
#### Enabling the Youtube API

1. Go to the GCP (Google Cloud Platform) [APIs & Services Dashboard](https://console.cloud.google.com/apis/dashboard)
2. Click the "+ENABLE APIS AND SERVICES" and search for "Youtube". Click on "YouTube Data API v3"
3. Enable the API

#### Obtaining a Youtube API key

1. Go to [https://console.cloud.google.com/apis/credentials](https://console.cloud.google.com/apis/credentials)
2. Click "+CREATE CREDENTIALS" and choose "API KEY". Click "RESTRICT KEY"
3. In the "API Restrictions" section, choose the "Restrict Key" option. Click in the "Select APIs" dropdown box, and choose "Youtube Data API v3". Click Save.

![](https://i.imgur.com/kwJjJuQ.png)

Store the Youtube API key in a file, such as `youtube_api_key.txt`

#### Downloading the comments

In order to extract the comments from the Youtube page, the code `get_comments_of_video_id.py` from the Github repo [github.com/XWilliamY/custom_yt_comments_dataset](https://github.com/XWilliamY/custom_yt_comments_dataset) may be used as follows:

```bash=
python get_comments_of_video_id.py --video_url https://www.youtube.com/watch?v=wW1lY5jFNcQ --apikey youtube_api_key.txt
```

The Youtube comments will be stored in a `.csv` file, `{video_id}_csv.csv` which can be read in Python using `df = pd.read_csv('{video_id}_final.csv', header=None)`

### Exploratory Data Analysis and Data cleaning
Let us start by looking through some of the comments that users are making. Looking through the comments are useful to understand the structure of data we need to deal with; any noise or cleaning required, a sense of the average length of the sentense or amount of data which might give us a sensing of the hardware needed for processing the data. 

> As a non American, this is highly entertaining 

> “i take full responsibility”<br> 
> 3 seconds later<br>
> “its china’s fault”

> Biden when trump is talking: 😄<br>
> Trump when Biden is talking: 😙

> I deleted my Netflix account.<br>
> This is much more entertaining

> ' i am the least racist person in this room ' <br>
> biden trying not to laugh

> If I wanted to watch 2 elderly people argue I’d just hang out with my parents.

> this should be under comedy in NETFLIX

> Obama 2009: Yes we can<br>
> Trump 2016:America first<br>
> Biden2020: Will u shut up man

> i cant tell if biden is laughing or crying

> Trump: who built the cages joe?<br>
> Biden: ignores. 



ermain Cain and Trump does not believe in covid.


### Clustering of intents

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

### Results and Conclusion

Next step Plans: 
Have different levels of abstraction: Ex:
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

                    - H