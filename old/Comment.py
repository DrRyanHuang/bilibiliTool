# -*- coding: utf-8 -*-
"""
@author: RyanHuang
@github: DrRyanHuang


@updateTime: 2021.08.06
@brife: 文件用于爬取视频的评论(无需登录, 无需cookie)
@notice:
    If you have suggestions or find bugs, please tell me. Thanks!
    (使用前最好阅读以下源码)
"""

import requests as r
import re
import json


def __getJSONUrl(reponse_text):
    '''
    @brife:
        获得B站评论json的url
        (为了使代码可拓展性更好, 将此函数单独写出)
    @para:
        reponse_text : 响应的内容(Content of the response)
    @notice:
        弹幕所需要的oid和评论所需要的oid竟然不是一个oid, 弹幕中的`oid`是`aid`, 据测试是av号?
    '''

    match_rule = r'&aid=(.*?)&attribute'
    oid = re.search(match_rule ,reponse_text).group().replace('&aid=','').replace('&attribute','')

    # 通过该 `oid` 参数获得xml的链接
    xml_url = 'https://api.bilibili.com/x/v2/reply?pn={}&type=1&oid='+oid
    
    return xml_url



def __getPageInfo(xml_url, headers=None):
    '''
    @Brife:
        获得评论的部分信息: 如, `num` 当前页面, `count` 总评论数
    @Param:
        xml_url : 获得由之前由函数 `getXMlUrl` 得到的参数 `xml_url`
    '''
    if headers is None:
        headers = {
          'User-Agent':'Mozilla/5.0',
        }
    xml_repose = r.get(xml_url.format(1), headers=headers)
    
    # 改为推荐编码
    xml_repose.encoding = xml_repose.apparent_encoding
    data_first = json.loads(xml_repose.text)
    
    # 通过第一页评论 json , 获得评论的部分信息
    info_dic = data_first['data']['page']
    info_dic['page_count'] = info_dic['count'] // info_dic['size'] + \
                            (1 if (info_dic['count'] % info_dic['size']) else 0)
    
    return info_dic



def getCommList(bv_url, headers=None, getXMlUrl_func=None, getPageInfo_func=None, save_path=None):
    '''
    @Brife:
        用于获取BV的评论JSON数据
    @Param:
        bv_url      :  可以直接提供BV视频的url, 也可以直接提供BV号
        headers     :  爬取的请求头
        getXMlUrl   :  获取评论 URL 的函数, 为了代码可拓展性, 故解耦将其单独列出
        getPageInfo :  用于获取视频评论的信息, 为了代码可拓展性, 故解耦将其单独列出
        save_path   :  保存路径(要含有文件名字!!), 若为None, 则不保存, 
    '''
    # 为了多态和参数初始化
    if headers is None:
        headers = {
          'User-Agent':'Mozilla/5.0',
        }
    
    if 'https://' not in bv_url:
        bv_url = 'https://www.bilibili.com/video/{}'.format(bv_url)
    
    getXMlUrl_func = __getJSONUrl if getXMlUrl_func is None else getXMlUrl_func
    getPageInfo_func = __getPageInfo if getPageInfo_func is None else getPageInfo_func
    

    # 初次读取视频链接响应
    resp = r.get(bv_url, headers=headers)
    
    # 改为推荐编码
    resp.encoding = resp.apparent_encoding
    xml_url = getXMlUrl_func(resp.text) # 建议用户直接浏览器访问该URL, 以获取更多信息
    
    # 获得视频的信息
    info = getPageInfo_func(xml_url)

    # 用于存放所有评论    
    data_comm_all = []
    
    for i in range(1, info['page_count']+1):
        
        # 获取未提取有用信息的评论响应
        comm_raw = r.get(xml_url.format(i), headers=headers)
        
        # 改为推荐编码 -> 改编码会报错故而注销, B站默认: 'utf-8'
        # comm_raw.encoding = comm_raw.apparent_encoding
        # 转换成字典
        data_comm = json.loads(comm_raw.text)
        
        # 提取信息
        data_comm = data_comm['data']['replies']
        
        data_comm_all += data_comm
    
    data_dic = {"comm_dic": data_comm_all}
    
    if save_path is not None:
        with open(save_path, "w", encoding='utf-8') as f:
            json_str = json.dumps(data_dic, ensure_ascii=False, indent=4, separators=(',', ':'))
            f.write(json_str)
            # 建议一定要打开这个json看一下, 这里将全部的评论信息都做了保存(包括评论时间戳, 评论人头像url等)
            # 请手动 load 这个json文件选择你想要的东西, 此处的后处理需要用户自己来写
    return data_comm_all


if __name__ == '__main__':
    
    # 以下代码用于测试
    bv_url = 'https://www.bilibili.com/video/BV1JD4y1U72G'
    need = getCommList(bv_url, save_path='comment.json')


    
    
    
    
    
    