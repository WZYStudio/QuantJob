import os
import pandas as pd

os.environ['LA_LIBRARY_FILEPATH'] = '/usr/local/opt/libarchive/lib/libarchive.dylib'
import libarchive.public

BASE_DATA_DIR = '/Users/zylab/1_Develop/10_StockData'
TMP_DATA_DIR = BASE_DATA_DIR + '/TMP'


def get_month_by_date(date):
    if date and len(date) == 10:
        month = date[0:7]
        return month


def is_date_7z_exist(date_str):
    month = get_month_by_date(date_str)
    if month:
        support_path = BASE_DATA_DIR + '/' + month + '/' + date_str + ".7z"
        return os.path.exists(support_path)


def get_df(stock_index, date):
    stock_index = str(stock_index)
    if date and len(date) == 10:
        # 组合路径
        tmp_stock_path = TMP_DATA_DIR + '/' + date + '/' + stock_index + '.csv'
        if os.path.exists(tmp_stock_path):
            return get_df_from_csv(tmp_stock_path)

        if not os.path.exists(TMP_DATA_DIR):
            os.makedirs(TMP_DATA_DIR)

        # 组合路径,还没解压过
        month = date[0:7]
        month_dir = BASE_DATA_DIR + '/' + month
        date_file_name = date + '.7z'
        date_full_file = month_dir + '/' + date_file_name
        # 根据stock_index解压
        stock_file_path = uncompress7z(stock_index, date_full_file)
        return get_df_from_csv(stock_file_path)


def get_df_from_csv(csv_path):
    df = pd.read_csv(csv_path)
    # 股票数 改为 手数
    df.loc[:, ['Volume', 'SaleOrderVolume', 'BuyOrderVolume']] = df.loc[:, ['Volume', 'SaleOrderVolume', 'BuyOrderVolume']].div(100)
    return df


def output_file(file_name, entry):
    with open(TMP_DATA_DIR + '/' + file_name, 'wb') as f:
        for block in entry.get_blocks():
            f.write(block)


def uncompress7z(stock_index, date_7z_file):
    # print('uncompress7z')
    stock_item_file = stock_index + '.csv'
    compress_file_pure_name = date_7z_file.split('.')[0].split('/')[-1]

    os.chdir(TMP_DATA_DIR)
    for entry in libarchive.public.file_pour(date_7z_file):
        # print(entry)
        if entry.pathname and entry.pathname.rstrip('/') != compress_file_pure_name:
            pure_entry_name = entry.pathname.partition(compress_file_pure_name + '/')[2]
            # 解压
            if stock_item_file == pure_entry_name:
                # print('extract start')
                output_file(pure_entry_name, entry)
                # print('extract end')
                return pure_entry_name


if __name__ == '__main__':
    uncompress7z('000002', '/Users/zylab/2020-03-23.7z')
