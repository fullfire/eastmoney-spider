#!/usr/bin/env python
# coding=utf-8

# 获取所有股票的代码和名称

import urllib2
import re
import time
from bs4 import BeautifulSoup

import sys
reload(sys)  # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')

start = time.time()
# 爬取页面内容
response = urllib2.urlopen('http://quote.eastmoney.com/stocklist.html')
html = response.read(response)

# 原网页编码是GB18030
soup = BeautifulSoup(html, "html.parser", from_encoding="GB18030")

li_elements = soup.find_all("li")
# li元素里面的内容如下
# <li><a target="_blank" href="http://quote.eastmoney.com/sh500006.html">基金裕阳(500006)</a></li>
# ()中间有代码的项，()需要转义
pattern1 = ".*\(\d+\).*"
pattern2 = ".*>(.*)</a.*"   # 尝试匹配  基金裕阳(500006)
count = 0   # 股票支数
stocks = {}

for item in li_elements:
    item_string = str(item)

    if re.match(pattern1, item_string):
        m = re.match(pattern2, item_string)
        count += 1
        name_code = m.group(1)
        idx1 = name_code.index("(")
        idx2 = name_code.index(")")
        name = name_code[:idx1]
        code = name_code[idx1 + 1: idx2]
        stocks[name] = code

lines = list()
print("Start to sort items")
sorted_stocks = sorted(stocks.iteritems(), key=lambda d: int(d[1]), reverse=False)
for name, code in sorted_stocks:
    print(name + "->" + code)
    lines.append(name + "," + code+'\n')
print("Total stock num: {0}".format(count))


with open('data.csv', 'w') as f:
    f.writelines(lines)
print("Time: {0}".format(time.time() - start))