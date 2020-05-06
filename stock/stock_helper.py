from stock.csv_loader import *
import datetime
from datetime import date


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
    get_each_tick_vol('000400', '2020-03-30', '2020-04-28')
