# -*- coding: utf-8 -*-
"""
@author: RyanHuang
@github: DrRyanHuang


@updateTime: 2020.6.22
@brife: 
@notice:
    If you have suggestions or find bugs, please be sure to tell me. Thanks!
"""



import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

headers = {
          'User-Agent':'Mozilla/5.0',
        }

bv_url = 'https://www.bilibili.com/video/BV12a4y1x7Vz'

resp = requests.get(bv_url, headers=headers)

# 改为推荐编码
resp.encoding = resp.apparent_encoding


def getXMlUrl(reponse_text):
    '''
    @brife:
        获得B站评论json的url
        (为了使代码可拓展性更好, 将此函数单独写出)
    @para:
        reponse_text : 响应的内容(Content of the response)
    @notice:
        弹幕所需要的oid和评论所需要的oid竟然不是一个oid, 弹幕中的`oid`是`aid`, 据测试是av号
    '''

    match_rule = r'&aid=(.*?)&attribute'
    oid = re.search(match_rule ,reponse_text).group().replace('&aid=','').replace('&attribute','')

    # 通过该 `oid` 参数获得xml的链接
    xml_url = 'https://api.bilibili.com/x/v2/reply?pn={}&type=1&oid='+oid

    return xml_url



print(getXMlUrl(resp.text))





