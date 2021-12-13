# [Presidential Debate Youtube Comments Clustering](https://boringppl.github.io/presidential_debates_comments_clustering/)

### Introduction
It was two weeks before the election. The foremost question on netizens' minds was who the next President of the United States would be. Thousands of commentators held forth on poll results and election probabilities, sharing their views on a myriad of digital platforms. As Data Scientists, we marvelled at the richness and variety of political discussion online, and wondered if we could use them to understand the key topics surrounding each candidate. The comments section of uploaded presidential debates on Youtube seemed particularly promising - that's where our journey begins.

Our goal is to analyse Youtube video comments to sieve out the key topics of discussion relevant to each candidate. We focus on two Youtube videos, namely the [first](https://www.youtube.com/watch?v=wW1lY5jFNcQ) and [second](https://www.youtube.com/watch?v=bPiofmZGb8o) presidential debates between Donald Trump and Joe Biden. We hope that this analysis would provide insight on the key concerns of Youtube commenters, which could serve as another indicator of election outcomes given Youtube's prevalance as the foremost website worldwide in traffic (8.6B monthly visits)<sup>[1](https://www.businessofapps.com/data/youtube-statistics/)</sup>. 

![](https://i.imgur.com/8L4hQmw.png)

While this exploration focuses on the 2020 US elections, our approach can be applied to a range of use cases. Youtube videos draw up to hundreds of thousands of comments, making it difficult for their creators to get a sense of the core ideas discussed. With our tool, an influencer can quickly understand the key topics that are most relevant to their audience, and tailor their response accordingly. This concept can also be extended to customer service chats or text-based surveys with a large number of respondents.

### Caveats
 
*First*, given that the demographics of Youtube users swings towards youths aged 18-34<sup>[2](https://www.businessofapps.com/data/youtube-statistics/)</sup>, there may be a risk of biased sampling amongst younger voters. That said, there is still significant engagement on Youtube from people of other age groups.

*Second*, the results of our analysis cannot be used as a stand-alone predictor of election outcomes. This is because Youtube commenters are not representative of the voting population, with many of them coming from overseas. There may also be gap between what commenters express online and their actual behavior at the polls. In addition, presidential election results use the Electoral College system, which are not directly correlated to votes cast.

### Overall Architecture Plan (TLDR of the whole flow) 

![](https://i.imgur.com/nhy4RtF.png)
​
We had four major considerations:

1. **Pulling data using Youtube API**: We had the option to either scrape the specific Youtube site using beautifulSoup (with some potential legal concerns) or extract data through the Youtube API. In this case, we assessed that the latter would be more robust, and our procedure is [described in detail here](https://boringppl.github.io/presidential_debates_comments_clustering/YOUTUBE_API).
2. **Exploratory data analysis and data cleaning**: The first step in any ML project is to print the data to get a sense of its edge cases. We expected user-generated comments to be messy, and anticipated needing to manage emojis and repeated words. 
3. **Encoding sentences into embeddings**: In conducting text analysis, we need to represent raw text with a vector that can act as input for the algorithms. Also known as embeddings, these vectors are essentially arrays of numbers, which combine to indicate the meaning of the underlying words or paragraphs. There are a few popular libraries that transform sentences to embeddings. In exploring the [Universal Sentence encoder](https://tfhub.dev/google/universal-sentence-encoder/4) and [SentenceBert](https://arxiv.org/abs/1908.10084) (more details subsequently), we randomly selected 30 comments and created a similarity matrix to compare both libraries. We found the Universal Sentence encoder to be the most accurate in terms of representing central core ideas in terms of comments.
4. **Clustering using different methods**: After the comments had been converted into vectors, the next step was to cluster the vectors. While clustering algorithms can group similar vectors together, it can be difficult to find similarities when the number of dimensions (i.e. number of items in an array) is too large. To mitigate this, we tranformed our data from a higher- to lower-dimensional space, adopting three clustering methods (detailed below): Principal Component Analysis (PCA), Uniform Manifold Approximation and Projection (UMap), and t-distributed Stochastic Neighbor Embedding (t-SNE).


We will now elaborate on the latter three sections.


### Exploratory Data Analysis and Data Cleaning
We began by looking through some of the comments, which helped us understand the structure of data and the amount of cleaning required. We were also able to gauge the average sentence length and amount of data, giving us a better sense of the hardware needed for processing. 

Here are some examples of the extracted comments:


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

We then proceeded to clean the text and prepare it for the next stage. This entailed standardising the text to lowercase, and removing special characters. We also needed to translate emojis into text, for which we utilised the emoji library<sup>[3](https://pypi.org/project/emoji/)</sup>. 

For example, the demojize function from the emoji library turns

> Biden when trump is talking: 😄

into
> Biden when trump is talking: :grinning face with smiling eyes:<br>

### Encoding Sentences into Embeddings
The next step was to convert the text into word embeddings for the clustering model. We experimented with BERT<sup>[4,](https://huggingface.co/sentence-transformers/bert-base-nli-mean-tokens)</sup><sup>[5](https://medium.com/genei-technology/richer-sentence-embeddings-using-sentence-bert-part-i-ce1d9e0b1343) </sup> embeddings and the Universal Sentence Encoder<sup>[6](https://tfhub.dev/google/universal-sentence-encoder/4)</sup>.

BERT, short for Bidirectional Encoder Representations from Transformers, uses a masked language model (MLM) that randomly masks some input tokens so as to predict the masked word using the other unmasked tokens in the sentence. While BERT is very good at generating word embeddings, Sentence-BERT (SBERT)<sup>[7](https://arxiv.org/pdf/1908.10084.pdf)</sup> builds on it to generate sentence embeddings. In its construction, SBERT was trained on on the Stanford Natural Language Inference (SNLI) and MultiNLI datasets. They collectively contain a million sentence pairs, each annotated to contradict, entail, or be neutral relative to one another. The illustration below shows SBERT applied in an Classification Objective Function. It passes two sentences through the same BERT network with similar weights (i.e. siamese network structure), adds a pooling operation to derive a fixed-size sentence embedding, and compares the output to determine the similarity between their meanings (aka semantic similarity). The weight for the Softmax function is trained to classify contradictory, entailed, and neutral sentences with as high a probability as possible. 
<center><img src="https://i.imgur.com/KsiAhSD.png" width="500"/></center>

On the other hand, the Universal Sentence Encoder converts tokens into vectors by computing the element-wise sum of the representations at each word position. The ordering and identity of the other words in the sentence are taken into account to produce the embedding. 

The model is optimized for text that is longer than words, such as sentences, phrases or short paragraphs. It is trained on a variety of data sources and tasks with the aim of dynamically accommodating a wide range of natural language understanding tasks. The input is variable length English text and the output is a 512-dimensional vector. Check out this [sample notebook](https://colab.research.google.com/github/tensorflow/hub/blob/master/examples/colab/semantic_similarity_with_tf_hub_universal_encoder.ipynb#scrollTo=BnvjATdy64eR) to intuit how well the Universal Sentence Encoder performs in determining semantic similarity. 
![](https://i.imgur.com/NdQXjiD.png)
We explored both types of embeddings, and you can check out our implementation in [GitHub](https://github.com/boringPpl/presidential_debates_comments_clustering). In gist, we passed sentences from comments into both SBERT and Universal Sentence Encoder, such as those below. We numbered them for reference below. Note that '\n' indicates a new line.

<font size="1"> PS: We ran out of memory when passing the whole array into the Universal Sentence Encoder, so we embedded our data in batches of 500. </font> 

<!--- Cutting down this part, it takes up too much real estate
> 25:28 Trump: Did you hear anything?\nBiden: No what was that sound. <br>
> 53:39 trump the idiot.\nYour the big man! I dont know if you are.. BUT YOUR THE BIG MAN.. which is it trump.. Grammer helps.. <br>
> Trump is the President of the USA !  no biden...<br>

> Driving home from school today because that Wednesday I’m going to schools for the day so I’m not going out of the house to get wills house <br>

> Trump won election the swamp rats in Washington did everything they could to cheat in order to have Biden win. Congrats you now have the power and this country and all we can do is sit around and watch you waste our money change the constitution do whatever they want and clearly I don't see our country strong and proud. This election was a disgrace 75 million people voted for president Trump and the few swing states should be ashamed of themselves for being pushed around to be bullied into being dishonest. No one on Trump side believes for one second that sleepy Joe won.  He is not my president.  I am sad, angry frustrated and upset so pelosi and shumner shame on you.  You have not done 1 thing for the American people. You are the reason we all want term limits because you don't deserve to be in government.   Do us all a favor. Retire <br>

> Biden looks too old <br>
> how many memes?
> I feel like disliking comments cause ain't nobody disliking sht. Not personal just cause its empty. Its ungodly to leave open space <br>

> Men and Women are entertained by this debate. What about 3rd genders?<br>
> I like <br>
> The lackadaisical dash histologically boast because select theoretically clean to a hoc health. sedate, late room <br>
> Cmon man. <br>
> Is he still under audit? <br>

> “The show will start very soon” She had no idea what kind of show she was talking about. <br>
> Chad Trump vs Demented Biden <br>
> TRAMP JE DRUGI KENEDI POBEDICE ISTINA <br>
> Biden by a landslide. He stomped Trump! <br>
> Trump is right about the corona virus we cannot shut down everything I've been tested positive for corona virus and it went away next time I tested so it does indeed go away <br>
> To be honest, I am amazed they allowed comments on this video <br>
--->

> 1. 25:28 Trump: Did you hear anything?\nBiden: No what was that sound. <br>
> 2. Trump is the President of the USA !  no biden...<br>
> 3. Trump won election the swamp rats in Washington did everything they could to cheat in order to have Biden win. Congrats you now have the power and this country and all we can do is sit around and watch you waste our money change the constitution do whatever they want and clearly I don't see our country strong and proud. This election was a disgrace 75 million people voted for president Trump and the few swing states should be ashamed of themselves for being pushed around to be bullied into being dishonest. No one on Trump side believes for one second that sleepy Joe won.  He is not my president.  I am sad, angry frustrated and upset so pelosi and shumner shame on you.  You have not done 1 thing for the American people. You are the reason we all want term limits because you don't deserve to be in government.   Do us all a favor. Retire <br>
> 4. Biden looks too old <br>
> 5. how many memes? <br>
> 6. The lackadaisical dash histologically boast because select theoretically clean to a hoc health. sedate, late room <br>
> 7. “The show will start very soon” She had no idea what kind of show she was talking about. <br>
> 8. Chad Trump vs Demented Biden <br>
> 9. TRAMP JE DRUGI KENEDI POBEDICE ISTINA <br>
> 10. Biden by a landslide. He stomped Trump! <br>

We ran 20 such comments through the Univeral Sentence Encoder as well as SBERT. We plotted the results in a confusion matrix below to visualise the similarity of the sentence vectors. The darker the colours, the more similar the models deemed the two sentences.

Universal Sentence Encoder | SBERT
:-------------------------:|:-------------------------:
![](https://i.imgur.com/FtOXTda.png)  |  ![](https://i.imgur.com/euVe4ab.png)

Interestingly, we can immediately see that the Universal Sentence Encoder did much better than SBERT at observing a range of semantic similarity between different sentence pairs, compared to SBERT which found many of them very similar. Here are the sentences that the Universal Sentence Encoder found similar. We renumbered them by serial number from the 10 above for brevity:

- Sentences 2 and 3
    > SN2. Trump is the President of the USA !  no biden... <br>
    > SN3. Trump won election the swamp rats in Washington did everything they could to cheat in order to have Biden win. ...
- Sentences 2 and 4
    > SN2. Trump is the President of the USA !  no biden... <br>
    > SN4. Biden looks too old
- Sentences 2 and 8
    > SN2. Trump is the President of the USA !  no biden... <br>
    > SN8. Chad Trump vs Demented Biden
- Sentences 2 and 10
    > SN2. Trump is the President of the USA !  no biden... <br>
    > SN10. Biden by a landslide. He stomped Trump!
- Sentences 8 and 10
    > SN8. Chad Trump vs Demented Biden <br>
    > SN10. Biden by a landslide. He stomped Trump!

We can see that the Universal Sentence Encoder performed was fairly accurate, except with the final comparison between sentences 8 and 10. Perhaps the association between 'landslide' and a positive or winning sentiment was not strong enough in the model's training. Hence we decided to use the Universal Sentence Encoder for the next step of our analysis.

### Dimension reduction using different methods

We experimented with 3 dimension reducing techniques on our cleaned dataset: PCA, UMap and t-SNE.

#### [Principal Component Analysis (PCA)](https://hackernoon.com/principal-component-analysis-unsupervised-learning-model-8f18c7683262)  
PCA is a popular unsupervised learning technique used to visualise higher-dimension data while preserving most of the variance. It is generally used to reduce higher-dimension data into lower dimensions for other clustering algorithms to be subsequently applied.

PCA works by first computing the covariance amongst all possible pairs of the variables in the data. Then, it compresses the initial variables into uncorrelated variables called principal components. It does this by solving the eigenvalue/eigenvector problem on the variables, which surface the variables with the highest amount of variance. For example, in the diagram below, the principal component is the green line that maximises the average squared distances from the data points represented by the white dots. This green line explains the largest amount of variance in this dataset.

<center><img src="https://i.imgur.com/1XGopx5.png" width="500"/></center>
![PCA graph from https://liorpachter.wordpress.com/2014/05/26/what-is-principal-component-analysis/]

#### [Uniform Manifold Approximation and Projection (UMAP)](https://en.wikipedia.org/wiki/Nonlinear_dimensionality_reduction#Uniform_manifold_approximation_and_projection) 

UMAP is based on a framework derived from Riemannian geometry and algebraic topology, using a manifold learning technique for dimensionality reduction. It essentially constructs a high-dimensional graph representation of the data, then optimises a low-dimensional graph to be as structually similar as possible.  UMAP scales well and is able to run efficiently on large datasets.

#### [t-distributed Stochsatic Neighbour Embedding (tSNE)](https://en.wikipedia.org/wiki/T-distributed_stochastic_neighbor_embedding) 

tSNE measures the similiarities between data pairs in both the high dimension space and low dimension space. tSNE works very similarly to UMAP, but UMAP is better at preserving global structure in the final projection<sup>[8](https://pair-code.github.io/understanding-umap/#:~:text=UMAP%2C%20at%20its%20core%2C%20works,as%20structurally%20similar%20as%20possible)</sup>. tSNE preserves small pairwise distances unlike PCA, which may result in a more accurate representation of the clusters.

Below is an example of the clustering between UMAP and tSNE, and shows how UMAP is better than tSNE in preserving global structure. While each category in both UMAP and T-SNE is clearly clustered accordingly indicated by the individual colours, similar categories are grouped closer together in UMAP than in T-SNE, thereby preserving the global structure for UMAP.

![](https://i.imgur.com/am5MvOd.png)
<sup>[Image link reference](https://pair-code.github.io/understanding-umap/)</sup>

Comparison between the 3 clustering algorithms on the MNIST dataset:
![](https://i.imgur.com/S48rcgj.jpg)
<sup>[Image link reference](https://uschilaa.github.io/physicsViz/#13)</sup>


### Results

We will now compare the results of using each clustering algorithm on our dataset. The clustering data is stored in the folder `cluster_data/`.  For the first presidential debate, the embeddings and labels are stored in the files `vec1_5k.tsv` and `meta_lab1_5k.tsv` respectively. For the second presidential debate, the corresponding files are: `vec2_5k.tsv` and `meta_lab2_5k.tsv`.

Note that these contain only the embeddings and labels for the first 5000 Youtube comments, due to the difficulty of loading more than 5000 vectors into [projector.tensorflow.org](http://projector.tensorflow.org). For reference, the full set is provided in `vecs1.parquet` and `meta_lab1.parquet` (first presidential debate) and `vecs2.parquet` and `meta_lab2.parquet` (second presidential debate). The [Apache Parquet](https://parquet.apache.org/) format was chosen for portability, as well as to keep the file sizes small.


Comparing the results of these 3 algorithms, UMAP seem to show more distinct clusters. This corresponds to the basis of these 3 algorithms, where UMAP is designed to better preserve the global structure of the data categories.

#### Comparing between HDB Scan and K-Means data points
We then extracted the data points in each of the top clusters after clustering using HDBScan and K-Means respectively to analyse the effectiveness of the clustering methods.

Below shows the clusters of the K-means and HDBscan algorithms.
For the K-means, we used the elbow method to find the optimal value of k which is 8.
![](https://i.imgur.com/opVF08m.png)

For HDBScan we did trial and error with the *cluster size* and *min sample* parameters to get 15 clusters.
![](https://i.imgur.com/z6yWiqj.png)



Drilling down into each individual clusters by HDBScan and K-means, generally clusters by HDBScan were more accurate then K-means though both algorithms were not the most accurate in grouping the same comments together. This could be because the elbow method in K-means show that 8 clusters are "optimal", while we were able to fine-tune it by doing trial and error with the *cluster size* and *min sample* parameters to get 15 clusters.

Let's look at the comments in a cluster about Chris.

For K-Means, comments in that particular cluster are either people feeling bad for Chris, criticising Chris, or praising Chris.

Extract from K-means:
>Poor Chris, he's in the middle of all that [Empathy for Chris] </br></br>
>chris is an idiot [Criticising Chris] </br></br>
>Props to chris for keeping his cool during this [Praising Chris]

While for HDBScan, there is a cluster on Chris as well, however the comments in that cluster were more from people feeling bad for Chris and criticising Chris. They contain somewhat more negative statements.

Extract from HDBScan:
>Poor Chris, I hope he got the day off afterwards [Empathy for Chris] </br></br>
>This Chris dude sucks [Criticising Chris]

We then further experimented with the parameters of the model to try to get better results.  



Comparing between the two, both HDBScan and K-means were not able to separate comments at a level of nuance that native English speakers would be able to group them separately. Both algorithms were able to understand that the comments were about Chris, but fail to understand the context about Chris. In the aspect of understanding the context, HDBScan seemed to perform slightly better than K-means and had relatively more negative statements in a single cluster. You can explore the clusters of text [here](https://docs.google.com/spreadsheets/d/1P9Hhzss79JxpgFtS5aEaYPaGneomMFsPxkLH_1uCyCU/edit#gid=166516754) 



### Conclusion
From this clustering analysis done on the Presidential Debate, there is no definite conclusion that a certain clustering algorithm is the best for this use-case. However, we can see the effectiveness of implementing clustering to group similar ideas together. There are plenty of use-cases for these and as such, can be generalised to other problems and data sets as well. An example of further steps to explore the clustering method would be to have different levels of abstraction.
 
Example of the different levels of abstraction: <br>
An example using the Youtube video: Coronavirus Ramps Up in the U.S. and Claims Herman Cain | The Daily Social Distancing Show [(link)](https://www.youtube.com/watch?v=yIwuzldM7HQ)<br>
Comments:
- Herman Cain survive cancer. Herman Cain didn't survive Trump stupidity. 
- Covid-19: "I attack everyone, especially African Americans, elderly people, and people who don't wear a mask or social distance in public spaces."
- Herman Cain (74 year old African American, with no mask on, in a Trump rally): "Masks will not be mandatory.... People are fed up."


Abstracted overviews:


- Hermain Cain is a African American who does not believe in covid and died from it
- Hermain Cain has cancer
- Donald Trump does not believe in covid

We have also identified some limitations that can be worked on to improve the accuracy of this analysis. Firstly, we have assumed that users do not make any spelling mistakes or type in other languages other than english. In addition, online chats realistically contain words in short-forms (eg. brb) and the use of numbers to replace words (eg. up 2 u). These words may not be converted into word embeddings that properly encapsulate the context of the sentence, hence reducing the accuracy of our findings. Secondly, given the computational limitations that we've faced, we could have had a larger and more comprehensive data set to indicate our findings.

This problem is hard because there is no objective function to decide how good the clustering is. As such, picking of parameters for the various clustering functions can seem subjective. For K-means, even with the elbow plot, it is not clear how many clusters we should pick. For HDBScan, the min cluster size and min samples are also hard to tweak. 

In conclusion, though we have shown that there are various use-cases for the usage of clustering techniques and it's usefulness on real world data, but it is still a long way from being production. 


#### Sources and References: 

<div>Icons made by <a href="https://www.flaticon.com/authors/flat-icons" title="Flat Icons">Flat Icons</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>

Image taken from https://tfhub.dev/google/universal-sentence-encoder/4