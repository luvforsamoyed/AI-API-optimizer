import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json, datetime
from scipy.stats import norm


def value_modeling(sample_size = 1000, seed = 0, cycle = 50, amp = 3, abn_num = 15, sig = 2):

    np.random.seed(seed)
    x1 = np.linspace(0, sample_size - 1, sample_size)
    y1 = amp * np.sin(2*np.pi / cycle * x1) + norm.rvs(size = sample_size)
    abn_pt = np.random.choice(range(sample_size), abn_num, replace = None)
    for i in abn_pt:
        y1[i] += np.random.normal(y1[i], sig)
    
    return abn_pt, y1

def gen_time_idx(init_dt = datetime.datetime(2000, 1, 1), sample_size = 1000, dtype = 'datetime'):
        
    if (dtype != 'datetime') & (dtype != 'timestamp'):
        print("Wrong dtype argument. Failed to generate time index.")
        return
    
    dt = []
    
    if dtype == 'timestamp':
        for i in range(sample_size):
            #add every 1day to make next point. iterate 1000 times
            ith_dt = init_dt + i * datetime.timedelta(days=1)
            dt.append(datetime.datetime.timestamp(ith_dt))

        return dt
    
    elif dtype == 'datetime':
        for i in range(sample_size):
            #add every 1day to make next point. iterate 1000 times
            ith_dt = init_dt + i * datetime.timedelta(days=1)
            dt.append(ith_dt.isoformat())
        
        return dt
    
def vis(y, dt, y_true, y_score):

    dt = np.array(dt)        

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
    plt.scatter(x=dt[tp], y=y[tp], c='red', label='True Positive')
    plt.scatter(x=dt[fp], y=y[fp], c='blue', label='False Positive')
    plt.scatter(x=dt[fn], y=y[fn], c='green', label='False Negative')
    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.title("Time Series Detetion")