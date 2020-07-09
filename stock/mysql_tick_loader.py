from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import stock.csv_loader as csv_loader
from stock.csv_loader import get_month_data_dir
import pandas as pd
import numpy as np
import os
from multiprocessing import Process, Queue

np.set_printoptions(suppress=True)

TICK_PREFIX = 'Tick_'


def get_db_url(db_name):
    return "mysql+pymysql://wzy:123@192.168.50.100/" + db_name + "?charset=utf8";


def get_db_name(date_str):
    return TICK_PREFIX + date_str


def make_db_by_datestr(date_str, engine=None):
    # 依照日期  创建并使用库
    db_name = get_db_name(date_str)
    url = get_db_url(db_name)

    if not engine:
        engine = create_engine(url, echo=True)

    if not database_exists(url):
        create_database(url)

    # 非常寸、带横杠的数据库名，要用反引号 引上才可以用， 否则sql报错
    use_db_dialect = 'USE ' + "`" + db_name + "`"
    engine.execute(use_db_dialect)

    return engine


def get_df_from_mysql(stock_index, date_str):
    engine = make_db_by_datestr(date_str)
    table_name = str(stock_index)
    sql_cmd = "SELECT * FROM " + "`" + table_name + "`"
    df = pd.read_sql(sql_cmd, engine)
    return df


def stock_csv_to_db(stock_index, date_str, stock_csv_path):
    engine = make_db_by_datestr(date_str)

    if stock_csv_path:
        df = csv_loader.get_df_from_csv(stock_csv_path)
    else:
        df = csv_loader.get_df(stock_index, date_str)
    table_name = str(stock_index)

    # 不得不说，就这样就挺好..
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    # 这个是用来检测数据的
    # df_tmp = new_df.head(20)
    # print(df_tmp.loc[:, ['Volume', 'SaleOrderVolume', 'BuyOrderVolume']])


def daily_csv_files_to_db(date_str, daily_tmp_dir):
    if os.path.isdir(daily_tmp_dir):
        files = os.listdir(daily_tmp_dir)
        for file in files:
            full_path = os.path.join(daily_tmp_dir, file)
            stock_index = file.partition('.')[0]
            stock_csv_to_db(stock_index, date_str, full_path)


def load_csv_to_db_per_month(month_str):
    # Step1 根据month 找到对应的文件夹 ,没有就退出

    dir_path = get_month_data_dir(month_str)
    if os.path.isdir(dir_path):
        # Step2 扫描文件夹里的 所有文件, 注意这是一级子目录下的文件
        files = os.listdir(dir_path)
        for file in files:
            load_csv_to_db_daily(dir_path, file)
            # if file.endswith('.7z'):
            #     date_str = file.partition('.')[0]
            #     # 绝对路径
            #     daily_zip_file = os.path.join(dir_path, file)
            #     # print('daily_file is:' + daily_zip_file)
            #     daily_tmp_dir = csv_loader.uncompress_daily_7z_to_tmp_dir(daily_zip_file)
            #     daily_csv_files_to_db(date_str, daily_tmp_dir)


# 其实month_str也可以从daily_str中提取出来， 这不是麻烦一点..就这样吧
def load_csv_to_db_daily(month_str, daily_7z_file_name):
    dir_path = get_month_data_dir(month_str)
    if daily_7z_file_name.endswith('.7z'):
        date_str = daily_7z_file_name.partition('.')[0]
        # 绝对路径
        daily_zip_file = os.path.join(dir_path, daily_7z_file_name)
        # print('daily_file is:' + daily_zip_file)
        daily_tmp_dir = csv_loader.uncompress_daily_7z_to_tmp_dir(daily_zip_file)
        daily_csv_files_to_db(date_str, daily_tmp_dir)


if __name__ == '__main__':
    # stock_csv_to_db('600196', '2020-07-08')
    # loop_csv_to_db_per_month('2020-07')
    process = Process(target=load_csv_to_db_per_month('2020-07'))

    process.start()
