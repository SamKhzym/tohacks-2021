
from flask import Flask
from alpha_vantage.timeseries import TimeSeries
import ta
import pandas as pd

app = Flask(__name__)

#Generates return columns from 1-28 days
def generate_returns(df):

    TIME_WINDOW = 28
    OPEN_NAME = "open"
    CLOSE_NAME = "adjusted_close"

    returns_columns = []

    for window in range(TIME_WINDOW):
        returns = (df[CLOSE_NAME] - df[OPEN_NAME].shift(periods=window))/df[OPEN_NAME].shift(periods=window)
        returns_columns.append(returns)

    return returns_columns

#Returns daily dataframe of specified stock ticker with all bukosabino/ta indicators
def get_stock_data(ticker):
    df = pd.read_csv("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol="+ticker+"&apikey=L6INA3MM73RWUHIO&datatype=csv&outputsize=full")
    df = df.iloc[::-1]

    df = ta.add_all_ta_features(df, open="open", high="high", low="low", close="adjusted_close", volume="volume")

    return df
