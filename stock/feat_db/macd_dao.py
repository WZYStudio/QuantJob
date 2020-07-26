from stock.feat_db.indicator_types import IndicatorType
from stock.feat_db.helper import KLineBlock
from enum import Enum, unique


@unique
class MACDType(Enum):
    # MACD
    MIN_15 = IndicatorType.MACD_15_MIN
    MIN_30 = IndicatorType.MACD_30_MIN
    HOUR_1 = IndicatorType.MACD_1_HOUR
    HOUR_2 = IndicatorType.MACD_2_HOUR
    DAY_1 = IndicatorType.MACD_1_DAY


class MACDBlock(KLineBlock):

    def __init__(self, my_type):
        super(self, my_type)
        # 需要这样实始化么？
        self._val, self._index, self._date_str = None
        if self._type not in MACDType:
            raise ValueError('invalid macd type: %d' % self._type)

    def set_index(self, date_str, index):
        self._index = index
        self._date_str = date_str

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, diff, dea, macd):
        self._val = (diff, dea, macd)

    @staticmethod
    def get_blocks_list(my_type: MACDType, end_date, end_index, count=20):
        pass

    def get_macd_tuples_list(my_type: MACDType, end_date, end_index, count=20):
        pass

    @staticmethod
    def get_macd_diff_list(my_type: MACDType, end_date, end_index, count=20):
        pass

    @staticmethod
    def get_macd_dea_list(my_type: MACDType, end_date, end_index, count=20):
        pass

    @staticmethod
    def get_macd_val_list(my_type: MACDType, end_date, end_index, count=20):
        pass
