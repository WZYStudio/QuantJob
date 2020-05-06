import stock.stock_helper as stock_helper
import pandas as pd


def get_saleorder_descend_greater_than_100_shou(stock_index, date):
    df = stock_helper.get_df(stock_index, date)
    df.drop_duplicates(subset=['SaleOrderID'], inplace=True)
    df.sort_values(by='SaleOrderVolume', ascending=False, kind='quicksort', inplace=True)
    # 注意底下那个只是df的某个列去重了，df本身还是那么多项，所以是不行的！
    # df['SaleOrderID'].drop_duplicates(inplace=True)
    df_clip = df.head(10)

    # 底下这个，虽然确实可以除100，但是只剩三列，别的列都没有了..这个不行
    # df_clip = df_clip[['Volume', 'SaleOrderVolume', 'BuyOrderVolume']].div(100)

    # 这个虽然可以用，但写三遍太拖沓
    # df_clip['Volume'] = df_clip.Volume / 100

    # 这个好
    df_clip[['Volume', 'SaleOrderVolume', 'BuyOrderVolume']] = df_clip[
        ['Volume', 'SaleOrderVolume', 'BuyOrderVolume']].div(100)

    # 计算前10大卖单的总和

    # 这是设置DataFrame在console中的显示
    pd.set_option('precision', 0)
    pd.set_option("display.max_columns", 11)

    # print('finish:' + str(df_clip))
    print(df_clip)

    print('前10大卖单总和为:' + str(df_clip.SaleOrderVolume.sum()))


if __name__ == '__main__':
    get_saleorder_descend_greater_than_100_shou(600196, '2020-04-28')
