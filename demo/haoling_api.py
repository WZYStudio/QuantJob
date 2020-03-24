# -*- coding: utf-8 -*-
import time, hashlib, requests, json


# 解析输出的数据
def output(json_str):
    return json.dumps(json.loads(json_str), indent=4, ensure_ascii=False)


m_id = '10252'  # 你的ID   点击进入
token = '52804708f8077653ff91fb10308a8a67'  # 你的token 点击进入

# 时间要用北京时间（系统时间）
ndate = time.strftime("%Y%m%d%H%M", time.localtime())
m = hashlib.md5()
b = ndate.encode(encoding='utf-8')
m.update(b)
ndate = m.hexdigest()

m = hashlib.md5()
c = str(token + ndate).encode(encoding='utf-8')
m.update(c)
sign = m.hexdigest()

gcodes = 'sz002624'

param1 = {'actName': 'chengJiao', 'page': '1', 'm_id': m_id, 'sign': sign, 'gcodes': gcodes, 'date': '20200313'}
url = 'http://i.h0.cn/log.php'
req = requests.post(url, data=param1)
result = req.text
print(output(result))
