from stock.feat_db.base_types import IndicatorType, KLineBlock
from enum import Enum, unique
from sqlalchemy import Column, Integer, String, DECIMAL, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from stock.feat_db.base_types import TIME_DELTA_LIST

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
    vol = Column(Integer, nullable=False)

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
        self.vol = int(kwargs['volume'])

    @classmethod
    def create_all_tables(cls, db_engine):
        SqlAlchemy_Base_Model.metadata.create_all(db_engine)
        return


def get_price_table_cls(table_name):
    table_name = 'timeshare_' + table_name
    # 省着重新建类
    global price_table_cls_dict
    if table_name not in price_table_cls_dict:
        cls_name = table_name
        cls = type(cls_name, (Quotation,), {'__tablename__': table_name})
        price_table_cls_dict[table_name] = cls
    return price_table_cls_dict[table_name]
