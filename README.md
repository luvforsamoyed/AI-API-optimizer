# Scoring Anomaly Detection in Various APIs


Introduction
-------------
There are many APIs that carry out various machine learning algorithms. However, each API has different format so it is hard to adapt same problem to different-shaped APIs. Furthermore, to compare each API's score, user must have to use whole possible APIs. It is both time-consuming and wasteful way. So, in this project, we will provide python module that automatically compares scores between various APIs respect to certain modeling method. Through this module, you can choose your best API only by doing simple, and intuitive experiment.

*in this initial version, we only offer function respect to ANOMALY DETECTION.


About Dataset
-------------

It's hard to find time series dataset that ensures uniform time interval, and this dataset will only be used to check whether how well each API scores in general anomaly detection, so we will use virtual time series using random sampling. 
This was written in random_sampling.ipynb in detail

The process is following:

1. Sampling 1000(default) sample values from gaussian distribution.(mu = 10, sigma = 2) This values will be align with continuous timestamp index(interval: 1day) in step 4.

2. Randomly choose 15(default) indexs where each value will be amplified
*Caution: These 15 points are candidates for anomaly points but not exactly are same as anomaly points.

3. Amplify each point by adding (each value - mu) * (coef - 1). By doing so, modified value = mu + coef * deviation
(origin value = mu + deviation)

4. Generate continuous timestamp(start from 2000.01.01, make 1000 timestamp with uniform 1 day interval). Then align with random sample values.

Through this process we will get uniform interval-time series dataset. We are ready for work with each API.

Score Metrics
-------------

(should be written)

Possible API
-------------

5 APIs and environment without external API will be tested:

1. Without API(using Luminol python library)

2. Random Cut Forest algorithm in Amazon Web Service SageMaker(AWS)

3. Azure Anomaly Detector

4. Google Cloud Inference API

5. Adobe Analytics - Anomaly Detection

Conclusion
----------

### Brief conclusion

Without API: successfully applied using Luminol library

AWS: successfully applied

Azure: successfully applied

GCP, Adobe Analytics: only offers alpha version.

Watson Discovery: cannot applied to this dataset.



### Graphical results

-Without API

![Alt text](https://github.com/luvforsamoyed/anomaly_detection/blob/master/rs_without_api.png?raw=true)



-AWS

![Alt text](https://github.com/luvforsamoyed/anomaly_detection/blob/master/rs_aws.png?raw=true)



-Azure

![Alt text](https://github.com/luvforsamoyed/anomaly_detection/blob/master/rs_azure.png?raw=true)













