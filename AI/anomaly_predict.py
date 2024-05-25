
import pandas as pd
import numpy as np
import requests
import sklearn as skl

from tensorflow.keras.layers import Input, Dense, BatchNormalization, Activation, Dropout
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import regularizers
from tensorflow.keras.callbacks import EarlyStopping
import tensorflow as tf
from joblib import load

def get_data(WR, tg, apdex):
    df1 = pd.DataFrame(WR['data'], columns=['point', 'WR'])
    df2 = pd.DataFrame(tg['data'], columns=['point', 'tg'])
    df3 = pd.DataFrame(apdex['data'], columns=['point', 'apdex'])

    result = pd.merge(pd.merge(df1, df2, on='point', how='outer'), df3, on='point', how='outer')
    result['point'] = pd.to_datetime(result['point'])
    result.set_index('point', inplace=True)
    return result

def load_model():

    model = tf.keras.models.load_model('auto_model.keras')
    STscaler = load('scaler.joblib')
    return model, STscaler

def feature_Engineering(data):

    data['delta_wr'] = data['WR'].pct_change() 
    data['delta_tg'] = data['tg'].pct_change() 
    data['delta_apdex'] = data['apdex'].pct_change() 
    data.fillna(0, inplace=True)

    return data

def anomaly(data, model, SC, limit):

    limit = limit
    data_sc = SC.transform(data)

    data_delta = data_sc - model.predict(data_sc)
    data_sc =  pd.DataFrame(SC.inverse_transform(data_sc), columns=data.columns, index=data.index)
    data_delta =  pd.DataFrame(data_delta, index=data.index).abs().sum(axis=1)


    data_is_anomaly = pd.DataFrame(index=data.index)
    data_is_anomaly['Bool'] = data_delta.apply(lambda x: 1 if x>limit else 0)
    data_is_anomaly['ANOMALITY_CHANCE'] = 1 / (1 + np.exp(-data_delta/limit))


    json_result = data_is_anomaly.to_json(orient='records')
    return json_result

def anomaly_pipeline(WR, tg ,aprdex, limit=4.717213602576221):
    data = get_data(WR, tg, aprdex)
    model, scaler = load_model()
    data = feature_Engineering(data)
    json_result = anomaly(data, model, scaler, limit)
    return json_result



