import jqdatasdk
from jqdatasdk import *

jqdatasdk.auth('18618405316', '405316')

# 单个股票的基本信息

my_stock_index = '002624.XSHE'
end_date = '2020-03-13'
stock_info = get_security_info(my_stock_index)

print(stock_info)

stock_price = get_price(my_stock_index, end_date=end_date, frequency='daily', skip_paused=True, count=30)

print(stock_price)

# d = get_ticks("000001.XSHE",start_dt=None, end_dt="2018-07-03", count=20)
# print(d)