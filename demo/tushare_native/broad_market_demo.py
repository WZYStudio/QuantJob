import tushare as ts

# 这个数据里有vol, ma5,ma10什么的，还是好用的
if __name__ == '__main__':
    ts.set_token('c88ef7fb2542e2f89e9c79c2d22ce2421511da6af7f905f60c7a29b4')
    days_deal = ts.get_hist_data('600584', start='2020-05-18', end='2020-05-21')
    print(days_deal)


