import requests, re, json

headers = {
    "Accept-Encoding": "gzip, deflate, sdch",
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/54.0.2840.100 "
        "Safari/537.36"
    ),
}

session = None


def get_sina_quotation_pure_txt(stock_code, scale, datalen):
    links = 'http://money.finance.sina.com.cn/quotes_service/api/jsonp_v2.php/var=/CN_MarketData.getKLineData?symbol=' + stock_code + '&scale=' + str(
        scale) + '&ma=no&datalen=' + str(datalen)

    global session
    global headers

    if session is None:
        session = requests.session()

    resp = session.get(links, headers=headers)

    return resp.text


def get_sina_quotation_dict_list(stock_code, scale, datalen):
    txt = get_sina_quotation_pure_txt(stock_code, scale, datalen)
    pattern = re.compile(r'\[.+\]')
    content = pattern.findall(txt)
    dict_list = None
    if content:
        print("sub txt is %s" % content[0])
        json_str = content[0]
        dict_list = json.loads(json_str)  # 形成了dict 列表
    return dict_list


if __name__ == "__main__":
    get_sina_quotation_dict_list('sh600196', '15', '20')
