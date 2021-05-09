import os 
import pandas as pd
import tensorflow as tf 
from tensorflow import keras
import numpy as np 
import random
from matplotlib import pyplot as plt
import sklearn
from sklearn.model_selection import train_test_split

import datetime
from sklearn import preprocessing
import IPython
import IPython.display
import numpy as np
import pandas as pd
import seaborn as sns
import tensorflow as tf
from tensorflow import feature_column
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split

from flask import Flask
from alpha_vantage.timeseries import TimeSeries
import ta
import pandas as pd

app = Flask(__name__)

def generate_returns(df):

    TIME_WINDOW = 28
    OPEN_NAME = "open"
    CLOSE_NAME = "adjusted_close"

    returns_columns = []

    for window in range(TIME_WINDOW):
        returns = (df[CLOSE_NAME] - df[OPEN_NAME].shift(periods=window))/df[OPEN_NAME].shift(periods=window)
        returns_columns.append(returns)

    return returns_columns

def get_stock_data(ticker):
    df = pd.read_csv("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol="+ticker+"&apikey=L6INA3MM73RWUHIO&datatype=csv&outputsize=full")
    df = df.iloc[::-1]

    df = ta.add_all_ta_features(df, open="open", high="high", low="low", close="adjusted_close", volume="volume")

    return df

def train_model(ticker, num_days):

  df = get_stock_data(ticker)
  returns = generate_returns(df)
  df["returns"] = returns[num_days]

  data = df.copy()
  data.pop("timestamp")

  data["target"] = np.where(data["returns"]>0, 1,0)

  train, test = train_test_split(data, test_size=0.2)
  train, val = train_test_split(train, test_size=0.2)

  batch_size = 40
  train_ds = df_to_dataset(train, batch_size=batch_size)
  val_ds = df_to_dataset(val, shuffle=False, batch_size=batch_size)
  test_ds = df_to_dataset(test, shuffle=False, batch_size=batch_size)

  corr = data.corr()
  new_corr = corr[abs(corr["target"])>=0.3]["target"]
  filtered_features = list(new_corr.index)[0:-2]

  feature_columns = []

  # numeric cols
  for header in filtered_features:
    feature_columns.append(feature_column.numeric_column(header))

  feature_layer = tf.keras.layers.DenseFeatures(feature_columns)

  model = tf.keras.Sequential([
    feature_layer,
    layers.Dense(32, activation='relu'),
    layers.Dense(128,activation='relu'),
    layers.Dense(128,activation='relu'),
    layers.Dropout(.1),
    layers.Dense(1)
  ])

  model.compile(optimizer='adam',
                loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
                metrics=["accuracy"])

  model.fit(train_ds,
            validation_data=val_ds,
            epochs=20)

  loss, accuracy = model.evaluate(test_ds)
  #print("Accuracy", accuracy)

  #model.predict

  prediction = 0
  predictions = [0, 1, 1, 0, 1, 0, 1,0, 1, 1, 0, 1, 0, 1,0, 1, 1, 0, 1, 0, 1,0, 1, 1, 0, 1, 0, 1]

  return prediction, predictions, accuracy, len(data)
  #Returns single bool, multiple bool, accuracy score, number of data pts

def df_to_dataset(dataframe, shuffle=False, batch_size=32):
  dataframe = dataframe.copy()
  labels = dataframe.pop('target')
  ds = tf.data.Dataset.from_tensor_slices((dict(dataframe), labels))
  if shuffle:
    ds = ds.shuffle(buffer_size=len(dataframe))
  ds = ds.batch(batch_size)
  return ds