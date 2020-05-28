import stock.stock_vol_helper as vol_helper
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def draw_sale_vol_info_multiday(stock_index, start_date, end_date, head_value=20):
    data_list = vol_helper.get_sale_vol_info_multi_day(stock_index, start_date, end_date, head_value)
    df = pd.DataFrame.from_records(data_list, index='date')
    df.plot.bar()
    plt.show()
    # df.plot()
    # print(df)


def get_duplex_top_big_deal(stock_index, date, top_count):
    pass

if __name__ == '__main__':
    draw_sale_vol_info_multiday('600196', '2020-05-19', '2020-05-28')
