import time
import os
import configparser
from apscheduler.schedulers.background import BackgroundScheduler
from multiprocessing import Process
import stock.base_io.sina_quotation_net_loader as sina_loader
import stock.feat_db.price_dao as price_dao

cfg_parser = None


def get_favor_stock_list():
    global cfg_parser
    if cfg_parser is None:
        cfg_parser = configparser.ConfigParser(allow_no_value=True)

    cfg_parser.read('../favor_stock.cfg')
    stock_list = list(cfg_parser['FAVOR_STOCK'].keys())
    print(stock_list)
    return stock_list


# 第一次初始化单支股票的数据, 就是下载16x26个15min行情 到数据库
def init_market_data(stock_index: str):
    dict_data = sina_loader.get_sina_quotation_dict_list(stock_index, '15', '200')
    price_dao.input_price_dict_to_db(stock_index, dict_data)


def start_interval_loop_job(job_func, param):
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


def try_compute_macd():
    pass


if __name__ == "__main__":
    try_compute_macd()

    # get_favor_stock_list()
    init_market_data('002074')
    # init_market_data('300465')

    # job = init_market_data
    # start_interval_loop_job(job, '002074')
