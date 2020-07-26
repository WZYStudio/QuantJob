from stock.dao_indicator.base_types import *
import configparser

cfg_parser = None


def get_favor_stock_list():
    global cfg_parser
    if cfg_parser is None:
        cfg_parser = configparser.ConfigParser(allow_no_value=True)

    cfg_parser.read('./favor_stock.cfg')
    stock_list = list(cfg_parser['FAVOR_STOCK'].keys())
    print(stock_list)
    return stock_list


def process_disk_cache():
    pass


def loop_request_net_real_data():
    favor_stock_list = StockRecord.get_favor_stocks()
    pass


def request_net_history_data():
    favor_stock_list = StockRecord.get_favor_stocks()
    pass


if __name__ == "__main__":
    # request_net_history_data()
    # loop_request_net_real_data()
    get_favor_stock_list()
