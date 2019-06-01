# API Comparison for Anomaly Detection in Time Series
Luminol(오픈 소스)를 포함한 총 3가지의 환경에서 time series에 대한 anomaly detection 성능비교를 진행할 것이다.

* Luminol python library
* Amazon Web Service SageMaker


* Microsoft Azure

# Library Architecture
성능 비교를 위해서 직접 import 할 모듈은 util_.py 하나이다. 전체적인 라이브러리 구조는 다음과 같다.

![
](https://ifh.cc/g/6LeDh.png)



# Dataset Description
데이터셋은 Yahoo! Webscope<sup>[1](#1)</sup>로부터 제공된 것이다.

데이터셋은 70여개의 실제 시계열 데이터와 300여개의 가상 데이터셋으로 4개의 섹션(A1, A2, A3, A4)으로 구분되어 있다.

|  |A1|A2|A3|A4|
|--|--|--|--|--|
|데이터셋 개수|64[^2]|100|100|100|
|time interval|1 hour|1 hour|1 hour|1 hour|
|실제/가상|실제|가상|가상|가상|
|Hand Labeling 여부|O|X|X|X|
|Seasonality, Noise Labeling|X|X|O|O|
|Trend, Change Point 여부|X|X|X|O|

<a name="1">Yahoo! Webscope dataset ydata-labeled-time-series-anomalies-v1_0 
[[https://yahooresearch.tumblr.com/post/114590420346/a-benchmark-dataset-for-time-series-anomaly](https://yahooresearch.tumblr.com/post/114590420346/a-benchmark-dataset-for-time-series-anomaly)]</a>


[^1]: Yahoo! Webscope dataset ydata-labeled-time-series-anomalies-v1_0 
[[https://yahooresearch.tumblr.com/post/114590420346/a-benchmark-dataset-for-time-series-anomaly](https://yahooresearch.tumblr.com/post/114590420346/a-benchmark-dataset-for-time-series-anomaly)]


[^2]: Anomal Point가 없는 데이터셋 3개 제외




# Performance Metrics
Average Precision (AP) score를 이용할 것이다.

 $$
\text{AP} = \sum_n (R_n - R_{n-1}) P_n
 $$
$P_n$과 $R_n$는 n번째 threshold에서의 Precision과 Recall이다. 
0에 가까울수록 Anomaly Detection 능력이 떨어지고,
1에 가까울수록 탐지 능력이 우수하다.


# Brief Conclusion
각 Section과 전체 (364개) 데이터셋에 대한 평균 AP값을 비교했다.

|  |Luminol|Azure|AWS|
|--|--|--|--|
|A1|0.46|0.33|<center>-|
|A2|0.77|0.73|<center>-|
|A3|0.78|0.82|<center>-|
|A4|0.65|0.31|<center>-|
|**Average**|**0.79**|**0.69**|<center>**-**|


