import pandas as pd
import numpy as np
import requests
import json
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score

batch_detection_url = "/anomalydetector/v1.0/timeseries/entire/detect"
latest_point_detection_url = "/anomalydetector/v1.0/timeseries/last/detect"

endpoint = "https://westus2.api.cognitive.microsoft.com/"
subscription_key = "039b14e520f64e5b9907af6ac58edff2"

def send_request(endpoint, url, subscription_key, request_data):
    headers = {'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': subscription_key}
    response = requests.post(endpoint+url, data=json.dumps(request_data), headers=headers)
    return json.loads(response.content.decode("utf-8"))

def detect_batch(request_data):
    result = send_request(endpoint, batch_detection_url, subscription_key, request_data)

    if result.get('code') != None:
        print("Detection failed. ErrorCode:{}, ErrorMessage:{}".format(result['code'], result['message']))
    else:
        # Find and display the positions of anomalies in the data set
        anomalies = result["isAnomaly"]
        true = []
        for x in range(len(anomalies)):
            if anomalies[x] == True:
                true.append(x)
                
    return true

def detect_latest(request_data):
    print("Determining if latest data point is an anomaly")
    # send the request, and print the JSON result
    result = send_request(endpoint, latest_point_detection_url, subscription_key, request_data)
    print(json.dumps(result, indent=4))
    

def f1_metrics(abn_pt, y, dt):
    lists = []
    for i in range(y.size):
        lists.append({"timestamp": dt[i], "value": y[i]})
    df = {'granularity': 'daily', 'series': lists}
    true_ = detect_batch(df)
    
    y_true = np.zeros(y.size)
    for i in abn_pt:
        y_true[i] = 1 
    
    y_score = np.zeros(y.size)
    for i in true_:
        y_score[i] = 1
        
    f1 = f1_score(y_true, y_score)
    
    return f1, y_true, y_score

def vis(y, ts, y_true, y_score):

    tp = []
    fp = []
    fn = []

    for i in range(y_true.size):
        if (y_true[i] == 1) & (y_score[i] == 1):
            tp.append(i)
        elif (y_true[i] == 1) & (y_score[i] == 0):
            fn.append(i)            
        elif (y_true[i] == 0) & (y_score[i] == 1):
            fp.append(i)    
    
    req_stamp = pd.Series(y, index = ts)
    req_stamp.plot(x=req_stamp.index, y=req_stamp.values, figsize=(12,6))
    plt.scatter(x=tp, y=y[tp], c='red', label='True Positive')
    plt.scatter(x=fp, y=y[fp], c='blue', label='False Positive')
    plt.scatter(x=fn, y=y[fn], c='green', label='False Negative')
    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.title("Virtual Time Series")