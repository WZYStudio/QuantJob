from stock.feat_db.base_types import IndicatorType
from stock.feat_db.base_types import KLineBlock
import stock.feat_db.price_dao as price_dao
from enum import Enum, unique
import numpy
import talib
from pandas import DataFrame


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


def get_macd_result(close_price_list):
    result = _get_macd_by_ta_lib(close_price_list)
    # result = _get_macd_by_pd_ewm(close_price_list)
    return result


# 经过计算，虽然diff值与同花顺有一些不一致，但ta-lib的算法macd值相似度与同花顺相当高的，基本一样。完全可用，就先用ta-lib版本了。
# 注意的是 close_price_list， 个数要大于33， 因为33个之后，ta-lib才会产生macd值，至于为什么还不知道
def _get_macd_by_ta_lib(close_price_list):
    nd_close_price_list = numpy.array(close_price_list)
    macd_result = talib.MACD(nd_close_price_list, fastperiod=12, slowperiod=26, signalperiod=9)
    return macd_result


def _get_macd_by_pd_ewm(close_price_list):
    # data是包含高开低收成交量的标准dataframe short_,long_,m分别是macd的三个参数 返回值是包含原始数据和diff,dea,macd三个列的dataframe

    data = DataFrame(close_price_list, columns=['close'])
    short_period = 12
    long_period = 26
    m_period = 9

    data['diff'] = data['close'].ewm(adjust=False, alpha=2 / (short_period + 1), ignore_na=True).mean() - \
                   data['close'].ewm(adjust=False, alpha=2 / (long_period + 1), ignore_na=True).mean()
    data['dea'] = data['diff'].ewm(adjust=False, alpha=2 / (m_period + 1), ignore_na=True).mean()
    data['macd'] = 2 * (data['diff'] - data['dea'])
    return data['macd']


if __name__ == "__main__":
    close_price_list = price_dao.get_min15_close_price_list('002074', '2020-07-31', 16, 80)
    macd_result = get_macd_result(close_price_list)
    print('end')
