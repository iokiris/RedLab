import pandas as pd
import numpy as np
import tensorflow as tf
from joblib import load
model = tf.keras.models.load_model('AI/resources/model.keras')
STscaler = load('AI/resources/StandartScaler.joblib')


def feature_Engineering(data):

    data['point'] = pd.to_datetime(data['point'])
    data.set_index('point', inplace=True)
    data['delta_wr'] = data['WR'].pct_change() 
    data['delta_tg'] = data['tg'].pct_change() 
    data['delta_apdex'] = data['apdex'].pct_change() 
    data.fillna(0, inplace=True)

    first_10_columns = data['WR'].head(10)
    window_size = 3  # Размер окна для скользящего среднего
    data['WR'] = data['WR'].rolling(window=window_size).mean()
    data['WR'][:10] = first_10_columns

    data['tg'] = data['tg'].diff().dropna().replace([np.inf, -np.inf], np.nan).dropna()

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
    result = list(zip(data_is_anomaly['Bool'].tolist(), data_is_anomaly['ANOMALITY_CHANCE'].tolist()))
    return result

def anomaly_pipeline(json, limit=3.4029455500570346):
    data = pd.DataFrame(json, columns=['point', 'WR', 'tg', 'apdex'])
    data = feature_Engineering(data)
    json_result = anomaly(data, model, STscaler, limit)
    return json_result
