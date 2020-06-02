import stock.stock_vol_helper as vol_helper
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def draw_sale_vol_info_multiday(stock_index, start_date, end_date, head_value=20):
    data_list = vol_helper.get_sale_vol_info_multi_day(stock_index, start_date, end_date, head_value)
    df = pd.DataFrame.from_records(data_list, index='date')
    plt.rcParams['figure.figsize'] = (19.2, 10.8)
    plt.rcParams['figure.dpi'] = 100
    df.plot.bar()
    plt.xticks(rotation=30)
    plt.show()
    # df.plot()
    # print(df)


def get_duplex_top_big_deal(stock_index, date, top_count):
    sale_df = vol_helper.get_duplex_top_deal_dataframe(stock_index, date, head_value=top_count, is_sale=True)
    sale_df['Action'] = 'sale'
    buy_df = vol_helper.get_duplex_top_deal_dataframe(stock_index, date, head_value=top_count, is_sale=False)
    buy_df['Action'] = 'buy'
    # append不会改变sale_df自己，除非手动赋值
    df_result = sale_df.append(buy_df)
    df_result.set_index(['Time'], inplace=True)
    df_result.sort_values(by='Time', inplace=True)

    print(df_result)

    # 基本的东西
    plt.rcParams['figure.figsize'] = (19.2, 10.8)
    plt.rcParams['figure.dpi'] = 100

    # 所以 ylim 是要自己算的，或取当天的最高值和最低值, 或取当天的 涨停值和跌停值
    # 股票软件是这么算的， 中线=昨天的收盘价，低线=今天的最低价，高线=中线+ （中线-低线）
    df_result.loc[:, 'Price'].plot(kind='line', marker='o', linestyle='dashed', ylim=[30, 37])
    # df_result.loc[:,'Volume'].plot.bar()
    # plt.ylim([30, 39]) 也可以直接这样调用

    plt.xticks(rotation=30)
    # plt.xlim('09:30:00', '15:00:00')
    plt.show()


if __name__ == '__main__':
    draw_sale_vol_info_multiday('600196', '2020-05-21', '2020-06-01')
    # get_duplex_top_big_deal('600196', '2020-05-19', 5)