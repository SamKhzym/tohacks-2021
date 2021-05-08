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