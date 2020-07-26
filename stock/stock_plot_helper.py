import stock.stock_vol_helper as vol_helper
import stock.stock_helper as stock_helper
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from datetime import time as module_time
import matplotlib.ticker as ticker
from stock import mysql_tick_loader

# 基本的东西


print(matplotlib.matplotlib_fname())
# 查找字体缓存路径
print(matplotlib.get_cachedir())

plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 这两行需要手动设置
plt.rcParams['figure.figsize'] = (19.2, 10.8)
plt.rcParams['figure.dpi'] = 100


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


def draw_duplex_top_big_deal(stock_index, date, top_count):
    df = stock_helper.get_df(stock_index, date)
    # 注意mysql里的 成交量是手，不是股，不用再除100了
    # df = mysql_tick_loader.get_df_from_mysql(stock_index, date)

    sale_df = vol_helper.get_duplex_top_deal_dataframe(stock_index, date, head_value=top_count, is_sale=True, df=df)
    sale_df['Action'] = 'sale'
    buy_df = vol_helper.get_duplex_top_deal_dataframe(stock_index, date, head_value=top_count, is_sale=False, df=df)
    buy_df['Action'] = 'buy'
    # append不会改变sale_df自己，除非手动赋值
    df_result = sale_df.append(buy_df)
    df_result.set_index(['Time'], inplace=True)
    df_result.sort_values(by='Time', inplace=True)

    print(df_result)

    # 所以 ylim 是要自己算的，或取当天的最高值和最低值, 或取当天的 涨停值和跌停值
    # 股票软件是这么算的， 中线=昨天的收盘价，低线=今天的最低价，高线=中线+ （中线-低线） | 其实是 昨收 和 今天与最高价diff 或最低价diff中比较大的那个

    last_day = stock_helper.get_last_day(date)
    price_dict = stock_helper.get_tick_high_low_open_close_price(stock_index, date, df=df)
    last_price_dict = stock_helper.get_tick_high_low_open_close_price(stock_index, last_day)

    last_close_price = last_price_dict['close']
    today_high_price = price_dict['high']
    today_low_price = price_dict['low']

    today_diff1 = abs(today_high_price - last_close_price)
    today_diff2 = abs(today_low_price - last_close_price)

    diff = today_diff1 if today_diff1 > today_diff2 else today_diff2

    # 按Time排序后，time变成了index，所以dataframe.Time 还不行了，得用index了 ,index.values是ndarray，再转list
    nd_time_array = df_result.index.values
    time_array = nd_time_array.tolist()

    time_array_obj = []

    # time版
    # for i in time_array:
    #     datatime_str = i
    #     time_array_obj.append(module_time.fromisoformat(datatime_str))

    # datetime版 ,没感觉有区别
    for i in time_array:
        datatime_str = date + " " + i
        print('datetime str is:' + datatime_str)
        time_array_obj.append(datetime.fromisoformat(datatime_str))

    # time_array.insert(0, '09:25:00')
    # time_array.append('15:00:00')

    # --------执行画图-------

    fig, ax = plt.subplots()

    # 这三个起码我目前设了，没有任何用
    # plt.gca().xaxis.set_major_locator(mdates.HourLocator())
    # plt.gca().xaxis.set_major_locator(mdates.SecondLocator())
    plt.gca().xaxis.set_major_locator(mdates.MinuteLocator())

    # 也没啥用
    # hoursLoc = mdates.MinuteLocator(interval=6)  # 为6小时为1副刻度
    # ax.xaxis.set_minor_locator(hoursLoc)
    # ax.xaxis.set_minor_formatter(mdates.DateFormatter('%M'))

    # 要的就是这个！说的其实是我的采样点的间隔，比如隔2个显示一个，隔10个显示一个这样的. 但是如果设为1 ，文案会被互相遮挡
    tick_spacing = 1
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

    # 这个管用，这个比之前强， 但还不够好
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    xlim_start = datetime.fromisoformat(date + " 09:25:00")
    xlim_end = datetime.fromisoformat(date + " 15:00:00")

    # 乘1.1是为了给annotation留空间
    ylim_top = last_close_price + diff * 1.1
    ylim_bottom = last_close_price - diff * 1.1
    annotation_top = last_close_price + diff * 1.05
    annotation_bottom = last_close_price - diff * 0.5
    # df_result.loc[:, 'Price'].plot(kind='line', marker='o', linestyle='dashed', x=time_array_obj, ylim=[ylim_bottom, ylim_top])
    df_result.loc[:, 'Price'].plot(kind='line', marker='o', linestyle='dashed', ylim=[ylim_bottom, ylim_top])

    title = vol_helper.get_duplex_top_big_deal(stock_index, date, top_count)['desc_en']
    ax.set_title(title, fontsize=16)

    # 添加注解
    count_loop = 0
    for index, row in df_result.iterrows():
        y = row.Price
        vol = row.Volume
        type = row.Type
        big_order_type = 'S' if row.SaleOrderVolume > row.BuyOrderVolume else 'B'
        big_order_desc = 'sell' if row.SaleOrderVolume > row.BuyOrderVolume else 'buy'
        big_order_vol = row.SaleOrderVolume if row.SaleOrderVolume > row.BuyOrderVolume else row.BuyOrderVolume

        # active
        prefix_str = " :a"
        if type != big_order_type:
            # passive
            prefix_str = ":p"

        desc = str(big_order_vol) + prefix_str
        # print('annotation:' + desc)

        if big_order_type == 'B':
            plt.annotate(desc, xy=(count_loop, y), xytext=(count_loop, annotation_top), color='r',
                         arrowprops=dict(facecolor='black', headwidth=0.1, width=0.1, headlength=0.2),
                         fontsize=15,
                         verticalalignment='top', rotation=45)

        else:
            plt.annotate(desc, xy=(count_loop, y), xytext=(count_loop, annotation_bottom), color='g',
                         arrowprops=dict(facecolor='black', headwidth=0.1, width=0.1, headlength=0.2),
                         fontsize=15,
                         verticalalignment='top', rotation=45)

        count_loop += 1

    # xlim=[xlim_start, xlim_end])
    # df_result.loc[:,'Volume'].plot.bar()

    # ax.xaxis.set_major_locator(mdates.HourLocator())

    # 不用dataFrame.plot的方式画图
    # plt.plot(kind='line', marker='o', linestyle='dashed')
    # plt.xlim([xlim_start, xlim_end])

    # x轴的时间处理不好，这三个都不行
    # plt.xticks(time_array_obj, rotation=60)
    # plt.xticks(time_array_obj, rotation=60, freq='M')
    # plt.yticks(df_result['Price'].values)

    # 这个也不行，从AttributeError: 'datetime.time' object has no attribute 'toordinal' 这个来看，plt想要的是datetime.datetime，只用time这事是不行的,其实这事简单，加上年月日就可以了
    # m_dates = mdates.date2num(time_array_obj)
    # plt.plot_date(m_dates, df_result['Price'].values)
    # plt.ylim(last_close_price - diff, last_close_price + diff)

    # 解决标签重叠，这个要放在dataframe.loc的后边
    plt.gcf().autofmt_xdate()
    # plt.xticks(rotation=60)  # 设置x轴标签旋转角度

    plt.show()


if __name__ == '__main__':
    # draw_sale_vol_info_multiday('002459', '2020-07-01', '2020-07-10')
    draw_duplex_top_big_deal('002074', '2020-07-24', 20)
