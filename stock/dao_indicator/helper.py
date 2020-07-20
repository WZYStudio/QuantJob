import abc
from stock.dao_indicator.indicator_types import IndicatorType


class KLineBlock(abc.ABC):

    def __init__(self):
        pass

    def __init__(self, type):
        self._type = type

    @abc.abstractmethod
    def set_index(self, date_str, index):
        """一定要写点注释么: 这里可以根据index和date_str，算出block的真正起始和终点时间"""
