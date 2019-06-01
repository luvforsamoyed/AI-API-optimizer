import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

from luminol.anomaly_detector import AnomalyDetector
from luminol.modules.time_series import TimeSeries
from sklearn.metrics import f1_score
from sklearn.metrics import average_precision_score

class luminol():
    
    def set_data(self, anomal_pt, value, time_series, percentile = None, algorithm=None):
        self.abn_pt = anomal_pt
        self.y = value
        self.ts = time_series
        self.algorithm = algorithm
        self.percentile = percentile
        
    def f1_metrics(self):
        
        y = self.y
        ts = self.ts
        abn_pt = self.abn_pt
        req_stamp = pd.Series(y, index = ts)
        detector = AnomalyDetector(req_stamp.to_dict())
        scores = detector.get_all_scores()
        
        y_true = np.zeros(y.size)
        for i in abn_pt:
            y_true[i] = 1    
        self.y_true = y_true
        
        np_score = []
        for i in scores.iteritems():
            np_score.append(i[1])
        req_ = pd.Series(data = np_score)        
        
        ap = average_precision_score(y_true, np_score)        
        
        range_ = np.log10(np.arange(0, 9, .1) + 1)
        
        f1 = []
        for i in range_:
            threshold = np.quantile(np_score, i)
            anomalies = req_[req_.values > threshold].index.values

            y_score = np.zeros(y.size)
            for i in anomalies:
                y_score[i] = 1
            f1.append(f1_score(y_true, y_score))        
        
        threshold = np.quantile(np_score, range_[np.argmax(f1)])
        anomalies = req_[req_.values > threshold].index.values
        y_score = np.zeros(y.size)
        for i in anomalies:
            y_score[i] = 1

        return ap, y_true, y_score