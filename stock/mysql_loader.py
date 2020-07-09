from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import stock.csv_loader as csv_file_loader
import pandas as pd
import numpy as np

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


def stock_csv_to_db(stock_index, date_str):
    engine = make_db_by_datestr(date_str)
    df = csv_file_loader.get_df(stock_index, date_str)
    df.loc[:, ['Volume', 'SaleOrderVolume', 'BuyOrderVolume']] = df.loc[:, ['Volume', 'SaleOrderVolume', 'BuyOrderVolume']].div(100)
    table_name = str(stock_index)

    # 不得不说，就这样就挺好..
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    # 这个是用来检测数据的
    # df_tmp = new_df.head(20)
    # print(df_tmp.loc[:, ['Volume', 'SaleOrderVolume', 'BuyOrderVolume']])


if __name__ == '__main__':
    stock_csv_to_db('600196', '2020-07-08')
    pass
