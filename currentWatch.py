# -*- coding: utf-8 -*-
"""
@author: RyanHuang
@github: DrRyanHuang


@CreateTime: 2021.08.06
@brife: 获取某视频当前正在看的人数
@notice:
    If you have suggestions or find bugs, please tell me. Thanks!
"""

import requests as r
import json

def __getCID(BVid, headers=None):
    '''
    @brife:
        每个BV视频的每一P都会对应一个Cid
        获取当前视频的每一个CID
        (为了使代码可拓展性更好, 将此函数单独写出)
    @param:
        BVid    : 视频的BV号, 就是视频链接后边那一段
        headers : 爬取的请求头
    @notice:
    '''
    
    cid_url = "https://api.bilibili.com/x/player/pagelist?bvid={}".format(BVid)
    
    if headers is None:
        headers = {
          'User-Agent':'Mozilla/5.0',
        }
        
    pages_info_raw = r.get(cid_url, headers=headers)
    # 改为推荐编码 -> 改编码会报错故而注销, B站默认: 'utf-8'
    pages_info_raw.encoding = pages_info_raw.apparent_encoding
    # 转换成字典
    pages_info = json.loads(pages_info_raw.text)['data']
    # 将所有的 cid 提取出来
    all_cid = [page['cid'] for page in pages_info]
    
    return all_cid


def getCurrentWatch(BVid, headers=None, CID_select_func=lambda x:x[0]):
    '''
    @brife:
        获取正在看的人数
    @param:
        reponse_text    : 响应的内容(Content of the response)
        BVid            : 视频的BV号, 就是视频链接后边那一段
        CID_select_func :
    @notice:
        爬取正在看竟然需要cid......
        每个BV视频的每一P都会对应一个Cid
    '''
    
    # 获取当前视频的所有cid
    all_cid = __getCID(BVid)
    # 选择你需要的cid
    cid_selected = CID_select_func(all_cid)
    # 通过该 `cid` 参数获得 JSON 的链接
    JSON_url = "https://api.bilibili.com/x/player/online/total?cid={}&bvid={}".format(cid_selected, BVid)
    
    info_raw = r.get(JSON_url, headers=headers)
    # 改为推荐编码 -> 改编码会报错故而注销, B站默认: 'utf-8'
    info_raw.encoding = info_raw.apparent_encoding
    # 转换成字典
    info = json.loads(info_raw.text)
    
    return info['data']


if __name__ == "__main__":
    info = getCurrentWatch("BV12W411x7ac")
    # 大概长这样:
    # {'total': '10+', 'count': '14', 'show_switch': {'total': True, 'count': True}}
    print(info)
