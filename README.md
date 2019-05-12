# anomaly_detection

#Introduction




#About Datset

It's hard to find time series dataset that ensures uniform time interval, and this dataset will only be used to check whether how well each API scores in general anomaly detection, so we will use virtual time series using random sampling. 
This was written in random_sampling.ipynb

The process is following:

1. Sampling 1000(default) sample values from gaussian distribution.(mu = 10, sigma = 2) This values will be align with continuous timestamp index(interval: 1day) in step 4.

2. Randomly choose 15(default) indexs where each value will be amplified
*Caution: These 15 points are candidates for anomaly points but not exactly are same as anomaly points.

3. Amplify each point by adding (each value - mu) * (coef - 1). By doing so, modified value = mu + coef * deviation
(origin value = mu + deviation)

4. Generate continuous timestamp(start from 2000.01.01, make 1000 timestamp with uniform 1 day interval). Then align with random sample values.

Through this process we will get uniform interval-time series dataset. We are ready for work with each API.

#Possible API






#Conclusion

-Brief conclusion

Without API: successfully applied using Luminol library

AWS: successfully applied

Azure: successfully applied

GCP, Adobe Analytics: only offers alpha version.

Watson Discovery: cannot applied to this dataset.













