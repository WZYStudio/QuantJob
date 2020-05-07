import stock.stock_helper as stock_helper
import pandas as pd
import datetime
from datetime import date, time


# 时间是24小时制的,比如 9:35:01, 14:25:59  ，要精确到秒 ，注意要用time.fromisoformat的话，不能是9:35：01 ，要是09:35:01 ，差个0不行..
def get_order_descend_time_interval_single_day(stock_index, date, begin_time, end_time, is_sale=True):
    df = stock_helper.get_df(stock_index, date)
    KEY_ID = 'SaleOrderID' if (is_sale) else 'BuyOrderID'
    KEY_VOL = 'SaleOrderVolume' if (is_sale) else 'BuyOrderVolume'

    df.drop_duplicates(subset=[KEY_ID], keep='last', inplace=True)
    df.sort_values(by=KEY_VOL, ascending=False, kind='quicksort', inplace=True)
    df_copy = df.copy()
    df_copy.loc[:, ['Volume', 'SaleOrderVolume', 'BuyOrderVolume']] = df_copy.loc[:, ['Volume', 'SaleOrderVolume',
                                                                                      'BuyOrderVolume']].div(100)

    pass


def get_saleorder_info_greater_than_100shou(stock_index, date, is_sale=True):
    df = stock_helper.get_df(stock_index, date)
    KEY_ID = 'SaleOrderID' if (is_sale) else 'BuyOrderID'
    KEY_VOL = 'SaleOrderVolume' if (is_sale) else 'BuyOrderVolume'

    df.drop_duplicates(subset=[KEY_ID], keep='last', inplace=True)
    df.sort_values(by=KEY_VOL, ascending=False, kind='quicksort', inplace=True)
    df_copy = df.copy()
    df_copy.loc[:, ['Volume', 'SaleOrderVolume', 'BuyOrderVolume']] = df_copy.loc[:, ['Volume', 'SaleOrderVolume',
                                                                                      'BuyOrderVolume']].div(100)
    df_copy = df_copy[df_copy[KEY_VOL] >= 300]

    order_count = df_copy.size
    order_sum = df_copy[KEY_VOL].sum()

    print("300手以上的总" + ("卖" if is_sale else "买") + "单数为%d, 总手数为%d" % (order_count, order_sum))


def get_big_deal_descend_top10(stock_index, date, is_sale=True):
    df = stock_helper.get_df(stock_index, date)
    KEY_ID = 'SaleOrderID' if (is_sale) else 'BuyOrderID'
    KEY_VOL = 'SaleOrderVolume' if (is_sale) else 'BuyOrderVolume'

    df.drop_duplicates(subset=[KEY_ID], keep='last', inplace=True)

    df.sort_values(by=KEY_VOL, ascending=False, kind='quicksort', inplace=True)
    # 注意底下那个只是df的某个列去重了，df本身还是那么多项，所以是不行的！
    # df['SaleOrderID'].drop_duplicates(inplace=True)
    df_clip_origin = df.head(30)

    # 底下这个，虽然确实可以除100，但是只剩三列，别的列都没有了..这个不行
    # df_clip = df_clip[['Volume', 'SaleOrderVolume', 'BuyOrderVolume']].div(100)

    # 这个虽然可以用，但写三遍太拖沓
    # df_clip['Volume'] = df_clip.Volume / 100

    # 这个好
    # df_clip[['Volume', 'SaleOrderVolume', 'BuyOrderVolume']] = df_clip[
    #     ['Volume', 'SaleOrderVolume', 'BuyOrderVolume']].div(100)

    df_clip = df_clip_origin.copy()
    df_clip.loc[:, ['Volume', 'SaleOrderVolume', 'BuyOrderVolume']] = df_clip.loc[:, ['Volume', 'SaleOrderVolume',
                                                                                      'BuyOrderVolume']].div(100)

    # 计算前10大卖单的总和

    # 这是设置DataFrame在console中的显示
    pd.set_option('precision', 0)
    pd.set_option("display.max_columns", 11)

    # print('finish:' + str(df_clip))

    if is_sale:
        print('前10大卖单总和为:' + str(df_clip.SaleOrderVolume.sum()))
    else:
        print('前10大买单总和为:' + str(df_clip.BuyOrderVolume.sum()))

    print(df_clip)


def get_duplex_big_deal_descend_top10(stock_index, date):
    get_big_deal_descend_top10(stock_index, date)
    get_big_deal_descend_top10(stock_index, date, False)


def get_duplex_saleorder_info_greater_than_100shou(stock_index, date):
    get_saleorder_info_greater_than_100shou(stock_index, date)
    get_saleorder_info_greater_than_100shou(stock_index, date, False)


def get_sale_vol_info_multi_day(stock_index, start_date, end_date):
    start = date.fromisoformat(start_date)
    end = date.fromisoformat(end_date)
    for i in range((end - start).days + 1):
        day = start + datetime.timedelta(days=i)
        day_str = str(day)
        if stock_helper.is_date_7z_exist(day_str):
            print("\n---%s---" % day_str)
            get_duplex_big_deal_descend_top10(stock_index, day_str)
            get_duplex_saleorder_info_greater_than_100shou(stock_index, day_str)


if __name__ == '__main__':
    get_duplex_big_deal_descend_top10('603986', '2020-05-07')
    # get_duplex_saleorder_info_greater_than_100shou('603986', '2020-05-07')

    # get_sale_vol_info_multi_day('600196', '2020-04-13', '2020-05-06'
    #
    # my_time = time.fromisoformat('09:30:02')
    # my_time2 = time.fromisoformat('10:30:01')
    #
    #
    #
    # if my_time > my_time2:
    #     print('true')
    # else:
    #     print('false')
