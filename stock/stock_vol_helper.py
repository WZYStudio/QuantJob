import stock.stock_helper as stock_helper
import pandas as pd
import datetime
from datetime import date, time
import numpy as np
import math

np.set_printoptions(suppress=True)


# 时间是24小时制的,比如 9:35:01, 14:25:59  ，要精确到秒 ，注意要用time.fromisoformat的话，不能是9:35：01 ，要是09:35:01 ，差个0不行..这个用zfill函数
def get_order_descend_time_interval_single_day(stock_index, date, begin_time, end_time, is_sale=True):
    df = stock_helper.get_df(stock_index, date)
    KEY_ID = 'SaleOrderID' if (is_sale) else 'BuyOrderID'
    KEY_VOL = 'SaleOrderVolume' if (is_sale) else 'BuyOrderVolume'

    df.drop_duplicates(subset=[KEY_ID], keep='last', inplace=True)
    df.sort_values(by=KEY_VOL, ascending=False, kind='quicksort', inplace=True)
    df_copy = df.copy()
    pass


def get_saleorder_info_greater_than_100shou(stock_index, date, is_sale=True):
    df = stock_helper.get_df(stock_index, date)
    KEY_ID = 'SaleOrderID' if (is_sale) else 'BuyOrderID'
    KEY_VOL = 'SaleOrderVolume' if (is_sale) else 'BuyOrderVolume'

    df.drop_duplicates(subset=[KEY_ID], keep='last', inplace=True)
    df.sort_values(by=KEY_VOL, ascending=False, kind='quicksort', inplace=True)
    df_copy = df.copy()
    df_copy = df_copy[df_copy[KEY_VOL] >= 100]

    order_count = df_copy.size
    order_sum = df_copy[KEY_VOL].sum()

    print("300手以上的总" + ("卖" if is_sale else "买") + "单数为%d, 总手数为%d" % (order_count, order_sum))


def get_top_big_deal_descend(stock_index, date, head_value=10, is_sale=True, time_sort=True, is_brief=False):
    # 计算前10大卖单的总和

    df = get_duplex_top_deal_dataframe(stock_index, date, head_value, is_sale, time_sort, is_brief)
    # 这是设置DataFrame在console中的显示
    pd.set_option('precision', 0)
    pd.set_option("display.max_columns", 11)

    # print('finish:' + str(df_clip))
    sum_value = df.SaleOrderVolume.sum() if is_sale else df.BuyOrderVolume.sum()

    print('前' + str(head_value) + '大' + ('卖单' if is_sale else '买单') + "总和为:" + str(sum_value))

    # if is_sale:
    #     print('前10大卖单总和为:' + str(sum_value))
    # else:
    #     print('前10大买单总和为:' + str(sum_value))

    if not is_brief:
        print(df)

    return sum_value


def get_duplex_top_deal_dataframe(stock_index, date, head_value=10, is_sale=True, is_time_sort=True, is_brief=False,
                                  df=None):
    if df is None:
        df = stock_helper.get_df(stock_index, date)
    KEY_ID = 'SaleOrderID' if is_sale else 'BuyOrderID'
    KEY_VOL = 'SaleOrderVolume' if is_sale else 'BuyOrderVolume'

    df.drop_duplicates(subset=[KEY_ID], keep='last', inplace=True)

    df.sort_values(by=KEY_VOL, ascending=False, kind='quicksort', inplace=True)
    # 注意底下那个只是df的某个列去重了，df本身还是那么多项，所以是不行的！
    # df['SaleOrderID'].drop_duplicates(inplace=True)
    df_clip_origin = df.copy().head(head_value)

    # 底下这个，虽然确实可以除100，但是只剩三列，别的列都没有了..这个不行
    # df_clip = df_clip[['Volume', 'SaleOrderVolume', 'BuyOrderVolume']].div(100)

    # 这个虽然可以用，但写三遍太拖沓
    # df_clip['Volume'] = df_clip.Volume / 100

    # 这个好
    # df_clip[['Volume', 'SaleOrderVolume', 'BuyOrderVolume']] = df_clip[
    #     ['Volume', 'SaleOrderVolume', 'BuyOrderVolume']].div(100)

    df_clip = df_clip_origin.copy()
    # df_clip.loc[:, ['Time']] = df_clip.loc[:, ['Time']].zfill(8)

    # 时间加0这个就处理好了
    df_clip['Time'] = df['Time'].apply(lambda x: x.zfill(8))
    if is_time_sort:
        df_clip.sort_values(by='Time', ascending=True, kind='quicksort', inplace=True)
    return df_clip


def get_duplex_top_big_deal(stock_index, date, head_value=10, is_time_sort=True, is_brief=False):
    sale_sum = get_top_big_deal_descend(stock_index, date, head_value, is_sale=True, time_sort=is_time_sort,
                                        is_brief=is_brief)
    buy_sum = get_top_big_deal_descend(stock_index, date, head_value, is_sale=False, time_sort=is_time_sort,
                                       is_brief=is_brief)

    diff = buy_sum - sale_sum

    # diff 占有较少deal_sum的比例
    percentage = abs(diff) / (buy_sum if buy_sum > sale_sum else sale_sum)
    percentage_round = round(percentage, 3)

    desc = date + (' 流入:' if diff > 0 else " 流出:") + str(abs(diff)) + ',占小成交方向比例为:' + str(percentage_round)
    desc_en = date + '  ' + str(stock_index) + '   inflow:' + str(math.floor(buy_sum)) + '  outflow:' + str(
        math.floor(sale_sum)) + (
                  '  net inflow:' if diff > 0 else '  net outflow:') + str(
        math.floor(abs(diff))) + '  Proportion of small deal:' + str(
        percentage_round)
    print(desc)

    return {'date': date, 'stock': stock_index, 'buy_sum': buy_sum, 'sale_sum': sale_sum, 'diff': diff, 'desc': desc,
            'desc_en': desc_en}


def get_duplex_saleorder_info_greater_than_100shou(stock_index, date):
    get_saleorder_info_greater_than_100shou(stock_index, date)
    get_saleorder_info_greater_than_100shou(stock_index, date, False)


def get_sale_vol_info_multi_day(stock_index, start_date, end_date, head_value=20):
    start = date.fromisoformat(start_date)
    end = date.fromisoformat(end_date)
    deal_list = []
    for i in range((end - start).days + 1):
        day = start + datetime.timedelta(days=i)
        day_str = str(day)
        if stock_helper.is_date_7z_exist(day_str):
            print("\n---%s---" % day_str)
            data = get_duplex_top_big_deal(stock_index, day_str, head_value, is_brief=True)
            deal_list.append(data)
            # get_duplex_saleorder_info_greater_than_100shou(stock_index, day_str)
    return deal_list


if __name__ == '__main__':
    get_duplex_top_big_deal('002074', '2020-07-02', head_value=15, is_time_sort=True, is_brief=False)
    # get_duplex_saleorder_info_greater_than_100shou('300463', '2020-05-20')
    # get_sale_vol_info_multi_day('300242', '2020-03-10', '2020-04-29', 20)
