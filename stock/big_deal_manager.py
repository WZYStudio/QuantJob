import stock.stock_helper as stock_helper


def get_saleorder_descend_greater_than_100_shou(stock_index, date):
    df = stock_helper.get_df(stock_index, date)
    df.drop_duplicates(subset=['SaleOrderID'], inplace=True)
    df.sort_values(by='SaleOrderVolume', ascending=False, kind='quicksort', inplace=True)
    # 注意底下那个只是df的某个列去重了，df本身还是那么多项，所以是不行的！
    # df['SaleOrderID'].drop_duplicates(inplace=True)
    print('finish')


if __name__ == '__main__':
    get_saleorder_descend_greater_than_100_shou(600196, '2020-04-28')
