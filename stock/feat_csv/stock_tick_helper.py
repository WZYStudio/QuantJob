from stock.base_io.csv_loader import *
import datetime
from datetime import date, timedelta


#  查看某个股票 在一段时期的 每笔均量
def get_each_tick_vol(stock_index, start_date, end_date):
    start = date.fromisoformat(start_date)
    end = date.fromisoformat(end_date)
    for i in range((end - start).days + 1):
        day = start + datetime.timedelta(days=i)
        day_str = str(day)
        if is_date_7z_exist(day_str):
            vol_each_payment = get_vol_each_payment(stock_index, day_str)
            print(day_str + ":" + str(vol_each_payment) + "  ")


# 查看某个股票 某天的成交量
def get_vol_each_payment(stock_index, date):
    df = get_df(stock_index, date)
    tick_count = len(df)
    vol_sum = df['Volume'].sum()
    single_tick_vol = (vol_sum / tick_count) / 100
    return single_tick_vol


def get_tick_close_price(stock_index, date):
    df = get_df(stock_index, date)
    last_row_index = df.shape[0] - 1
    close_price = df['Price'][last_row_index]
    print('close price:' + str(close_price))
    return close_price


def get_tick_high_low_open_close_price(stock_index, date, df=None):
    if df is None:
        df = get_df(stock_index, date)
    # 是pandas.core.series.Series类型, nlargest和nsmallest 都是Series 自带类型
    series = df['Price']
    high_price_series = series.nlargest(1)
    high_val = high_price_series.values[0]
    low_price_series = series.nsmallest(1)
    low_val = low_price_series.values[0]

    last_row_index = df.shape[0] - 1
    open_price = df['Price'].values[0]
    close_price = df['Price'].values[last_row_index]

    print('high low open close price:' + str(high_val) + "|" + str(low_val) + "|" + str(open_price) + "|" + str(
        close_price))
    return {'high': high_val, 'low': low_val, 'close': close_price, 'open': open_price}


# 得到当前天的 上一天,我自己写的没有周末的问题
def get_last_day_demo(today_date):
    date_obj = date.fromisoformat(today_date)
    yesterday = date_obj.today() + timedelta(days=-1)
    yesterday_str = str(yesterday)
    print('yesterday is:' + yesterday_str)
    return yesterday_str


def get_last_day(today_date):
    adate = date.fromisoformat(today_date)
    adate -= timedelta(days=1)
    while adate.weekday() > 4:  # Mon-Fri are 0-4
        adate -= timedelta(days=1)

    print('get_last_work_day:' + str(adate))
    return str(adate)


def run_demo():
    df = get_df_from_csv('/Users/zylab/haha2.csv')
    # 成交笔数
    tick_count = len(df)
    vol_sum = df['Volume'].sum()
    single_tick_vol = (vol_sum / tick_count) / 100
    print('single_tick_vol:' + str(single_tick_vol))


if __name__ == '__main__':
    # run_demo()
    # print(str(get_vol_each_payment('002624', '2020-03-24')))
    # get_each_tick_vol('600859', '2020-03-10', '2020-05-08')
    # get_tick_close_price('002074', '2020-06-02')
    # get_tick_high_low_open_close_price('002074', '2020-06-02')
    # 2020-06-08是周一
    print('last work day :' + get_last_day('2020-06-08'))
    # pass
