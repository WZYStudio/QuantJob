import easyquotation


# 因为不是实时时间，所以我也看不到效果了, 块级行情可能不好拿
def get_stock_market():
    quotation = easyquotation.use('sina')
    result = quotation.real('600196')
    print("---to print data---")
    print(result)
    print("---print data end---")
    return


if __name__ == '__main__':
    get_stock_market()
