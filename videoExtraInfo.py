# -*- coding: utf-8 -*-
"""
@author: RyanHuang
@github: DrRyanHuang


@updateTime: 2021.08.07
@brife: 文件用于爬取视频的额外信息(无需登录, 无需cookie)
@notice:
    If you have suggestions or find bugs, please tell me. Thanks!
    (使用前最好阅读以下源码)
"""

import requests as r
import re
import json


def __get_aid(reponse_text):
    '''
    @brife:
        获得当前视频的 aid
        (为了使代码可拓展性更好, 将此函数单独写出)
    @para:
        reponse_text : 响应的内容(Content of the response)
    @notice:
        该 aid 和弹幕的oid是同一个
    '''
    match_rule = r'&aid=(.*?)&attribute'
    aid = re.search(match_rule ,reponse_text).group().replace('&aid=','').replace('&attribute','')

    return aid


def __getVideoInfoFromAid(aid, headers=None):
    '''
    @Brife:
        通过 `aid` 获得视频的数据
        
        aid、bvid、view(视频播放数)、danmaku(总弹幕数)、reply(评论数)
        share(分享数)、like(点赞数)、favorite(收藏)、coin(投币数)
    @Param:
        aid     : B站视频的 `aid`
        headers : 请求头字典
    @Return:
        video_info : 返回B站视频的点赞收藏量字典
    @Notice:
        
        以下参数暂时未知:
            
            "now_rank": 0,
            "his_rank": 0,
            "no_reprint": 1,
            "copyright": 1,
            "argue_msg": "",
            "evaluation": ""

    '''
    data_url = 'https://api.bilibili.com/x/web-interface/archive/stat?aid={}'.format(aid)
    
    if headers is None:
        headers = {
          'User-Agent':'Mozilla/5.0',
        }
    
    repon = r.get(data_url, headers=headers)
    repon.encoding = repon.apparent_encoding
    
    repon_dic = json.loads(repon.text)
    '''
    注:
        >>> repon_str.keys()
        dict_keys(['code', 'message', 'ttl', 'data'])
        
        >>> # 此处的键: 'code', 'message', 'ttl', 暂时未知, 但应该对本代码不影响
    '''
    video_info = repon_dic['data']
    
    return video_info



def getExtraInfo(bv_url, headers=None, save_path=None):
    '''
    @Brife:
        用于获取BV的评论JSON数据
    @Param:
        bv_url      :  可以直接提供BV视频的url, 也可以直接提供BV号
        headers     :  爬取的请求头
        save_path   :  保存路径(要含有文件名字!!), 若为None, 则不保存
    @Notice:
        这个代码冗余好多, 我好不想写hhhhhh
    '''
    # 为了多态和参数初始化
    if headers is None:
        headers = {
          'User-Agent':'Mozilla/5.0',
        }
    
    if 'https://' not in bv_url:
        bv_url = 'https://www.bilibili.com/video/{}'.format(bv_url)
    
    # 初次读取视频链接响应
    resp = r.get(bv_url, headers=headers)
    
    # 改为推荐编码
    resp.encoding = resp.apparent_encoding
    aid = __get_aid(resp.text)
    video_info = __getVideoInfoFromAid(aid)
    
    return video_info


if __name__ == '__main__':
    
    # 以下代码用于测试
    info = getExtraInfo("BV1zb4y167ii")
    print(info)