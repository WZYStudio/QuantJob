import os
import pandas as pd
import shutil

os.environ['LA_LIBRARY_FILEPATH'] = '/usr/local/opt/libarchive/lib/libarchive.dylib'
import libarchive.public

BASE_DATA_DIR = '/Users/zylab/1_Develop/10_StockData'
TMP_DATA_DIR = BASE_DATA_DIR + '/TMP'


def get_month_data_dir(month_str):
    return BASE_DATA_DIR + "/" + month_str


def get_month_by_date(date):
    if date and len(date) == 10:
        month = date[0:7]
        return month


def is_date_7z_exist(date_str):
    month = get_month_by_date(date_str)
    if month:
        support_path = BASE_DATA_DIR + '/' + month + '/' + date_str + ".7z"
        return os.path.exists(support_path)


def make_sure_tmp_dir():
    if not os.path.exists(TMP_DATA_DIR):
        os.makedirs(TMP_DATA_DIR)


def re_create_tmp_dir():
    # 梯归的删除tmp文件夹和所有子文件夹
    shutil.rmtree(TMP_DATA_DIR)
    make_sure_tmp_dir()


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


def uncompress_daily_7z_to_tmp_dir(file_7z_path):
    compress_file_pure_name = file_7z_path.split('.')[0].split('/')[-1]
    tmp_daily_dir = TMP_DATA_DIR + "/" + compress_file_pure_name
    make_sure_tmp_dir()
    # 清空一下要占有的目录
    if os.path.isdir(tmp_daily_dir):
        shutil.rmtree(tmp_daily_dir)
    os.chdir(TMP_DATA_DIR)
    # 一定要循环一下能解压， 只调用libarchive.public.file_pour(file_7z_path) ,是不行的
    for entry in libarchive.public.file_pour(file_7z_path):
        print('entry.path name is:' + entry.pathname)
    print('tmp_daily_dir is:' + tmp_daily_dir)
    return tmp_daily_dir


if __name__ == '__main__':
    uncompress7z('000002', '/Users/zylab/1_Develop/10_StockData/2020-07/2020-07-08.7z')
    # uncompress_daily_7z_to_tmp_dir('/Users/zylab/1_Develop/10_StockData/2020-07/2020-07-08.7z')
