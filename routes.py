
# routes file

from flask import Flask

app = Flask(__name__)


"""
TECH INDICATORS Example

from alpha_vantage.techindicators import TechIndicators
import matplotlib.pyplot as plt

ti = TechIndicators(key='YOUR_API_KEY', output_format='pandas')
data, meta_data = ti.get_bbands(symbol='MSFT', interval='60min', time_period=60)
data.plot()
plt.title('BBbands indicator for  MSFT stock (60 min)')
plt.show()

"""

#routes file
import ta
import pandas as pd

def generate_returns(df):

    TIME_WINDOW = 28
    OPEN_NAME = "Open"
    CLOSE_NAME = "Close"

    returns_columns = []

    for window in range(TIME_WINDOW):
        returns = df[CLOSE_NAME] - df[OPEN_NAME].shift(periods=window)
        returns_columns.append(returns)

    return returns_columns
