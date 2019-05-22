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
    
    return f1