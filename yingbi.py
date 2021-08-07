# -*- coding: utf-8 -*-
"""
@author: RyanHuang
@github: DrRyanHuang


@updateTime: 2021.08.06
@brife: 本代码无效, 用于测试

@notice:
    If you have suggestions or find bugs, please be sure to tell me. Thanks!
"""

import json
import requests as r
import re


# https://api.bilibili.com/x/player/v2?cid=217465303&aid=711571561&bvid=BV1JD4y1U72G



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
    
    


    
    
    
    
    
    
    
    
    
    
    
    
    
    