# [Presidential Debate Youtube Comments Clustering](https://boringppl.github.io/presidential_debates_comments_clustering/)

### Introduction
At the point when we started this project, election week is coming up. There was so much excitement in the air on who is the next US president to be elected. There were thousands of articles on who's leading the polls. The US election has been trending on most, if not all, social media platforms. Being Data Scientists, we wondered if it would be possible to leverage on these different data sources to understand various topics of discussion surrounding each candidate. Of which, we have decided to focus on Youtube comments as a starting point for this project. 

We were aware of the possibility of biased sampling as the demographic report of users on Youtube indicates the highest level of usage from users in the 18-34 age range<sup>[1](https://www.businessofapps.com/data/youtube-statistics/)</sup>, which also correlated to the most technogically savvy group of people. With that being said, there is still a significant number of people using Youtube from other age groups, and with Youtube being the number one site for web traffic worldwide (8.6 billion monthly visits)<sup>[2](https://www.businessofapps.com/data/youtube-statistics/)</sup>. It would be significant to conduct an analysis on the different core ideas of the Youtube comments section, specifically on the US election.

While this exploration covers the US election, the essential parts of the analysis are relevant to many other use-cases. Youtube influencers and content creators can receive hundreds of thousands of comments per video and it is often difficult to get an overview of all the core ideas, and it would not be easy to sift through every comment received in each video. Having an overview or a summary of the different perspectives of the viewers would be useful for them to either create another response video to address their concerns or to reply to each of these "clusters" of ideas. This analysis can also be extended to customer service chats or surveys from large number of users. 

To be clear, this is by no means a predictor of the election results. For example: 1. sample bias (Youtube commenters are not representive of the voting population), 2. not everyone commenting on Youtube or watching these debates is from US, 3. presidential elections use the Electoral College, this differs from casting votes in a direct election.
<br>

We have picked two Youtube videos to focus on.

![](https://i.imgur.com/8L4hQmw.png)

First 2020 Presidential Debate between Donald Trump and Joe Biden uploaded on Youtube
https://www.youtube.com/watch?v=wW1lY5jFNcQ



Second presidential debate uploaded on Youtube
https://www.youtube.com/watch?v=bPiofmZGb8o



For the purpose of this article, we would be focusing on creating a summary of the Youtube comments  found in the Presidential Debate between Donald Trump and Joe Biden as shown in the screenshots above.

### Overall Architecture Plan (TLDR of the whole flow) 


![](https://i.imgur.com/nhy4RtF.png)
​

Here are some of the major considerations when planning out the pieces:
1. **Pulling data from Youtube API**: We had either the option to scrape the site using beautifulSoup (with some potential legal concerns) or to make use of the Youtube API to extract the data. In this case, we felt that the latter approach would be more robust, and our procedure is [described in detail here](https://boringppl.github.io/presidential_debates_comments_clustering/YOUTUBE_API).
2. **Exploratory data analysis and data cleaning**: The first step to any ML project is always to print out the data to get a sense of the edge cases. We will expect the user generated comments to be rather messy. We will need to deal with emojis and repeated words. 
3. **Encoding the sentences**: Running text analysis requires us to change the text into a vector that the algorithms can work with. You can think of vectors as an array of numbers. A combination of these numbers give an indication of the meanings for the words or paragraphs. There are a few popular libraries to change sentences to embeddings. We explored [Universal sentence encoder](https://tfhub.dev/google/universal-sentence-encoder/4) and [SentenceBert](https://arxiv.org/abs/1908.10084). I will go into more details in the later sections, but you can also find plenty of articles explaining each of them in detail online. We randomly selected 30 comments and created a similarity matrix to compare both libraries. We found Universal Sentence encoder to be the most accurate in terms of representing central core ideas in terms of comments. 
    - We randomly selected 30 comments and created a similarity matrix to compare both libraries. We found Universal Sentence encoder to be the most accurate in terms of representing central core ideas in terms of comments.

4. **Exploration of different clustering methods**: After all the comments are converted into vectors, we can now run a standard clustering on these vectors. As the name suggest, clustering algorithms clumps similar vectors together. But it can be difficult to find similarities when the dimensions (dimensions just means number of items in an array) are really high. To help reduce that, we want to tranform the high dimension space to a lower dimension space that matters. [Pincipal Component Analysis](https://en.wikipedia.org/wiki/Principal_component_analysis) helps us do that by meshing all the dimensions down to a stated number. 
    - UMap
    - T-SNE


We will now go into further explanation for each section.


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

Why sentenceBERT https://medium.com/genei-technology/richer-sentence-embeddings-using-sentence-bert-part-i-ce1d9e0b1343

![](https://i.imgur.com/KsiAhSD.png)

As for the Universal Sentence Encoder, the tokens are converted into vectors by computing the element-wise sum of the representations at each word position. This takes into account the ordering and identity of the other words in the sentence to produce the embedding. Embeddings produced are approximately normalized. 

The model is trained and optimized for greater-than-word length text, such as sentences, phrases or short paragraphs. It is trained on a variety of data sources and a variety of tasks with the aim of dynamically accommodating a wide variety of natural language understanding tasks. The input is variable length English text and the output is a 512 dimensional vector. Here is a [sample notebook](https://colab.research.google.com/github/tensorflow/hub/blob/master/examples/colab/semantic_similarity_with_tf_hub_universal_encoder.ipynb#scrollTo=BnvjATdy64eR) to give an intuition of how well Universal Sentence Encoder perform for semantic similarity. 
![](https://i.imgur.com/NdQXjiD.png)

Usage of both embeddings can be found in the github notebook: comments_clustering.ipynb.
For the following sections, we used the embedding produced by the Unversal Sentence Encoder because of its efficiency, since we face a memory limitation.


### Clustering of intents

We've applied 3 clustering techniques: UMAP and T-SNE on our cleaned dataset.

### Preprocessing 
PCA(https://en.wikipedia.org/wiki/Principal_component_analysis) stands for Principal Component Analysis which serves as a popular technique to visualise higher dimension data, while preserving as much variance as possible. It is an unsupervised learning technique to form clusters by solving the  eigenvalue/eigenvector problem on the variables.

There are as many principal components as data variables. The principal component is a line that maximises the average squared distances from the projected points represented by the white dots.

![PCA graph from https://liorpachter.wordpress.com/2014/05/26/what-is-principal-component-analysis/](https://i.imgur.com/1XGopx5.png)


Uniform Manifold Approximation and Projection (UMAP)(https://en.wikipedia.org/wiki/Nonlinear_dimensionality_reduction#Uniform_manifold_approximation_and_projection) uses a framework based in Riemannian geometry and algebraic topology. It uses a manifold learning technique for dimensionality reduction. UMAP scales well and is able to run efficiently on large datasets.

(insert graph of cluster)

T-SNE(https://en.wikipedia.org/wiki/T-distributed_stochastic_neighbor_embedding), short for t-distributed Stochastic Neighbor Embedding, measures the similiarities between data pairs in both the high dimension space and low dimension space. T-SNE works very similarly to UMAP, but UMAP is better at preserving global structure in the final projection.https://pair-code.github.io/understanding-umap/#:~:text=UMAP%2C%20at%20its%20core%2C%20works,as%20structurally%20similar%20as%20possible. T-SNE preserves small pairwise distances unlike PCA, which may result in a more accurate representation of the clusters.

(insert graph of cluster)

### Results and Conclusion

(insert results here)

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

- 


#### Sources and attribution: 

<div>Icons made by <a href="https://www.flaticon.com/authors/flat-icons" title="Flat Icons">Flat Icons</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>

Image taken from https://tfhub.dev/google/universal-sentence-encoder/4