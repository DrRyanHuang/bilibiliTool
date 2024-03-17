# -*- coding: utf-8 -*-
"""
@author: RyanHuang
@github: DrRyanHuang


@updateTime: 2021.08.06
@brife: 用于获取B站给定url视频的弹幕(无需登录, 无需cookie)
@notice:
    If you have suggestions or find bugs, please be sure to tell me. Thanks!
"""

import requests
import re
from bs4 import BeautifulSoup
import pandas as pd


def __getXMlUrl(reponse_text):
    '''
    @brife:
        获得B站弹幕xml的url
        (为了使代码可拓展性更好, 将此函数单独写出)
    @para:
        reponse_text : 响应的内容(Content of the response)
    @notice:
        弹幕所需要的oid和评论所需要的oid竟然不是一个oid
    '''

    match_rule = r'cid=(.*?)&aid'
    oid = re.search(match_rule ,reponse_text).group().replace('cid=','').replace('&aid','')

    # 通过该 `oid` 参数获得xml的链接
    xml_url = 'https://api.bilibili.com/x/v1/dm/list.so?oid='+oid

    return xml_url



def get_df_DanMuFromXML(xml_url, headers=None, save_bool=False, save_path=None):
    '''
    @brife:
        从XML链接中, 获得B站弹幕, 并返回df
        (为了使代码可拓展性更好, 将此函数单独写出, 实际上并没有卵用hhh)
    @para:
        xml_url   : 响应的内容(Content of the response)
        headers   : 请求头字典
        save_bool : 是否保存
        save_path : 保存路径
    '''

    if headers is None:

        headers = {
          'User-Agent':'Mozilla/5.0',
        }

    resp = requests.get(xml_url, headers=headers)
    # 改为推荐编码
    resp.encoding = resp.apparent_encoding
    # 煲汤
    soup = BeautifulSoup(resp.text, 'html.parser')

    # 获得当前的所有弹幕
    danmu_list = soup.findAll('d')

    # 处理所有的 XML
    all_danmu = []
    for item in danmu_list:
        item_list = item.attrs['p'].split(',')
        item_list.append(item.text)

        all_danmu.append(item_list)

    # 在视频中的出现时间
    # 弹幕类型  1为滚动弹幕 4位底部弹幕 5为顶部弹幕
    # 字的大小  分别为 18 和 25
    # 颜色 : FF FF FF为最大值, 转换为了 16 进制
    # 添加弹幕时间戳
    # 是否被保护 ??
    # 用户 id ??
    # 弹幕 id ?? (其在XML中为递增, 与时间戳同为递增)
    # Update(2021.08.06): 这个俺不知道是啥, 去年的这个时候还没有这个属性, 范围是3到10

    columns = ['出现时间',
               '弹幕类型',
               '字的大小',
               '颜色',
               '弹幕添加时间戳',
               'unknown_5',
               'unknown_6',
               'unknown_7',
               'unknown_8',
               '弹幕内容']

    danmu_df = pd.DataFrame(all_danmu, columns=columns)

    if save_bool:

        if save_path is None:
            save_path = 'danmu.csv'

        danmu_df.to_csv(save_path, index=False)

    return danmu_df



def getDanMu(bv_url, headers=None, getXMlUrlFun=None, getDanmuFunc=None, save_bool=False, save_path=None):
    '''
    @brife:
        从B站链接中下载弹幕
        (为了使代码可拓展性更好, 可将处理函数传入)
    @para:
        bv_url        :  可以直接提供BV视频的url, 也可以直接提供BV号
        headers       :  请求头, 详见 `requests.request` 参数解析
        getXMlUrlFun  :  获得XML链接的函数
        getDanmuFunc  :  处理弹幕数据的函数
        save_bool     :  是否保存(优先级高于`save_path`)
        save_path     :  保存路径

        注: 若 `getXMlUrlFun` 和 `getDanmuFunc` 参数需要修改, 则推荐使用 `lambda` 表达式
    '''
    if 'https://' not in bv_url:
        bv_url = 'https://www.bilibili.com/video/{}'.format(bv_url)
    
    if headers is None:

        headers = {
          'User-Agent':'Mozilla/5.0',
        }

    if getXMlUrlFun is None:
        getXMlUrlFun = __getXMlUrl

    if getDanmuFunc is None:
        getDanmuFunc = get_df_DanMuFromXML

    resp = requests.get(bv_url, headers=headers)

    # 得到弹幕XML链接
    danmuXML_url = getXMlUrlFun(resp.text) # 建议用户直接浏览器访问该URL, 以获取更多信息
    # 得到弹幕数据
    danmu_df = getDanmuFunc(danmuXML_url, save_bool=save_bool, save_path=save_path)

    return danmu_df

if __name__ == '__main__':
    
    # 以下代码用于测试
    bv_url = 'https://www.bilibili.com/video/BV1bb4y1z7Gm' # 暴走大事件yyds
    need = getDanMu(bv_url, save_bool=True)