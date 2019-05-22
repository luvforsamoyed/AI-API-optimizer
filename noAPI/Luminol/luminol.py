import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

from luminol.anomaly_detector import AnomalyDetector
from luminol.modules.time_series import TimeSeries
from sklearn.metrics import f1_score

def f1_metrics(abn_pt, y, dt, threshold=None, algorithm=None):
    
    req_stamp = pd.Series(y, index = dt)
    detector = AnomalyDetector(req_stamp.to_dict(), score_threshold=threshold)
    anomalies = detector.get_anomalies()
    
    y_true = np.zeros(y.size)
    for i in abn_pt:
        y_true[i] = 1    

    y_score = np.zeros(y.size)
    for i in anomalies:
        y_score[req_stamp.index.get_loc(i.exact_timestamp)] = 1
        
    f1 = f1_score(y_true, y_score)
    
    return f1, y_true, y_score

def vis(y, dt, y_true, y_score):

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
    
    req_stamp = pd.Series(y, index = dt)
    req_stamp.plot(x=req_stamp.index, y=req_stamp.values, figsize=(12,6))
    plt.scatter(x=tp, y=y[tp], c='red', label='True Positive')
    plt.scatter(x=fp, y=y[fp], c='blue', label='False Positive')
    plt.scatter(x=fn, y=y[fn], c='green', label='False Negative')
    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.title("Virtual Time Series")