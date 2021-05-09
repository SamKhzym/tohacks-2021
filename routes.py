from flask import Flask
from alpha_vantage.timeseries import TimeSeries
import ta
import pandas as pd
from stockprediction import train_model

app = Flask(__name__)
