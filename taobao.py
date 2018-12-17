# -*- coding: utf-8 -*-
import requests
import re
from getcookies import Getcookies
import codecs
import json
import time
#参考https://blog.csdn.net/weixin_39523034/article/details/80152833

#from fake_useragent import UserAgent
#proxies=json.load(open("proxies.json", 'r', encoding='utf-8'))
f=codecs.open('yingtao_url_new56.txt','a','utf-8')
cookies={}
try:
    cookiefile = open('cookies.json', 'r', encoding='utf-8')
except FileNotFoundError:
    Getcookies()
    cookiefile = open('cookies.json', 'r', encoding='utf-8')
for cookie in json.load(cookiefile)["cookies"]:
    cookies[cookie["name"]] = cookie["value"]
cookiefile.close()

headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:63.0) Gecko/20100101 Firefox/63.0'}
#User-Agent:Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1
for N in range(1,2):
    print(N)
    #翻页该url是有规律可循的，其主要变量在data-value、时间戳_ksTS、callback以及s
    #进行翻页模拟需要引入time
    ktsts = time.time()
    _ksTS = '%s_%s' % (int(ktsts * 1000), str(ktsts)[-3:])
    callback = "jsonp%s" % (int(str(ktsts)[-3:]) + 1)
    data_value = 44 * N
    s=44*(N-1)
    url='https://s.taobao.com/search?data-key=s&data-value={}&ajax=true&_ksTS={}&callback={}&initiative_id=tbindexz_20170306&ie=utf8&spm=a21bo.2017.201856-taobao-item.2&sourceId=tb.index&search_type=item&ssid=s5-e&commend=all&imgfile=&q=樱桃&suggest=history_1&_input_charset=utf-8&wq=&suggest_query=&source=suggest&bcoffset=-6&ntoffset=0&p4ppushleft=1,48&s={}'.format(data_value,_ksTS,callback,s)
    print(url)
    #使用requests爬取得到类似json文件，然后使用正则进行筛选，爬数据时最好先打印出来再进行筛选
    r = requests.get(url, cookies=cookies, headers=headers).text
    g_page_config = re.compile(r'[(](.*)[)]', re.S)
    gg = re.findall(g_page_config, r)[0]
    data = json.loads(gg)
    #获取信息列表
    page_item = data['mods']['itemlist']["data"]["auctions"]
    #查看店铺数目
    print(len(page_item))
    for i in range(0, len(page_item)):
        #提取店铺标题，发货地点，价格，付款人数，商品URL
        title = page_item[i]['raw_title']
        item_loc = page_item[i]['item_loc']
        view_price = page_item[i]['view_price']
        view_sales = page_item[i]['view_sales']
        detail_url = page_item[i]['detail_url']
        #print(detail_url)
        #写入到txt中，以后可以考虑写入到excel中
        f.write(str(title) + ',' + str(item_loc) + ',' + str(view_price) + ',' + str(view_sales) + ',' + detail_url + '\n')

'''
写入到excel的case:
import xlwt
#持久化
f = xlwt.Workbook(encoding='utf-8')
sheet01 = f.add_sheet(u'sheet1',cell_overwrite_ok=True)
#写标题
 
sheet01.write(0,0,'标题')
sheet01.write(0,2,'标价')
sheet01.write(0,3,'是否包邮')
sheet01.write(0,4,'是否天猫')
sheet01.write(0,5,'地名')
sheet01.write(0,6,'店名')
sheet01.write(0,7,'url')
 
for i in range(len(DATA)):
    sheet01.write(i+1,0,DATA[i]['title'])
    sheet01.write(i + 1, 1, DATA[i]['view_price'])
    sheet01.write(i + 1, 2, DATA[i]['view_sales'])
    sheet01.write(i + 1, 3, DATA[i]['view_fee'])
    sheet01.write(i + 1, 4, DATA[i]['isTmall'])
    sheet01.write(i + 1, 5, DATA[i]['area'])
    sheet01.write(i + 1, 6, DATA[i]['name'])
    sheet01.write(i + 1, 7, DATA[i]['detail_url'])
 
    f.save(u'搜索python的结果.xls')
'''