import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json, datetime
from scipy.stats import norm

from AWS import aws
from noAPI.Luminol import luminol_
from Azure import azure

from sklearn.metrics import f1_score
from sklearn.metrics import precision_recall_curve

def value_modeling(sample_size = 1000, seed = 0, cycle = 50, amp = 3, abn_num = 15, sig = 2):

    np.random.seed(seed)
    x1 = np.linspace(0, sample_size - 1, sample_size)
    y1 = amp * np.sin(2*np.pi / cycle * x1) + norm.rvs(size = sample_size)
    abn_pt = np.random.choice(range(sample_size), abn_num, replace = None)
    for i in abn_pt:
        y1[i] += np.random.normal(y1[i], sig)
    
    return abn_pt, y1

def gen_time_idx(init_dt = datetime.datetime(2000, 1, 1), sample_size = 1000, dtype = 'datetime', interval = 'hours'):
        
    if (dtype != 'datetime') & (dtype != 'timestamp'):
        print("Wrong dtype argument. Failed to generate time index.")
        return
    
    dt = []
    
    if dtype == 'timestamp':
        for i in range(sample_size):
            #add every 1day to make next point. iterate 1000 times
            ith_dt = init_dt + i * datetime.timedelta(hours=1)
            dt.append(datetime.datetime.timestamp(ith_dt))

        return dt
    
    elif dtype == 'datetime':
        for i in range(sample_size):
            #add every 1day to make next point. iterate 1000 times
            ith_dt = init_dt + i * datetime.timedelta(hours=1)
            dt.append(ith_dt.isoformat())
        
        return dt
    
def vis(y, dt, y_true, y_score, type_):
    
    if (type_ != 'timestamp') and (type_ != 'datetime'):
        print('Wrong time index type.')
        return None
    
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
  
    pd.Series(y, index = dt).plot(figsize=(15,6))
    if type_ == 'timestamp':
        plt.scatter(x=dt[tp], y=y[tp], c='red', label='True Positive')
        plt.scatter(x=dt[fp], y=y[fp], c='blue', label='False Positive')
        plt.scatter(x=dt[fn], y=y[fn], c='green', label='False Negative')
    elif type_ == 'datetime':     
        plt.scatter(x=tp, y=y[tp], c='red', label='True Positive')
        plt.scatter(x=fp, y=y[fp], c='blue', label='False Positive')
        plt.scatter(x=fn, y=y[fn], c='green', label='False Negative')        
    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.title("Time Series Detetion for Best Epsilon")
    
def data_sel(branch='A1', num='1'):
    branch_ = branch + 'Benchmark'
    if branch == 'A1':
        num_ = 'real_' + num + '.csv'
    elif branch == 'A2':
        num_ = 'synthetic_' + num + '.csv'
    elif branch == 'A3':
        num_ = 'A3Benchmark-TS' + num + '.csv'
    elif branch == 'A4':
        num_ = 'A4Benchmark-TS' + num + '.csv'
    else:
        print('Wrong Branch name.')
        return None
    name = branch_ + "/" + num_ 
    return name

def inference_(api, branch, num, graph=False):
    ###data loading
    name = data_sel(branch, num)
    try:
        real_1 = pd.read_csv('dataset/' + name)
        real_1['value'] = real_1['value'].astype('float')
    except:
        return None
    
    sample_size_ = real_1.shape[0]
        
    #abn_pt
    if (branch == 'A1') or (branch == 'A2'): 
        abn_pt = real_1[real_1['is_anomaly'] == 1].index.values
    elif (branch == 'A3') or (branch == 'A4'): 
        abn_pt = real_1[real_1['anomaly'] == 1].index.values    
    #y
    y = real_1['value'].values
    y_true = np.zeros(y.size)
    for i in abn_pt:
        y_true[i] = 1
    
    if api == 'luminol':
        ts = gen_time_idx(dtype = 'timestamp', sample_size = sample_size_)
        lm = luminol_.luminol()
        lm.set_data(abn_pt, y, ts)

        ap, lm_true, lm_score = lm.f1_metrics()
#         print("AP score for %s is: %f" %(api, ap))
        if graph:
            vis(y, ts, lm_true, lm_score, type_ = 'timestamp')

    elif (api == 'aws') or (api == 'azure'):
        dt = gen_time_idx(dtype = 'datetime', sample_size = sample_size_)
        az = azure.azure()
        az.set_data(abn_pt, y, dt, 
                    url = "url", 
                    endpoint = "endpoint", 
                    key = "key",
                    granularity='hourly')

        ap, az_true, az_score = az.f1_metrics()  
#         print("AP score for %s is: %f" %(api, ap))
        if graph:
            vis(y, dt, az_true, az_score, type_ = 'datetime')
        
    return ap