# [Presidential Debate Youtube Comments Clustering](https://boringppl.github.io/presidential_debates_comments_clustering/)

### Introduction
At the point when we started this project, election week was coming up. There was so much anticipation in the air on who would be the next US president to be elected. There were thousands of articles on who's leading the polls. The US election has been trending on most, if not all, social media platforms. As Data Scientists, we wondered if it would be possible to leverage on these different data sources to understand various topics of discussion surrounding each candidate. Of which, we have decided to focus on Youtube comments as a starting point for this project. 

We were aware of the possibility of biased sampling as the demographic report of users on Youtube indicates the highest level of usage from users in the 18-34 age range<sup>[1](https://www.businessofapps.com/data/youtube-statistics/)</sup>, which also correlated to the most technologically savvy group of people. With that being said, there is still a significant number of people using Youtube from other age groups, and with Youtube being the number one site for web traffic worldwide (8.6 billion monthly visits)<sup>[2](https://www.businessofapps.com/data/youtube-statistics/)</sup>. It would be significant to conduct an analysis on the different core ideas of the Youtube comments section, specifically on the US election.

While this exploration covers the US election, the essential parts of the analysis are relevant to many other use-cases. Youtube influencers and content creators can receive hundreds of thousands of comments per video and it is often difficult to get an overview of all the core ideas, and it would not be easy to sift through every comment received in each video. Having an overview or a summary of the different perspectives of the viewers would be useful for them to either create another response video to address their concerns or to reply to each of these "clusters" of ideas. This analysis can also be extended to customer service chats or surveys from large number of users. 

To be clear, this is by no means a predictor of the election results. For example: 1. sample bias (Youtube commenters are not representive of the voting population), 2. not everyone commenting on Youtube or watching these debates is from US, 3. presidential elections use the Electoral College, this differs from casting votes in a direct election.
<br>

We have picked two Youtube videos to focus on.

![](https://i.imgur.com/8L4hQmw.png)

First 2020 Presidential Debate between Donald Trump and Joe Biden uploaded on Youtube:
https://www.youtube.com/watch?v=wW1lY5jFNcQ



Second presidential debate uploaded on Youtube:
https://www.youtube.com/watch?v=bPiofmZGb8o



For the purpose of this article, we would be focusing on creating a summary of the Youtube comments  found in the Presidential Debate between Donald Trump and Joe Biden as shown in the screenshots above.

### Overall Architecture Plan (TLDR of the whole flow) 


![](https://i.imgur.com/nhy4RtF.png)
​

Here are some of the major considerations when planning out the pieces:
1. **Pulling data from Youtube API**: We had the option to either scrape the site using beautifulSoup (with some potential legal concerns) or to make use of the Youtube API to extract the data. In this case, we felt that the latter would be more robust, and our procedure is [described in detail here](https://boringppl.github.io/presidential_debates_comments_clustering/YOUTUBE_API).
2. **Exploratory data analysis and data cleaning**: The first step to any ML project is always to print out the data to get a sense of the edge cases. We will expect the user generated comments to be rather messy. We will need to deal with emojis and repeated words. 
3. **Encoding the sentences**: Running text analysis requires us to change the text into a vector that the algorithms can work with. You can think of vectors as an array of numbers. A combination of these numbers give an indication of the meanings for the words or paragraphs. There are a few popular libraries to change sentences to embeddings. We explored [Universal sentence encoder](https://tfhub.dev/google/universal-sentence-encoder/4) and [SentenceBert](https://arxiv.org/abs/1908.10084). I will go into more details in the later sections, but you can also find plenty of articles explaining each of them in detail online. We randomly selected 30 comments and created a similarity matrix to compare both libraries. We found Universal Sentence encoder to be the most accurate in terms of representing central core ideas in terms of comments. 
    - We randomly selected 30 comments and created a similarity matrix to compare both libraries. We found Universal Sentence encoder to be the most accurate in terms of representing central core ideas in terms of comments.

4. **Exploration of different clustering methods**: After all the comments are converted into vectors, we ran a standard clustering on these vectors. As the name suggests, clustering algorithms clump similar vectors together, but it can be difficult to find similarities when the dimensions (number of items in an array) are too large. To mitigate this, we want to tranform our data from a higher dimensional space to a lower dimensional space that provides more value in our analysis. [Principal Component Analysis](https://en.wikipedia.org/wiki/Principal_component_analysis) helps us do that by meshing all the dimensions down to a stated number. 
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

The usual cleaning of text was done, namely standardising the text to lowercase, and the removal of special characters.

### Word Embedding
After cleaning the data, we have to convert the text into word embeddings for the clustering model. We experimented with Bert<sup>[4](https://huggingface.co/sentence-transformers/bert-base-nli-mean-tokens)</sup> embeddings and Universal Sentence Encoder<sup>[5](https://tfhub.dev/google/universal-sentence-encoder/4)</sup>.

BERT, short for Bidirectional Encoder Representations from Transformers, uses a masked language model(MLM) that randomly masks some tokens of the input such that the aim is to predict accurately the masked word using the other unmasked tokens in the sentence. 

Why sentenceBERT https://medium.com/genei-technology/richer-sentence-embeddings-using-sentence-bert-part-i-ce1d9e0b1343

![](https://i.imgur.com/KsiAhSD.png)

As for the Universal Sentence Encoder, the tokens are converted into vectors by computing the element-wise sum of the representations at each word position. This takes into account the ordering and identity of the other words in the sentence to produce the embedding. Embeddings produced are approximately normalized. 

The model is trained and optimized for greater-than-word length text, such as sentences, phrases or short paragraphs. It is trained on a variety of data sources and a variety of tasks with the aim of dynamically accommodating a wide variety of natural language understanding tasks. The input is variable length English text and the output is a 512 dimensional vector. Here is a [sample notebook](https://colab.research.google.com/github/tensorflow/hub/blob/master/examples/colab/semantic_similarity_with_tf_hub_universal_encoder.ipynb#scrollTo=BnvjATdy64eR) to give an intuition of how well Universal Sentence Encoder perform for semantic similarity. 
![](https://i.imgur.com/NdQXjiD.png)

Usage of both embeddings can be found in the github notebook: comments_clustering.ipynb.
For the following sections, we used the embedding produced by the Unversal Sentence Encoder because of its efficiency. 

Here is the list of sentenses that are passed into both sentense-bert and Universal sentence encoder: 
- 25:28 Trump: Did you hear anything?\nBiden: No what was that sound.
- 53:39 trump the idiot.\nYour the big man! I dont know if you are.. BUT YOUR THE BIG MAN.. which is it trump.. Grammer helps..
- Trump is the President of the USA !  no biden...
- Driving home from school today because that Wednesday I’m going to schools for the day so I’m not going out of the house to get wills house
- Trump won election the swamp rats in Washington did everything they could to cheat in order to have Biden win. Congrats you now have the power and this country and all we can do is sit around and watch you waste our money change the constitution do whatever they want and clearly I don't see our country strong and proud. This election was a disgrace 75 million people voted for president Trump and the few swing states should be ashamed of themselves for being pushed around to be bullied into being dishonest. No one on Trump side believes for one second that sleepy Joe won.  He is not my president.  I am sad, angry frustrated and upset so pelosi and shumner shame on you.  You have not done 1 thing for the American people. You are the reason we all want term limits because you don't deserve to be in government.   Do us all a favor. Retire
- Biden looks too old
- how many memes?
- I feel like disliking comments cause ain't nobody disliking sht\nNot personal just cause its empty \nIts ungodly to leave open space
- I feel like disliking comments cause ain't nobody disliking sht\nNot personal just cause its empty \nIts ungodly to leave open space
- Men and Women are entertained by this debate. What about 3rd genders?
- I like
- The lackadaisical dash histologically boast because select theoretically clean to a hoc health. sedate, late room
- Cmon man.
- Is he still under audit?
- “The show will start very soon”\nShe had no idea what kind of show she was talking about.
- Chad Trump vs Demented Biden
- TRAMP JE DRUGI KENEDI POBEDICE ISTINA
- Biden by a landslide. He stomped Trump!
- Trump is right about the corona virus we cannot shut down everything I've been tested positive for corona virus and it went away next time I tested so it does indeed go away
- To be honest, I am amazed they allowed comments on this video

We ran a confusion metrix to visualise the similarity of the vectors for 20 comments: 

![](https://i.imgur.com/FtOXTda.png)
Confusion metrix for Universal Sentence encoder
![](https://i.imgur.com/euVe4ab.png)
Confusion metrix for Sentence Bert

Universal Sentence Encoder found these sentences similar

sentence 3 and 5
- Trump is the President of the USA !  no biden...
- Trump won election the swamp rats in Washington did everything they could to cheat in order to have Biden win. Congrats you now have the power and this country and all we can do is sit around and watch you waste our money change the constitution do whatever they want and clearly I don't see our country strong and proud. This election was a disgrace 75 million people voted for president Trump and the few swing states should be ashamed of themselves for being pushed around to be bullied into being dishonest. No one on Trump side believes for one second that sleepy Joe won.  He is not my president.  I am sad, angry frustrated and upset so pelosi and shumner shame on you.  You have not done 1 thing for the American people. You are the reason we all want term limits because you don't deserve to be in government.   Do us all a favor. Retire

sentence 3 and 6
- Trump is the President of the USA !  no biden...
- Biden looks too old

sentence 3 and 16
- Trump is the President of the USA !  no biden...
- Chad Trump vs Demented Biden

sentence 3 and 18
- Trump is the President of the USA !  no biden...
- Biden by a landslide. He stomped Trump!

sentence 16 and 18
- Chad Trump vs Demented Biden
- Biden by a landslide. He stomped Trump!

It is interesting to observe that universal sentence encoder did significant better than sentense bert. It could pick out most of the sentences correctly. It seems like it got sentence 18 pretty wrong. It is possible that Biden by a landslide is not commonly used to denote positive context. 

PS: In the final code, we faced a memory limitation using universal sentence encoder. We ran out of memory trying to run the whole array. To bypass this, we embedded our data in batches of 500. 

### Clustering of intents

We've applied 3 clustering techniques: PCA, UMAP and T-SNE on our cleaned dataset.

#### PCA 
PCA<sup>[5](https://en.wikipedia.org/wiki/Principal_component_analysis)</sup> stands for Principal Component Analysis which serves as a popular technique to visualise higher dimension data, while preserving as much variance as possible. It is an unsupervised learning technique to form clusters by solving the  eigenvalue/eigenvector problem on the variables.

There are as many principal components as data variables. The principal component is a line (green line represented below) that maximises the average squared distances from the projected points represented by the white dots.

![PCA graph from https://liorpachter.wordpress.com/2014/05/26/what-is-principal-component-analysis/](https://i.imgur.com/1XGopx5.png)

#### UMAP
Uniform Manifold Approximation and Projection (UMAP)<sup>[6](https://en.wikipedia.org/wiki/Nonlinear_dimensionality_reduction#Uniform_manifold_approximation_and_projection)</sup> uses a framework based in Riemannian geometry and algebraic topology. It uses a manifold learning technique for dimensionality reduction. UMAP scales well and is able to run efficiently on large datasets.

#### T-SNE
T-SNE<sup>[7](https://en.wikipedia.org/wiki/T-distributed_stochastic_neighbor_embedding)</sup>, short for t-distributed Stochastic Neighbor Embedding, measures the similiarities between data pairs in both the high dimension space and low dimension space. T-SNE works very similarly to UMAP, but UMAP is better at preserving global structure in the final projection<sup>[8](https://pair-code.github.io/understanding-umap/#:~:text=UMAP%2C%20at%20its%20core%2C%20works,as%20structurally%20similar%20as%20possible)</sup>. T-SNE preserves small pairwise distances unlike PCA, which may result in a more accurate representation of the clusters.

Below is an example of the clustering between UMAP and T-SNE, and how UMAP is better than T-SNE in preserving global structure. While each category in both UMAP and T-SNE is clearly clustered accordingly indicated by the individual colours, similar categories are grouped closer together in UMAP than in T-SNE, thereby preserving the global structure for UMAP.

![](https://i.imgur.com/am5MvOd.png)
<sup>[Image link reference](https://pair-code.github.io/understanding-umap/)</sup>

Comparison between the 3 clustering algorithms on the MNIST dataset:
![](https://i.imgur.com/S48rcgj.jpg)
<sup>[Image link reference](https://uschilaa.github.io/physicsViz/#13)</sup>



### Results and Conclusion

We will now compare the results of each of the clustering algorithms run on our dataset.

(insert results here: PCA, UMAP, T-SNE)

Results for PCA:

Results for UMAP:

Results for T-SNE:


From this clustering analysis done on the Presidential Debate, we can see the effectiveness of implementing clustering to group similar ideas together. There are plenty of use-cases for these and as such, can be generalised to other problems and data sets as well. An example of further steps to explore the clustering method would be to have different levels of abstraction.
 
Example of the different levels of abstraction: <br>
An example using the Youtube video: Coronavirus Ramps Up in the U.S. and Claims Herman Cain | The Daily Social Distancing Show [(Youtube link)](https://www.youtube.com/watch?v=yIwuzldM7HQ)<br>
Comments:
- Herman Cain survive cancer. Herman Cain didn't survive Trump stupidity. 
- Covid-19: "I attack everyone, especially African Americans, elderly people, and people who don't wear a mask or social distance in public spaces."
- Herman Cain (74 year old African American, with no mask on, in a Trump rally): "Masks will not be mandatory.... People are fed up."


Abstracted overview:


- Hermain Cain is a African American who does not believe in covid and died from it
- Hermain Cain has cancer
- Donald Trump does not believe in covid

We have also identified some limitations that can be worked on to improve the accuracy of this analysis. Firstly, we have assumed that users do not make any spelling mistakes or type in other languages other than english. In addition, online chats realistically contain words in short-forms (eg. brb) and the use of numbers to replace words (eg. up 2 you). These words may not be converted into word embeddings that properly encapsulate the context of the sentence. Secondly, given the computational limitations that we've faced, we could have had a larger and more comprehensive data set to indicate our findings.

In conclusion, there are various use-cases for the usage of clustering techniques and it's usefulness on real world data.




#### Sources and References: 

<div>Icons made by <a href="https://www.flaticon.com/authors/flat-icons" title="Flat Icons">Flat Icons</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>

Image taken from https://tfhub.dev/google/universal-sentence-encoder/4