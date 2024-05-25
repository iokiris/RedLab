
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



def get_data(start, end):

    DATA = pd.read_csv('data_main.csv')
    DATA['point'] = pd.to_datetime(DATA['point'])
    DATA.set_index('point', inplace = True)

    DATA['erore'] = DATA['erore'].fillna(0)
    DATA.drop('erore', inplace=True, axis=1)
    return DATA.copy().loc[start:end]

def load_model():

    model = tf.keras.models.load_model('resources/auto_model.keras')
    STscaler = load('resources/scaler.joblib')
    return model, STscaler

def feature_Engineering(data):

    data['delta_wr'] = data['WR'].pct_change() 
    data['delta_tg'] = data['tg'].pct_change() 
    data['delta_apdex'] = data['apdex'].pct_change() 
    data.fillna(0, inplace=True)

    return data

def anomaly(data, model, SC):

    limit = 4.717213602576221
    data_sc = SC.transform(data)

    data_delta = data_sc - model.predict(data_sc)
    data_sc =  pd.DataFrame(SC.inverse_transform(data_sc), columns=data.columns, index=data.index)
    data_delta =  pd.DataFrame(data_delta, index=data.index).abs().sum(axis=1)


    data_is_anomaly = pd.DataFrame(index=data.index)
    data_is_anomaly['Bool'] = data_delta.apply(lambda x: 1 if x>limit else 0)
    data_is_anomaly['ANOMALITY_CHANCE'] = 1 / (1 + np.exp(-data_delta/limit))


    json_result = data_is_anomaly.to_json(orient='records')
    return json_result

def anomaly_pipeline(start, end, limit=4.717213602576221):
    data = get_data(start, end)
    model, scaler = load_model()
    data = feature_Engineering(data)
    json_result = anomaly(data, model, scaler)
    return json_result


