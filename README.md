# Background

nVidia and AMD are major fabless chip designers. nVidia is more GPU focused than AMD, but up until Spring 2022 (with the entry of Intel Arc GPUs), the GPU market has been an AMD - nVidia duopoly since around the year 2000 with the exit of pioneers such as 3dfx.

For many years, AMD has been seen as the "budget option", with their GPUs retailing at lower prices than nVidia GPUs of similar performance. In terms of CPUs, AMD fell far behind nVidia and consigned us to years of being stuck with quad core CPUs as Intel lost their willingness to innovate. This changed with the introduction of chiplets in Ryzen CPUs. AMD is now attempting to break away from monolithic designs in their GPUs as well with RDNA3. 

However, the market perception of AMD being the weaker budget option still persists, and users constantly complain about driver issues.

# Problem Statement

## AUDIENCE:

AMD Strategic Planners (Consumer GPUs)

## PROBLEM:

As stated above, there is a perception that AMD's consumer GPUs are inferior to nVidia's consumer GPUs.

It is unclear whether the perception of AMD products being more problematic is a marketing or an engineering issue. If it is genuinely an engineering issue, we would expect to see many more negative posts on r/amd than r/nvidia. If the negative posts are similar, then it is likely a marketing issue. The theory is as follows:

1. Both subreddits are moderated - negative posts such as "amd sucks" without specific reference to a problem the poster is facing gets removed.

2. We would therefore only expect there to be negative posts about actual problems.

3. If a higher proportion of posts on r/amd is negative than on r/nvidia, then it is likely that there is a genuine issue with AMD QA, which should be addressed.

4. If a similar proportion of posts on both subreddits are negative, then it is a perception issue which can be corrected by the deployment of marketing resources.

## OBJECTIVES:

1. The model has to be able to differentiate between comments about AMD and nVidia for more widespread deployment (in the event that becomes necessary).

2. The same data can be used to determine where (marketing or engineering) AMD should deploy resources to improve the perception of their product (see problem above).

## SCOPE:

1. Use text data posted to Reddit on the r/amd and r/nvidia subreddits to build a model to differentiate between text about AMD and text about nVidia. 

2. The purpose of modelling is to be able to use the model on other GPU discussion forums with no split between posts about AMD/nVidia in order to apply the same sentiment analysis tools we are applying to the Reddit dataset.

3. Use sentiment analysis tools to establish whether the perception is driven by nVidia's mindshare or by a genuine engineering problem.
 
## DATA:

1. Titles, descriptions, and comments posted to r/amd and r/nvidia.

## METHODS AND TOOLS:

1. Naive Bayes.

2. Random Forest.

3. Boosted Models.

4. Simple Sequential Neural Network.

## SUCCESS METRICS:

1. Precision.

2. Sentiment Analysis.

# Hardware and Hardware-related Requirements

CUDA compatible GPU: https://developer.nvidia.com/cuda-gpus

CUDA >= 11.8

Note: The version of PyTorch implemented has been tested with and is compatible with CUDA 12.2.

### notebook requirements:

gensim              4.3.2

matplotlib          3.7.2

nltk                3.8.1

numpy               1.25.2

pandas              2.1.0

scipy               1.11.2

session_info        1.0.0

sklearn             1.3.0

swifter             1.4.0

torch               2.0.1+cu118

torchmetrics        1.1.2

vaderSentiment      NA

wordcloud           1.9.2

xgboost             2.0.0

### .py files requirements:

certifi==2023.7.22

charset-normalizer==3.2.0

idna==3.4

numpy==1.25.2

pandas==2.1.0

praw==7.7.1

prawcore==2.3.0

python-dateutil==2.8.2

pytz==2023.3.post1

requests==2.31.0

six==1.16.0

tzdata==2023.3

update-checker==0.18.0

urllib3==2.0.4

websocket-client==1.6.2

# Modelling Conclusions

### Model Performance and Time Taken
|Model|Train Score|Test Score|Precision|Recall|F1-Score|Fit time|
|---|---|---|---|---|---|---|
|Naive Bayes with cvec|0.990|0.944|0.909|0.820|0.862|18s|
|Naive Bayes with tvec|0.993|0.941|0.915|0.739|0.818|14s|
|Random Forest with tvec|0.999|0.937|0.932|0.736|0.823|43s|
|Adaboost with tvec|0.999|0.913|0.885|0.735|0.819|58s|
|Gradient Boost with tvec|0.999|0.937|0.922|0.737|0.819|2m 12s|
|XGBoost with tvec|0.573|0.477|0.493|0.637|0.556|33s (CUDA)|
|Sequential Neural Net with tvec|N/A|0.865|0.931|0.752|0.832|5s (CUDA)|

We will only consider the models with a precision score of 0.90 and above.

The simple sequential neural network is overall the best model. However, there is the issue of it being entirely dependent on nVidia proprietary technology. It would not look for an AMD internal data team to be deploying such a model if word got out. However, if something similar can be implemented using AMD ROCm, the neural network may be the way forward.

In the meantime, despite having a slightly lower precision score, the model to be deployed is Naive Bayes with the Tfidf vectoriser. This is due to the fact that while random forest gets a better score, it also took 3 times as long to fit. In view of the absolute size (3 times Naive Bayes (*emphasis*)) of the total dataset which may need to be processed in the future, considerations about performance win out over the small difference in precision score.

# Sentiment Analysis Conclusions

### Headline Conclusions

1. The percentage of negative posts in r/nvidia is 10.9%.

2. The percentage of negative posts in r/amd is 15.2%.

3. This is a significant difference - For every n comments on r/amd, there are 38.9% more negative comments than for every n comments on r/nvidia.

4. There is likely a genuine issue with AMD products.

### Provisos

1. It is not possible to filter out price-related complaints on r/nVidia. These complaints have been quite common since the major price increase in the RTX xx80 GPUs of the Lovelace generation.

2. Posts relating to AMD CPUs (which have been extremely well received) have not been filtered out. 

3. Given the above, there is likely an even greater difference in technical complaints than 38.9%.

# Recommendations

### Modelling

1. Given that this model is going to be deplyed by AMD, we should use the model which is compatible with AMD's hardware. Therefore, we should use Naive Bayes with the tfidf vectoriser.

2. We are concerned with precision as this metric ensures that subsequent sentiment analysis includes as few non-AMD related posts as possible. This is because the use-case for the model is to pick out AMD-related posts from GPU discussion forums. A precision score of 0.92 from this models is adequate.

3. This model will need to be re-trained as a multi-classification model to take into Intel Arc GPUs into account once they achieve further market penetration.

### Sentiment Analysis

1. Engineering needs to be given more resources to apply towards development for greater driver stability.

2. A good start would be the development and implementation of a comprehensive testing suite before any new graphics driver release.

3. A major difference in AMD / Nvidia user software is the lack of settings available for AMD GPUs. Having more available parameters means users will likely be better able to tune their GPUs for their systems. See: nVidia Control Panel / nVidia Profile Inspector. AMD's GPU software looks modern, compared to nVidia's 90's chic control software, but nVidia's software works, and does not hide settings behind a ton of menus. AMD's software also lacks a the massive number of settings available to nVidia users.