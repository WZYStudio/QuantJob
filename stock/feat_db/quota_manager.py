import configparser
import stock.base_io.sina_quotation_net_loader as sina_loader
import stock.feat_db.price_dao as price_dao
from datetime import datetime
import stock.base_io.mysql_helper as mysql_helper

from subprocess import call
from apscheduler.schedulers.background import BackgroundScheduler
import time
import os
from multiprocessing import Process, Queue

cfg_parser = None

STOCK_TIMESHARE_DB_NAME = 'StockTimeShare'


def get_favor_stock_list():
    global cfg_parser
    if cfg_parser is None:
        cfg_parser = configparser.ConfigParser(allow_no_value=True)

    cfg_parser.read('../favor_stock.cfg')
    stock_list = list(cfg_parser['FAVOR_STOCK'].keys())
    print(stock_list)
    return stock_list


def get_db_engine():
    return mysql_helper.get_db_engine_by_name(STOCK_TIMESHARE_DB_NAME)


def get_db_session():
    session = mysql_helper.get_db_session_by_name(STOCK_TIMESHARE_DB_NAME)
    return session


def input_dict_to_db(stock_index: str, dict_data):
    db_obj_list = []
    for item in dict_data:
        time_str = item['day']
        time_obj = datetime.fromisoformat(time_str)

        # 本周期未完全完结，但数据下载下来的这种，当然是不能插入
        if datetime.now().__le__(time_obj):
            print('MarketTime greater than now :' + str(time_obj) + " vs " + str(datetime.now()))
            continue

        item['date'] = date_str = str(time_obj.date())
        item['stock_index'] = stock_index

        table_cls = price_dao.get_price_table_cls(date_str)
        table_obj = table_cls()
        table_obj.fill_data_15min(**item)
        db_obj_list.append(table_obj)

        # get_db_session().add(table_obj)
        # session merge的强大作用 : 如果是新的数据就插入， 如果是已经存在的数据，就更新。这个事add并做不了
        # get_db_session().merge(table_obj)

    price_dao.Quotation.create_all_tables(get_db_engine())
    for item in db_obj_list:
        get_db_session().merge(item)
    try:
        get_db_session().commit()
    except Exception as err:
        print('DB_ERR:' + str(err))

    finally:
        get_db_session().close()


# 第一次初始化单支股票的数据, 就是下载16x26个15min行情 到数据库
def init_market_data(stock_index: str):
    dict_data = sina_loader.get_sina_quotation_dict_list(stock_index, '15', '20')
    input_dict_to_db(stock_index, dict_data)


def add_interval_loop_job(job_func, param):
    def run_background_scheduler():
        nonlocal job_func, param
        scheduler = BackgroundScheduler()
        # scheduler.add_job(mac_time, 'interval', minutes=15, start_date='2020-07-19 18:15:00', end_date='2020-07-19 21:00:00')
        scheduler.add_job(job_func, trigger='interval', minutes=2, args=[param])
        scheduler.start()

        print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
        try:
            # This is here to simulate application activity (which keeps the main thread alive).
            while True:
                time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            # Not strictly necessary if daemonic mode is enabled but should be done if possible
            scheduler.shutdown()

    process = Process(target=run_background_scheduler())
    process.start()


if __name__ == "__main__":
    # get_favor_stock_list()
    init_market_data('002074')
    # init_market_data('300465')

    # job = init_market_data
    # add_interval_loop_job(job, '002074')
