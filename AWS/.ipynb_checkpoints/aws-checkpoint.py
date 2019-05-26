import boto3
import botocore
import sagemaker
import sys
import pandas as pd
from sagemaker import RandomCutForest
from sagemaker.predictor import csv_serializer, json_deserializer
from sklearn.metrics import f1_score
import matplotlib.pyplot as plt
import numpy as np

class aws():

    def set_data(self, anomal_pt, value, time_series, sensitivity = None, **kwargs):
        
        self.abn_pt = anomal_pt
        self.y = value
        self.dt = time_series      
        self.df = pd.DataFrame({'datetime': self.dt, 'value': self.y})

    def inference(self, **kwargs):

        self.bucket = kwargs.get('bucket')
        self.prefix = kwargs.get('prefix')
        self.execution_role = kwargs.get('execution_role')
        self.instance_type = kwargs.get('instance_type')
        self.aws_access_key_id = kwargs.get('aws_access_key_id')
        self.aws_secret_access_key = kwargs.get('aws_secret_access_key')
        self.region_name = kwargs.get('region_name')
        
        
        print("//////boto3 session generating")
        boto_session = boto3.Session(
            aws_access_key_id = self.aws_access_key_id,
            aws_secret_access_key = self.aws_secret_access_key,
            region_name = self.region_name
        )

        # check if the bucket exists
        print("\n//////check if the bucket exists")    
        try:
            boto_session.client('s3').head_bucket(Bucket=self.bucket)
        except botocore.exceptions.ParamValidationError as e:
            print('Hey! You either forgot to specify your S3 bucket'
                  ' or you gave your bucket an invalid name!')
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == '403':
                print("Hey! You don't have permission to access the bucket, {}.".format(self.bucket))
            elif e.response['Error']['Code'] == '404':
                print("Hey! Your bucket, {}, doesn't exist!".format(self.bucket))
            else:
                raise
        else:
            print('Training input/output will be stored in: s3://{}/{}'.format(self.bucket, self.prefix))

        print("\n//////define sagemaker session")    
        sg_session = sagemaker.Session(boto_session)

        print("\n//////define rcf model")    
        # specify general training job information
        rcf = RandomCutForest(role=self.execution_role,
                              train_instance_count=1,
                              train_instance_type=self.instance_type,
                              data_location='s3://{}/{}/'.format(self.bucket, self.prefix),
                              output_path='s3://{}/{}/output'.format(self.bucket, self.prefix),
                              num_samples_per_tree=512,
                              num_trees=50,
                              sagemaker_session = sg_session)

        print("\n//////fitting rcf model")    
        # automatically upload the training data to S3 and run the training job
        rcf.fit(rcf.record_set(self.df.value.as_matrix().reshape(-1,1)))

        print("\n//////infer the virtual data")    
        rcf_inference = rcf.deploy(
            initial_instance_count=1,
            instance_type=self.instance_type,
        )

        print("\n//////serialize the output data")    
        rcf_inference.content_type = 'text/csv'
        rcf_inference.serializer = csv_serializer
        rcf_inference.accept = 'application/json'
        rcf_inference.deserializer = json_deserializer

        df_numpy = self.df.value.as_matrix().reshape(-1,1)
        self.results = rcf_inference.predict(df_numpy)
        


    def f1_metrics(self):

        scores = [datum['score'] for datum in self.results['scores']]

        # add scores to taxi data frame and print first few values
        self.df['score'] = pd.Series(scores, index=self.df.index)

        score_mean = self.df['score'].mean()
        score_std = self.df['score'].std()
        score_cutoff = score_mean + 3*score_std

        anomalies = self.df[self.df['score'] > score_cutoff]

        y_true = np.zeros(self.y.size)
        for i in self.abn_pt:
            y_true[i] = 1 
        self.y_true = y_true
        
        y_score = np.zeros(self.y.size)
        for i in anomalies.index:
            y_score[i] = 1
        self.y_score = y_score

        f1 = f1_score(y_true, y_score)
        return f1, y_true, y_score