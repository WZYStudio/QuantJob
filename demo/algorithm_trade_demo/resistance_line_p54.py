import pandas as pd
import statistics as stats
import math
from pandas_datareader import data


def load_yahoo_daily_df(stock_code=None, start_date=None, end_date=None):
    stock_code = '600196.ss'
    start_date = '2020-07-01'
    end_date = '2020-06-15'
    SRC_DATA_FILENAME = '600196_data.csv'

    try:
        goog_data2 = pd.read_csv(SRC_DATA_FILENAME)
    except FileNotFoundError:
        goog_data2 = data.DataReader(stock_code, 'yahoo', start_date, end_date)
        goog_data2.to_csv(SRC_DATA_FILENAME)
        print('goog_data2 occured')

    goog_data = goog_data2.tail(20)
    lows = goog_data['Low']
    highs = goog_data['High']
    closes = goog_data['Close']
    return goog_data


def get_sma_10():  # 求最近10个日期的 10日均线, 需要最近20日的值
    df = load_yahoo_daily_df()
    closes = df['Close']

    history = []
    sma_values = []

    for close_price in closes:
        history.append(close_price)
        if len(history) > 20:
            del (history[0])
        sma_values.append(stats.mean(history))


def get_boll():
    df = load_yahoo_daily_df()
    closes = df['Close']

    time_period = 20
    stdev_factor = 2

    history = []
    sma_values = []
    upper_band = []
    lower_band = []

    for close_price in closes:
        history.append(close_price)
        if len(history) > time_period:
            del (history[0])
        sma = stats.mean(history)
        sma_values.append(sma)

        variance = 0

        for hist_price in history:
            variance = variance + ((hist_price - sma) ** 2)  # ** 是平方
        stdev = math.sqrt(variance / len(history))  # use square root to get standard deviation

        upper_band.append(sma + stdev_factor * stdev)
        lower_band.append(sma - stdev_factor * stdev)

    return


if __name__ == "__main__":
    # load_yahoo_daily_df()
    get_sma_10()
