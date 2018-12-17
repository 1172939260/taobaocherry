#爬取url
import requests
#使用正则表达式
import re
#调用getcookies.py中Getcookies方法
from getcookies import Getcookies
#lxml是python的一个解析库，支持HTML和XML的解析，支持XPath解析方式
from lxml import etree
#使用json格式
import json
#codecs专门用作编码转换
import codecs
#from fake_useragent import UserAgent
#f=open('yingtao_url_new_all.txt','a')
#读取cookies.json文件
cookies={}
try:
    cookiefile = open('cookies.json', 'r', encoding='utf-8')
except FileNotFoundError:
    Getcookies()
    cookiefile = open('cookies.json', 'r', encoding='utf-8')
for cookie in json.load(cookiefile)["cookies"]:
    cookies[cookie["name"]] = cookie["value"]
cookiefile.close()
#可以指定一个编码打开文件，使用这个方法打开的文件读取返回的将是unicode。写入时，如果参数是unicode，
#则使用open()时指定的编码进行编码后写入；如果是str，则先根据源代码文件声明的字符编码，解码成unicode后再进行前述 操作。相对内置的open()来说，这个方法比较不容易在编码上出现问题。
f3=codecs.open('no get url.txt','a','utf-8')#存取get 信息失败的url

def get_tm_detail(url):
    r = requests.get(url, cookies=cookies, headers=headers)
    #编码格式
    r.encoding = 'gb2312'
    doc_tree = etree.HTML(r.text)
    #保质期等
    detail = doc_tree.xpath('.//*[@id="J_AttrUL"]/li/text()')
    #print(detail)
    try:
        #根据xpath爬虫
        tmmailname = doc_tree.xpath('.//*[@class="slogo"]/a/strong/text()')[0]
    except IndexError:
        #查找失败的时候，赋值为空，并存入no get url.txt中
        tmmailname='none'
        f3.write(str(url)+'\n')
    try:
        tmmiaoshu = doc_tree.xpath('.//*[@class="main-info"]/div[1]/div[2]/span/text()')[0]
    except IndexError:
        tmmiaoshu='none'
    try:
        tmfuwu = doc_tree.xpath('.//*[@class="main-info"]/div[2]/div[2]/span/text()')[0]
    except IndexError:
        tmfuwu='none'
    try:
        tmwuliu = doc_tree.xpath('.//*[@class="main-info"]/div[3]/div[2]/span/text()')[0]
    except:
        tmwuliu='none'
    return detail,tmmailname,tmmiaoshu,tmfuwu,tmwuliu

def get_tb_detail(url):
    r = requests.get(url, cookies=cookies, headers=headers)
    r.encoding = 'gb2312'
    #print(r.text)
    doc_tree = etree.HTML(r.text)
    detail = doc_tree.xpath('.//*[@class="attributes-list"]/li/text()')
    try:
       tbmailname = doc_tree.xpath('.//*[@class="tb-shop-name"]/dl/dd/strong/a/@title')[0]
    except IndexError:
        tbmailname='none'
        f3.write(str(url)+'\n')
    try:
        xinyu_url = doc_tree.xpath('.//*[@class="tb-shop-info-hd"]/div[2]/dl/dd/a/@href')[0]
    except IndexError:
        xinyu_url='none'
    try:
        tbzhifubao = doc_tree.xpath('.//*[@class="tb-shop-icon"]/dl/dd/a[@class="tb-icon tb-icon-alipay-persion-auth"]/@title')[0]
    except IndexError:
        tbzhifubao = 'none'
    try:
        tbfoodtezhong = doc_tree.xpath('.//*[@class="tb-shop-icon"]/dl/dd/a[@class="tb-icon tb-icon-food"]/@title')[0]
    except IndexError:
        tbfoodtezhong = 'none'
    try:
        tbbaozhengjing = doc_tree.xpath('.//*[@class="tb-shop-icon"]/dl/dd/a[@class="tb-seller-bail"]/@title')[0]
    except IndexError:
        tbbaozhengjing = 'none'
    try:
        tbmiaoshu = doc_tree.xpath('.//*[@class="tb-shop-rate"]/dl[1]/dd/a/text()')[0]
        tbmiaoshu = re.sub('\s', '', tbmiaoshu)
    except IndexError:
        tbmiaoshu = 'none'
    try:
        tbfuwu = doc_tree.xpath('.//*[@class="tb-shop-rate"]/dl[2]/dd/a/text()')[0]
        tbfuwu = re.sub('\s', '', tbfuwu)
    except IndexError:
        tbfuwu = 'none'
    try:
        tbwuliu = doc_tree.xpath('.//*[@class="tb-shop-rate"]/dl[3]/dd/a/text()')[0]
        tbwuliu = re.sub('\s', '', tbwuliu)
    except IndexError:
        tbwuliu = 'none'
    return detail,tbmailname,xinyu_url,tbzhifubao,tbfoodtezhong,tbbaozhengjing,tbmiaoshu,tbfuwu,tbwuliu


f1=codecs.open('yingtao_tianmao_information.txt','a','utf-8')
f2=codecs.open('yingtao_taobao_information.txt','a','utf-8')

headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:63.0) Gecko/20100101 Firefox/63.0'}
f=codecs.open('yingtao_url_new_all.txt','r','utf-8')
k=0
for line in f:
    k+=1
    line1=line.strip().split(',')
    line2=line1[4]
    http = re.search('https', str(line2))
    #print(http)
    if(http):
        url=str(line2)
        print(url)
        #print('ok')
        #url='https://item.taobao.com/item.htm?id=564458907267&ns=1&abbucket=11#detail'
        #url='http://detail.tmall.com/item.htm?id=582875433053&ns=1&abbucket=11'
        res = re.search('detail', url)
        if (res):
            f2.write(str(line1[0]) + ',' + str(line1[1]) + ',' + str(line1[2]) + ',' + str(line1[3]) + ',' + str(
                line1[4]) + ',')
            detail, tbmailname,xinyu_url, tbzhifubao, tbfoodtezhong, tbbaozhengjing, tbmiaoshu, tbfuwu, tbwuliu = get_tb_detail(url)
            for i in range(0, len(detail)):
                f2.write(str(detail[i]) + ',')
            f2.write(str(xinyu_url) + ',' + str(tbzhifubao) + ',' + str(tbfoodtezhong) + ',' + str(
                tbbaozhengjing) + ',' + str(tbmiaoshu) + ',' + str(tbfuwu) + ',' + str(tbwuliu))
            f2.write('\n')
            print(k)
        else:
            f1.write(str(line1[0]) + ',' + str(line1[1]) + ',' + str(line1[2]) + ',' + str(line1[3]) + ',' + str(
                line1[4]) + ',')
            detail, tmmailname, tmmiaoshu, tmfuwu, tmwuliu=get_tm_detail(url)
            for i in range(0, len(detail)):
                f1.write(str(detail[i]) + ',')
            f1.write( str(tmmiaoshu) + ',' + str(tmfuwu) + ',' + str(tmwuliu))
            f1.write('\n')
            print(k)

    else:
        url = 'http:' + str(line2)
        print(url)
        # url='https://item.taobao.com/item.htm?id=564458907267&ns=1&abbucket=11#detail'
        # url='http://detail.tmall.com/item.htm?id=582875433053&ns=1&abbucket=11'
        res = re.search('tmall', url)
        res1 = re.search('taobao', url)
        #print(res1)
        if (res):
            f1.write(str(line1[0]) + ',' + str(line1[1]) + ',' + str(line1[2]) + ',' + str(line1[3]) + ',' + str(
                line1[4]) + ',')
            detail,tmmailname, tmmiaoshu, tmfuwu, tmwuliu = get_tm_detail(url)
            for i in range(0, len(detail)):
                f1.write(str(detail[i]) + ',')
            f1.write( str(tmmiaoshu) + ',' + str(tmfuwu) + ',' + str(tmwuliu))
            f1.write('\n')
            print(k)
        elif (res1):
            f2.write(str(line1[0]) + ',' + str(line1[1]) + ',' + str(line1[2]) + ',' + str(line1[3]) + ',' + str(
                line1[4]) + ',')
            detail, tbmailname,xinyu_url,tbzhifubao, tbfoodtezhong, tbbaozhengjing, tbmiaoshu, tbfuwu, tbwuliu = get_tb_detail(url)
            for i in range(0, len(detail)):
                f2.write(str(detail[i]) + ',')
            f2.write( str(xinyu_url)+','+str(tbzhifubao) + ',' + str(tbfoodtezhong) + ',' + str(
                tbbaozhengjing) + ',' + str( tbmiaoshu) + ',' + str(tbfuwu) + ',' + str(tbwuliu))
            f2.write('\n')
            print(k)