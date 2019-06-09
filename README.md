# Cloud API 성능 비교 Report

### Index
* API 별 특징 - AWS vs Rest of all
* 성능 비교
	* Anomaly Detection (Time Series)
	* Regression (Tableau)
	* Classification (Tableau)

# API 별 특징 - AWS vs Rest of all
사실 API간의 비교는 AWS vs 나머지 API의 구도라고 볼 수 있다. GCP, Azure, Watson 같은 경우, 사용자가 데이터를 업로드하면, API는 자동으로 데이터를 분석하고, 인사이트를 도출해내는, 사용자 친화적인 GUI를 제공하고 있다. AWS같은 경우, 알고리즘, 파라미터, 인스턴스 등 결과 도출에 필요한 모든 설정을 사용자가 명령어들을 통해 제어해야 한다.

이는 AWS가 사용자에게 굉장한 선택의 폭을 제공한다는 것을 의미한다. 다시 말해 성능과 비용의 최적화를 지향한다. 동시에 입문 장벽이 굉장히 높다는 것이 큰 단점이다.

반대로 다른 API는 입문 장벽이 낮은 동시에, 빠른 시간 안에 결과를 도출할 수 있다는 장점이 있으며, 개인에게 최적화된 솔루션을 구축하기엔 다소 비효율적이라는 단점이 있다.
 
# Anomaly Detection 

### 비교 환경
* Luminol python library (non-ML)
* MS Azure - Anomaly Detector (non-ML)
* AWS Sagemaker - Random Cut Forest

### 데이터셋
데이터셋은 Yahoo! Webscope<sup id ='a1'>[1](#1)</sup>로부터 제공된 것이다.

데이터셋은 70여개의 실제 시계열 데이터와 300여개의 가상 데이터셋으로 4개의 섹션(A1, A2, A3, A4)으로 구분되어 있다.

|  |A1|A2|A3|A4|
|--|--|--|--|--|
|데이터셋 개수|64<sup id ='a2'>[2](#2)</sup>|100|100|100|
|time interval|1 hour|1 hour|1 hour|1 hour|
|실제/가상|실제|가상|가상|가상|
|Hand Labeling 여부|O|X|X|X|
|Seasonality, Noise Labeling|X|X|O|O|
|Trend, Change Point 여부|X|X|X|O|

### Performance Metrics
Average Precision (AP) score를 이용할 것이다.

![
](https://ifh.cc/g/3w8we.png)

P_n과 R_n는 n번째 threshold에서의 Precision과 Recall이다. 
0에 가까울수록 Anomaly Detection 능력이 떨어지고,
1에 가까울수록 탐지 능력이 우수하다.


### Results
각 Section과 전체 (364개) 데이터셋에 대한 평균 AP값을 비교했다.

|  |Luminol|Azure|AWS|
|--|--|--|--|
|A1|0.46|0.33|<center>-|
|A2|0.77|0.73|<center>-|
|A3|0.78|0.82|<center>-|
|A4|0.65|0.31|<center>-|
|**Average**|**0.79**|**0.69**|<center>**-**|



# Regression

### 비교 환경
* Keras/Tensorflow
* AWS Sagemaker - Linear Learner
* AWS Sagemaker - XGBoost
* GCP AutoML Tables 
### 데이터셋<sup id ='a3'>[3](#3)</sup>

#### 개요
 1년간(14.05 -15.05)의 King County 지역의 주택 매매 기록

#### Stats
18 Features (exclude Transaction ID, Date)  
17,290 Train Samples (80%)  
4,323 Test Samples (20%)  
Target Feature : House Price  


### Results
|  |Keras|AWS Linear Learner|AWS XGBoost|GCP|
|--|--|--|--|--|
|RMSE|159,439|232,880|153,974|121,138|
|MAE|81,958|129,768|73,890|67,357|
|R^2|0.87|0.69|0.86|0.91|
|MAPE|14.98%|25.34%|13.32%|12.44%|
# Classification

### 비교 환경
* Keras/Tensorflow
* AWS Sagemaker - Linear Learner
* AWS Sagemaker - XGBoost
* GCP AutoML Tables

### 데이터셋<sup id ='a4'>[4](#4)</sup>

#### 개요
4개월(2017.01.01 - 2017.04.30)간의 의료 예약 기록


#### Stats
18 Features    
48,971 Train Samples (80%)  
12,243 Test Samples (20%)  
Target Feature : (0: No Show, 1: Show)  


### Results
|  |Keras|AWS Linear Learner|AWS XGBoost|GCP|
|--|--|--|--|--|
|AUPRC|0.567|0.570|0.623|0.504|
|AUROC|0.829|0.828|0.856|0.795|
|Log Loss|0.504|0.503|0.490|0.532|
## Foot Note

<p id="1">
[1] https://yahooresearch.tumblr.com/post/114590420346/a-benchmark-dataset-for-time-series-anomaly</a> <a href = "#a1">↩</a></p>

<p id="2"> [2] Anomal Point가 없는 데이터셋 3개 제외 <a href = "#a2">↩</a></p>

<p id="3"> [3] https://www.kaggle.com/harlfoxem/housesalesprediction<a href = "#a3">↩</a></p>

<p id="4"> 
[4] https://www.kaggle.com/afflores/medical-appointment<a href = "#a4">↩</a></p>
