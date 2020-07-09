import datetime
import pandas as pd
import pandas_datareader.data as web


def yahoo_src():
    start = datetime.datetime(2020, 6, 30)  # 获取数据的时间段-起始时间
    end = datetime.date.today()  # 获取数据的时间段-结束时间
    stock = web.DataReader("600196.SS", "yahoo", start, end)  # 获取华泰证券2019年1月1日至今的股票数据
    print(stock.head(5))


def Alpha_Vantage_src():
    # https://www.alphavantage.co/documentation/   这个key很重要
    key = 'WHIST67XV2C5G0WL'

    requst_url = "https://www.alphavantage.co/query?function =TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=" + key;
    # 这个竟然可以, 注意深证是399001.sz ,可以测一下实时是否可以
    requst_url_600196 = "https://www.alphavantage.co/query?function =TIME_SERIES_INTRADAY&symbol=600196.SS&interval=5min&apikey=" + key;


if __name__ == '__main__':
    yahoo_src()
