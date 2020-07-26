import configparser
import stock.base_io.sina_quotation_net_loader as sina_loader
import stock.feat_db.price_dao as price_dao
from datetime import datetime
import stock.base_io.mysql_helper as mysql_helper

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


# 第一次初始化单支股票的数据, 就是下载16x26个15min行情 到数据库
def init_market_data(stock_index: str):
    data_dict = sina_loader.get_sina_quotation_dict_list(stock_index, '15', '20')

    for item in data_dict:
        time_str = item['day']
        time_obj = datetime.fromisoformat(time_str)
        item['date'] = date_str = str(time_obj.date())
        item['stock_index'] = stock_index

        table_cls = price_dao.get_price_table_cls(date_str)
        table_obj = table_cls()
        table_obj.fill_data_15min(**item)
        get_db_session().add(table_obj)

    price_dao.Quotation.create_all_tables(get_db_engine())
    get_db_session().commit()
    get_db_session().close()

    return


if __name__ == "__main__":
    # get_favor_stock_list()
    init_market_data('002074')
