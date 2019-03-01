import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

def clean(df):
    df = df.drop(['surge_pct'], axis=1)
    df['signup_date'] = pd.to_datetime(df['signup_date'], infer_datetime_format=True)
    df['last_trip_date'] = pd.to_datetime(df['last_trip_date'], infer_datetime_format=True)
    date = pd.to_datetime('20140601', infer_datetime_format=True)
    df['churn'] = df['last_trip_date'] >= date
    return df

if __name__ == "__main__":
    df_train = pd.read_csv('data/churn_train.csv')
    df_test = pd.read_csv('data/churn_test.csv')
    df_train = clean(df_train)
    print(df_train)