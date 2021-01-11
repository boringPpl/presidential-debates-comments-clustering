# [Presidential Debate Youtube Comments Clustering](https://boringppl.github.io/presidential_debates_comments_clustering/)

### Introduction
At the point when we started this project, election week is coming up. There was so much excitement in the air on who is the next US president to be elected. There were thousands of articles on who's leading the polls. The US election has been trending on most, if not all, social media platforms. Being Data scientists, we wonder if it would be possible to leverage on these different data sources to understand various topics of discussion surrounding each candidate. Of which, we have decided to focus on Youtube comments as a starting point for this project. 

We were aware of the possibility of biased sampling as the demographic report of users on Youtube indicates the highest level of usage from users in the 18-34 age range<sup>[1](https://www.businessofapps.com/data/youtube-statistics/)</sup>, which also correlated to the most technogically savvy group of people. With that being said, there is still a significant number of people using Youtube from other age groups, and with Youtube being the number one site for web traffic worldwide (8.6 billion monthly visits)<sup>[2](https://www.businessofapps.com/data/youtube-statistics/)</sup>. It would be significant to conduct an analysis on the different core ideas of the Youtube comments section, specifically on the US election.

While this exploration covers the US election, the essential parts of the analysis are relevant to many other use-cases. Youtube influencers and content creators can receive hundreds of thousands of comments per video and it is often difficult to get an overview of all the core ideas, and it would not be easy to sift through every comment received in each video. Having an overview or a summary of the different perspectives of the viewers would be useful for them to either create another response video to address their concerns or to reply to each of these "clusters" of ideas. This analysis can also be extended to customer service chats or surveys from large number of users. 

To be clear, this is by no means a predictor of the election results. 1. biased samples, 2. not everyone on youtube or watches this is from US, 3. presidential elections use the Electoral College, which is not a direct result to the total
<br>

We have hence picked two Youtube videos to focus on.

![](https://i.imgur.com/8L4hQmw.png)

First 2020 Presidential Debate between Donald Trump and Joe Biden uploaded on Youtube
https://www.youtube.com/watch?v=wW1lY5jFNcQ



Second presidential debate uploaded on Youtube
https://www.youtube.com/watch?v=bPiofmZGb8



For the purpose of this article, we would be focusing on creating a summary of the Youtube comments  found in the Presidential Debate between Donald Trump and Joe Biden as shown in the screenshots above.

### Overall Architecture Plan (TLDR of the whole flow) 


![](https://i.imgur.com/nhy4RtF.png)
​

Here are some of the major considerations when planning out the pieces:
1. Pulling data from Youtube API: We can either go with scrapping the site with beautifulSoup (barring some legal concerns) or we can pull directly off the Youtube API. In this case, we found that pulling off the API is the easier way to go about it since that will be more robust. 
2. Exploratory data analysis and data cleaning: We will expect the user generated comments can be rather messy. We will need to deal with emojis and repeated words. The first step to any ML project is always to print out the data to explore what we are dealing with. 
3. Encoding the sentences: Running text analysis requires us to change the text into a vector that the algorithms can work with. There are a few popular libraries to change sentences to embeddings. I will not go into details, but you can find plenty of articles explaining each of them in detail online. After a test evaluation, we found Universal Sentence encoder to be the most accurate in terms of representing central core ideas in terms of comments. 
    - Universal sentence encoder 
    - SentenceBert
    - Infersent

4. Exploration of different clustering methods
    - PCA 50 
    - UMap
    - T-SNE


We will now go into further explanation for each section.

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

```bash=
python get_comments_of_video_id.py --video_url https://www.youtube.com/watch?v=wW1lY5jFNcQ --apikey youtube_api_key.txt
```

The Youtube comments will be stored in a `.csv` file, `{video_id}_csv.csv` which can be read in Python using `df = pd.read_csv('{video_id}_final.csv', header=None)`

### Exploratory Data Analysis and Data cleaning
Let us start by looking through some of the comments that users are making. By looking through the comments, we are able to understand the structure of data we need to deal with, and the amount of cleaning required. We would also be able to gauge the average length of the sentences and amount of data to better give us a sense of the hardware needed for processing. 

Example of some comments extracted from the Youtube video:

> As a non American, this is highly entertaining 

> “i take full responsibility”<br> 
> 3 seconds later<br>
> “its china’s fault”

> Biden when trump is talking: 😄<br>
> Trump when Biden is talking: 😙

> I deleted my Netflix account.<br>
> This is much more entertaining

> "i am the least racist person in this room" <br>
> biden trying not to laugh

> If I wanted to watch 2 elderly people argue I’d just hang out with my parents.

> this should be under comedy in NETFLIX

> Obama 2009: Yes we can<br>
> Trump 2016:America first<br>
> Biden2020: Will u shut up man

> i cant tell if biden is laughing or crying

> Trump: who built the cages joe?<br>
> Biden: ignores. 

We can now proceed with cleaning the text and prepping it for the next stage. Looking at the comments above, we have to remove the emoji's and translate them into text-form. 

This is done by using the emoji library<sup>[3](https://pypi.org/project/emoji/)</sup> to convert convert emoticons into words.

For example, using a comment from above:

> Biden when trump is talking: 😄

becomes
> Biden when trump is talking: :grinning face with smiling eyes:<br>

when the demojize function from the emoji library is applied on the sentence.

There was also the issue of running into an "out of memory error" due to the length of the sentences. We found that it crashes at around 2300+ characters. Hence we truncated the comments to a maximum of about 2200 characters to overcome this problem.

The usual cleaning of text was then done, namely standardising the text to lowercase, and the removal of special characters.

### Embedding
After cleaning the data, we have to convert the text into word embeddings for the clustering model. We experimented with Bert<sup>[4](https://huggingface.co/sentence-transformers/bert-base-nli-mean-tokens)</sup> embeddings and Universal Sentence Encoder<sup>[5](https://tfhub.dev/google/universal-sentence-encoder/4)</sup>.

BERT, short for Bidirectional Encoder Representations from Transformers, uses a masked language model(MLM) that randomly masks some tokens of the input such that the aim is to predict accurately the masked word using the other unmasked tokens in the sentence. 

As for the Universal Sentence Encoder, the tokens are converted into vectors by computing the element-wise sum of the representations at each word position. This takes into account the ordering and identity of the other words in the sentence to produce the embedding. Embeddings produced are approximately normalized.

Usage of both embeddings can be found in the github notebook: comments_clustering.ipynb.
For the following sections, we used the embedding produced by the Unversal Sentence Encoder because of its efficiency, since we face a memory limitation.


### Clustering of intents

- Dimension reduction
    - [PCA](https://en.wikipedia.org/wiki/Principal_component_analysis)
    - [UMAP](https://en.wikipedia.org/wiki/Nonlinear_dimensionality_reduction#Uniform_manifold_approximation_and_projection)
    - [T-SNE](https://en.wikipedia.org/wiki/T-distributed_stochastic_neighbor_embedding)

### Results and Conclusion

From this clustering analysis done on the Preseidential Debate, we can see the effectiveness of having clustering to group similar ideas together. There are plenty of use-cases for these and as such, can be generalised to other problems and data sets as well. Further steps to explore the clustering method would be to have different levels of abstraction.
 
Example of the different levels of abstraction: <br>
An example using the Youtube video: Coronavirus Ramps Up in the U.S. and Claims Herman Cain | The Daily Social Distancing Show [(Youtube link)](https://www.youtube.com/watch?v=yIwuzldM7HQ)<br>
Comments:
- Herman Cain survive cancer. Herman Cain didn't survive Trump stupidity. 
- Covid-19: "I attack everyone, especially African Americans, elderly people, and people who don't wear a mask or social distance in public spaces."
- Herman Cain (74 year old African American, with no mask on, in a Trump rally): "Masks will not be mandatory.... People are fed up."

**[José Gomes](https://www.youtube.com/channel/UCOzhu7x9YPjoijyzO0WV8wA)** [1 day ago](https://www.youtube.com/watch?v=yIwuzldM7HQ&lc=UgxIPbruQ-UeJx-bUCB4AaABAg)

Herman Cain: Coronavirus doesn’t exist
Coronavirus: Herman Cain doesn’t exist

Hermain Cain to himself after he tested positive:
                    “awwww shucky ducky...”

Herman Cain: There is no pandemic.
Pandemic: There is no Herman Cain.

![https://s3-us-west-2.amazonaws.com/secure.notion-static.com/926655e0-4f75-4db4-9847-bd9e7d86b6e6/Screenshot_2020-08-02_at_9.12.37_PM.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/926655e0-4f75-4db4-9847-bd9e7d86b6e6/Screenshot_2020-08-02_at_9.12.37_PM.png)

Abstracted overview:

Level 1: 

- Hermain Cain is a African American who does not believe in covid and died from it
- Hermain Cain has cancer
- Donald Trump does not believe in covid

Level 2: 

- H



<div>Icons made by <a href="https://www.flaticon.com/authors/flat-icons" title="Flat Icons">Flat Icons</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>