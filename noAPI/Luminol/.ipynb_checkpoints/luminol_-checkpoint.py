import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

from luminol.anomaly_detector import AnomalyDetector
from luminol.modules.time_series import TimeSeries
from sklearn.metrics import f1_score

class luminol():
    
    def set_data(self, anomal_pt, value, time_series, threshold = None, algorithm=None):
        self.abn_pt = anomal_pt
        self.y = value
        self.ts = time_series
        self.algorithm = algorithm
        self.threshold = threshold
        
    def f1_metrics(self):
        
        y = self.y
        ts = self.ts
        abn_pt = self.abn_pt
        threshold = self.threshold
        
        req_stamp = pd.Series(y, index = ts)
        detector = AnomalyDetector(req_stamp.to_dict(), score_threshold=threshold)
        anomalies = detector.get_anomalies()

        y_true = np.zeros(y.size)
        for i in abn_pt:
            y_true[i] = 1    
        self.y_true = y_true
        
        y_score = np.zeros(y.size)
        for i in anomalies:
            y_score[req_stamp.index.get_loc(i.exact_timestamp)] = 1
        self.y_score = y_score
        
        f1 = f1_score(y_true, y_score)

        return f1

    def vis(self):

        y_true = self.y_true
        y_score = self.y_score
        y = self.y
        ts = self.ts
        ts = np.array(ts)
        
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
        plt.scatter(x=ts[tp], y=y[tp], c='red', label='True Positive')
        plt.scatter(x=ts[fp], y=y[fp], c='blue', label='False Positive')
        plt.scatter(x=ts[fn], y=y[fn], c='green', label='False Negative')
        plt.legend()
        plt.xlabel('Time')
        plt.ylabel('Value')
        plt.title("Virtual Time Series")