from enum import Enum, unique


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
