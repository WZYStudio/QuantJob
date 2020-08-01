from stock.feat_db.base_types import IndicatorType, KLineBlock
from enum import Enum, unique
from sqlalchemy import Column, Integer, String, DECIMAL, DateTime
from sqlalchemy.ext.declarative import declarative_base
from stock.feat_db.base_types import TIME_DELTA_LIST, get_db_session, get_db_engine
import stock.feat_db.price_dao as price_dao
from datetime import datetime
import math
import numpy
import talib
import pandas as pd
from pandas import DataFrame

price_table_cls_dict = {}


def get_sequence_by_time(time_str):
    strip_str = time_str.strip()
    seq_index = TIME_DELTA_LIST.index(strip_str) + 1
    return seq_index


@unique
class PriceType(Enum):
    MIN_15 = IndicatorType.PRICE_15_MIN
    MIN_30 = IndicatorType.PRICE_30_MIN
    HOUR_1 = IndicatorType.PRICE_1_HOUR
    HOUR_2 = IndicatorType.PRICE_2_HOUR
    DAY_1 = IndicatorType.PRICE_1_DAY


SqlAlchemy_Base_Model = declarative_base()


# 这里边错还挺多的，先搞别的
# class PriceBlock(KLineBlock, SqlAlchemy_Base_Model):
#
#     def __init__(self, my_type):
#         super(self, my_type)
#         self._start_price, self._end_price, self._vol, self._index, self._date_str = None
#         if self._type not in PriceType:
#             raise ValueError('invalid macd type: %d' % self._type)
#
#     def set_index(self, date_str, index):
#         self._index = index
#         self._date_str = date_str
#
#     @property
#     def val(self):
#         return (self._start_price, self._end_price, self._vol)
#
#     @property.setter
#     def val(self, start_price, end_price, vol):
#         self._start_price = start_price
#         self._end_price = end_price
#         self._vol = vol


def input_price_dict_to_db(stock_index: str, dict_data):
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

        table_cls = get_price_table_cls(date_str)
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


def get_min15_close_price_list(stock_index: str, end_date, end_table_seq_index, block_count):
    price_list = get_min15_price_list(stock_index, end_date, end_table_seq_index, block_count)

    close_price_list = []
    for item in price_list:
        demical_close = item.close  # Demical.demical类型
        float_close = float(demical_close)
        close_price_list.append(float_close)

    return close_price_list


def get_min15_price_list(stock_index: str, end_date, end_table_seq_index, block_count):
    stock_attr_name = stock_index + "_min_15"
    tables = get_db_engine().table_names()
    end_table = 'timeshare_' + end_date
    end_table_index = tables.index(end_table)

    # 像上取整
    diff_date_count = math.ceil((block_count - end_table_seq_index) / 16)
    begin_table_index = end_table_index - diff_date_count
    begin_table = tables[begin_table_index]

    full_diff_count = math.floor((block_count - end_table_seq_index) / 16)
    # 源于 (16-begin_index)+1+(diff_count*16)=count-index
    begin_table_seq_index = 17 + full_diff_count * 16 + end_table_seq_index - block_count

    data_list = []
    scan_table_list = tables[begin_table_index:end_table_index + 1]

    for i, table_name in enumerate(scan_table_list):
        table_cls = get_price_table_cls(table_name, True)
        if i == 0:
            tmp_result_list = get_db_session().query(table_cls).filter(table_cls.attr_name == stock_attr_name,
                                                                       table_cls.seq_index >= begin_table_seq_index) \
                .order_by(table_cls.seq_index).all()
        elif i == (len(scan_table_list) - 1):
            tmp_result_list = get_db_session().query(table_cls).filter(table_cls.attr_name == stock_attr_name,
                                                                       table_cls.seq_index <= end_table_seq_index) \
                .order_by(table_cls.seq_index).all()
        else:
            tmp_result_list = get_db_session().query(table_cls).filter(table_cls.attr_name == stock_attr_name) \
                .order_by(table_cls.seq_index).all()

        data_list.extend(tmp_result_list)

    return data_list


class Quotation(SqlAlchemy_Base_Model):
    __abstract__ = True  # 关键语句,定义所有数据库表对应的父类
    __table_args__ = {"extend_existing": True}  # 允许表已存在

    row_code = Column(String(25), primary_key=True)
    attr_name = Column(String(25), nullable=False)
    stock_index = Column(String(6), nullable=False)
    date_time = Column(DateTime, nullable=False)
    seq_index = Column(Integer, nullable=False)
    open = Column(DECIMAL(8, 2), nullable=False)
    close = Column(DECIMAL(8, 2), nullable=False)
    high = Column(DECIMAL(8, 2), nullable=False)
    low = Column(DECIMAL(8, 2), nullable=False)
    volume = Column(Integer, nullable=False)

    def fill_data_15min(self, **kwargs):
        time_str = kwargs['day']
        time_obj = datetime.fromisoformat(time_str)
        the_time = str(time_obj.time())

        self.stock_index = kwargs['stock_index']
        self.attr_name = self.stock_index + "_min_15"
        self.date_time = time_obj
        self.seq_index = get_sequence_by_time(the_time)
        self.row_code = self.attr_name + "_" + str(self.seq_index)
        self.open = float(kwargs['open'])
        self.close = float(kwargs['close'])
        self.high = float(kwargs['high'])
        self.low = float(kwargs['low'])
        self.volume = int(kwargs['volume'])

    @classmethod
    def create_all_tables(cls, db_engine):
        SqlAlchemy_Base_Model.metadata.create_all(db_engine)
        return


def get_price_table_cls(table_name, have_prefix=False):
    if not have_prefix:
        table_name = 'timeshare_' + table_name
    # 省着重新建类
    global price_table_cls_dict
    if table_name not in price_table_cls_dict:
        cls_name = table_name
        cls = type(cls_name, (Quotation,), {'__tablename__': table_name})
        price_table_cls_dict[table_name] = cls
    return price_table_cls_dict[table_name]


def my_macd(data, short_, long_, m):
    '''
    data是包含高开低收成交量的标准dataframe
    short_,long_,m分别是macd的三个参数
    返回值是包含原始数据和diff,dea,macd三个列的dataframe
    '''
    data['diff'] = data['close'].ewm(adjust=False, alpha=2 / (short_ + 1), ignore_na=True).mean() - \
                   data['close'].ewm(adjust=False, alpha=2 / (long_ + 1), ignore_na=True).mean()
    data['dea'] = data['diff'].ewm(adjust=False, alpha=2 / (m + 1), ignore_na=True).mean()
    data['macd'] = 2 * (data['diff'] - data['dea'])
    return data


if __name__ == "__main__":
    close_price_list = get_min15_close_price_list('002074', '2020-07-31', 16, 34)
    nd_close_price_list = numpy.array(close_price_list)
    df = DataFrame(close_price_list, columns=['close'])

    macd_result = talib.MACD(nd_close_price_list, fastperiod=12, slowperiod=26, signalperiod=9)

    macd_result2 = my_macd(df, 12, 26, 9)

    print('end')
