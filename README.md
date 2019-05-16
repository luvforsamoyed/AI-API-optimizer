# Scoring Anomaly Detection in Various APIs


Introduction
-------------
There are many APIs that carry out various machine learning algorithms. However, each API has different format so it is hard to adapt same problem to different-shaped APIs. Furthermore, to compare each API's score, user must have to use whole possible APIs. It is both time-consuming and wasteful way. So, in this project, we will provide python module that automatically compares scores between various APIs respect to certain modeling method. Through this module, you can choose your best API only by doing simple, and intuitive experiment.

*in this initial version, we only offer function respect to ANOMALY DETECTION.

The whole pipeline will be the following figure

![Alt text](https://github.com/luvforsamoyed/anomaly_detection/blob/master/pipeline.png?raw=true)



Random Sampling
-------------

It's hard to find time series dataset that ensures uniform time interval, and this dataset will only be used to check whether how well each API scores in general anomaly detection, so we will use virtual time series using random sampling. 
This was written in random_sampling.ipynb in detail

### The process is following:

1. Sampling 1000(default) sample values from gaussian distribution.(mu = 10, sigma = 2) This values will be align with continuous timestamp index(interval: 1day) in step 4.

2. Randomly choose 15(default) indexs where each value will be amplified
*Caution: These 15 points are candidates for anomaly points but not exactly are same as anomaly points.

3. Amplify each point by adding (each value - mu) * (coef - 1). By doing so, modified value = mu + coef * deviation
(origin value = mu + deviation)

4. Generate continuous timestamp(start from 2000.01.01, make 1000 timestamp with uniform 1 day interval). Then align with random sample values.

### Sample Dataset (seed = 1)

![Alt text](https://github.com/luvforsamoyed/anomaly_detection/blob/master/dataset.png?raw=true)

Through this process we will get uniform interval-time series dataset. We are ready for working with each API.

Environments for Inference
-------------

3 environments(including without API) will be tested:

1. Without API(using Luminol python library build by LinkedIn)

2. Random Cut Forest algorithm in Amazon Web Service SageMaker(AWS)

3. Azure Anomaly Detector


Inference
----------
## Without API(using Luminol python library build by LinkedIn)

## Random Cut Forest algorithm in Amazon Web Service SageMaker(AWS)

## Azure Anomaly Detector


Performance Metrics - Compare AUPRC
-------------
For scoring anomaly detection of each API, we will use AUPRC metrics. It stands for Area Under Precision Recall Curve.

(should be written)


### Graphical results

-Without API

![Alt text](https://github.com/luvforsamoyed/anomaly_detection/blob/master/rs_without_api.png?raw=true)



-AWS

![Alt text](https://github.com/luvforsamoyed/anomaly_detection/blob/master/rs_aws.png?raw=true)



-Azure

![Alt text](https://github.com/luvforsamoyed/anomaly_detection/blob/master/rs_azure.png?raw=true)


Conclusion
------------











