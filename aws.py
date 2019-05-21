import boto3
import botocore
import sagemaker
import sys
import pandas as pd
from sagemaker import RandomCutForest
from sagemaker.predictor import csv_serializer, json_deserializer
from sklearn.metrics import f1_score

def inference(y, dt):

    df = pd.DataFrame({'datetime': dt, 'value': y})
    
    bucket = '[YOUR_BUCKET_NAME]'   
    prefix = '[YOUR_PREFIX]'
    execution_role = '[YOUR_EXECUTION_ROLE]''
    instance_type = '[YOUR_INSTANCE_TYPE]'

    print("//////boto3 session generating")
    boto_session = boto3.Session(
        aws_access_key_id="[YOUR_ACCESS_KEY_ID]",
        aws_secret_access_key="[YOUR_SECRET_ACCESS_KEY]",
        region_name= "[YOUR_REGION]"
    )
    
    # check if the bucket exists
    print("\n//////check if the bucket exists")    
    try:
        boto_session.client('s3').head_bucket(Bucket=bucket)
    except botocore.exceptions.ParamValidationError as e:
        print('Hey! You either forgot to specify your S3 bucket'
              ' or you gave your bucket an invalid name!')
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '403':
            print("Hey! You don't have permission to access the bucket, {}.".format(bucket))
        elif e.response['Error']['Code'] == '404':
            print("Hey! Your bucket, {}, doesn't exist!".format(bucket))
        else:
            raise
    else:
        print('Training input/output will be stored in: s3://{}/{}'.format(bucket, prefix))

    print("\n//////define sagemaker session")    
    sg_session = sagemaker.Session(boto_session)

    print("\n//////define rcf model")    
    # specify general training job information
    rcf = RandomCutForest(role=execution_role,
                          train_instance_count=1,
                          train_instance_type=instance_type,
                          data_location='s3://{}/{}/'.format(bucket, prefix),
                          output_path='s3://{}/{}/output'.format(bucket, prefix),
                          num_samples_per_tree=512,
                          num_trees=50,
                          sagemaker_session = sg_session)

    print("\n//////fitting rcf model")    
    # automatically upload the training data to S3 and run the training job
    rcf.fit(rcf.record_set(df.value.as_matrix().reshape(-1,1)))

    print("\n//////infer the virtual data")    
    rcf_inference = rcf.deploy(
        initial_instance_count=1,
        instance_type=instance_type,
    )

    print("\n//////serialize the output data")    
    rcf_inference.content_type = 'text/csv'
    rcf_inference.serializer = csv_serializer
    rcf_inference.accept = 'application/json'
    rcf_inference.deserializer = json_deserializer

    df_numpy = df.value.as_matrix().reshape(-1,1)
    results = rcf_inference.predict(df_numpy)
    
    return results


def f1_metrics(abn_pt, y, dt, results):
    
    df = pd.DataFrame({'datetime': dt, 'value': y})    

    scores = [datum['score'] for datum in results['scores']]

    # add scores to taxi data frame and print first few values
    df['score'] = pd.Series(scores, index=df.index)

    score_mean = df['score'].mean()
    score_std = df['score'].std()
    score_cutoff = score_mean + 3*score_std

    
    anomalies = df[df['score'] > score_cutoff]
    anomalies

    y_true = np.zeros(y.size)
    for i in abn_pt:
        y_true[i] = 1  

    y_score = np.zeros(y.size)
    for i in anomalies.index:
        y_score[i] = 1

    f1 = f1_score(y_true, y_score)
    return f1