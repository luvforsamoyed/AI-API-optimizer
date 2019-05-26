import pandas as pd
import numpy as np
import requests
import json
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score

class azure():
    
    def set_data(self, anomal_pt, value, time_series, sensitivity = None, algorithm=None, granularity='daily', **kwargs):
    
        self.abn_pt = anomal_pt
        self.y = value
        self.dt = time_series
        self.algorithm = algorithm 
        self.granularity = granularity
        self.batch_detection_url = kwargs.get('url')
        self.endpoint = kwargs.get('endpoint')
        self.subscription_key = kwargs.get('key')

    def send_request(self, endpoint, url, subscription_key, request_data):
        headers = {'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': subscription_key}
        response = requests.post(endpoint+url, data=json.dumps(request_data), headers=headers)
        return json.loads(response.content.decode("utf-8"))

    def detect_batch(self, request_data):
        
        result = self.send_request(self.endpoint, self.batch_detection_url, self.subscription_key, request_data)

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

    def f1_metrics(self):
        
        y = self.y
        dt = self.dt
        abn_pt = self.abn_pt        
        
        lists = []
        for i in range(y.size):
            lists.append({"timestamp": dt[i], "value": y[i]})
        df = {'granularity': self.granularity, 'series': lists}
        true_ = self.detect_batch(df)

        y_true = np.zeros(y.size)
        for i in abn_pt:
            y_true[i] = 1 
        self.y_true = y_true
        
        y_score = np.zeros(y.size)
        for i in true_:
            y_score[i] = 1
        self.y_score = y_score    

        f1 = f1_score(y_true, y_score)

        return f1, y_true, y_score