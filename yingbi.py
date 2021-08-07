# -*- coding: utf-8 -*-
"""
@author: RyanHuang
@github: DrRyanHuang


@updateTime: 2021.08.06
@brife: 用于获取B站给定url视频的硬币收藏数等(无需登录, 无需cookie)
@notice:
    If you have suggestions or find bugs, please be sure to tell me. Thanks!
"""

import json
import requests as r
import re


# https://api.bilibili.com/x/player/v2?cid=217465303&aid=711571561&bvid=BV1JD4y1U72G


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




def getVideoInfoFromAid(aid, headers=None):
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
    
    repon_str = json.loads(repon.text)
    '''
    注:
        >>> repon_str.keys()
        dict_keys(['code', 'message', 'ttl', 'data'])
        
        >>> # 此处的键: 'code', 'message', 'ttl', 暂时未知, 但应该对本代码不影响
    '''
    video_info = repon_str['data']
    
    return video_info








# 视频链接
# https://lv6rur2.yfcalc.com:48129/upos-dash-mirrorks3u.bilivideo.com/bilibilidash_9bcf6f6d51fa976772f26e7148b34dcff9d6736f/197909629_nb2-1-30080.m4s?timeout=1595922942&check=2576959748&yfdspt=1595318142783&sttype=90&scuid=I7VmBFeAx22t6dB1niZx&yfpri=150&yfopt=17&yfskip=1&yfreqid=CMpPliFRgDxaffsAAF&yftt=100&yfhost=0nmr0o1.yfcache.com&yfpm=1
# 主页视频信息
# https://api.bilibili.com/x/space/arc/search?mid=10119428&ps=30&pn=2
uid = '10119428'
space_url = 'https://space.bilibili.com/10119428'


def _(uid=None, space_uid=None):
    '''
    @brife:
        uid        : 用户 `id` 号
        space_uid  : 用户的 `space` 的url
    '''
    space_url = 'https://space.bilibili.com/{}'.format(uid)
    
    


    
    
    
    
    
    
    
    
    
    
    
    
    
    