from enum import Enum, unique

import abc
from sqlalchemy import Column, Integer, INTEGER, String, Date, DECIMAL, Boolean
from sqlalchemy.ext.declarative import declarative_base

TIME_DELTA_LIST = ["09:45:00", "10:00:00", "10:15:00", "10:30:00", "10:45:00", "11:00:00", "11:15:00", "11:30:00", "13:15:00", "13:30:00", "13:45:00",
                   "14:00:00", "14:15:00", "14:30:00", "14:45:00", "15:00:00"]

SqlAlchemy_Base_Model = declarative_base()


@unique
class IndicatorType(Enum):
    # 行情快
    PRICE_15_MIN = 0
    PRICE_30_MIN = 1
    PRICE_1_HOUR = 2
    PRICE_2_HOUR = 3
    PRICE_1_DAY = 4

    # MACD
    MACD_15_MIN = 5
    MACD_30_MIN = 6
    MACD_1_HOUR = 7
    MACD_2_HOUR = 8
    MACD_1_DAY = 9

    # BOLL
    BOLL_15_MIN = 10
    BOLL_30_MIN = 11
    BOLL_1_HOUR = 12
    BOLL_2_HOUR = 13
    BOLL_1_DAY = 14


class KLineBlock(abc.ABC):

    def __init__(self):
        pass

    def __init__(self, type):
        self._type = type
        self._stock_index = None

    @abc.abstractmethod
    def set_index(self, date_str, index):
        """一定要写点注释么: 这里可以根据index和date_str，算出block的真正起始和终点时间"""


class StockRecord(SqlAlchemy_Base_Model):
    __tablename__ = 'stock_quotation_progress'

    id = Column(Integer, primary_key=True)
    stock_index = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    min_15_seq_index = Column(Integer, nullable=False)
    is_favor = Column(Boolean, default=False)
