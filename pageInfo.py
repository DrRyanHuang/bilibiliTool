# -*- coding: utf-8 -*-
"""
@author: RyanHuang
@github: DrRyanHuang


@CreateTime: 2021.08.06
@brife: 获取视频有多少P, 每一P有多长时间(无需Cookie)
@notice:
    If you have suggestions or find bugs, please tell me. Thanks!
"""
import requests
import json
import pandas as pd


def __getJSONUrl(BVid):
    '''
    @brife:
        获得每一P json信息的url
    @para:
        BVid         : 视频的BV号, 就是视频链接后边那一段
    @notice:
        只需要一个 BVid , 我和我的小伙伴们都惊呆了
    '''
    
    # 通过该 `BVid` 参数获得链接
    JSON_url = "https://api.bilibili.com/x/player/pagelist?bvid={}"
    
    return JSON_url.format(BVid)
 


def getPageInfo(BVid, headers=None, save_path=None):
    '''
    @brife:
        获得该BV视频下所有P JSON信息并保存
    @para:
        BVid      : 视频的BV号, 就是视频链接后边那一段
        headers   : 爬取的请求头
        save_path : 保存路径(要含有文件名字!!), 若为None, 则不保存
    @notice:
        
    '''
    if headers is None:

        headers = {
          'User-Agent':'Mozilla/5.0',
        }
    
    JSON_url = __getJSONUrl(BVid)
    
    resp = requests.get(JSON_url, headers=headers)
    # 改为推荐编码
    resp.encoding = resp.apparent_encoding
    
    ALL_P_info = json.loads(resp.text)['data']

    if save_path is not None:
        with open(save_path, "w", encoding='utf-8') as f:
            json_str = json.dumps(ALL_P_info, ensure_ascii=False, indent=4, separators=(',', ':'))
            f.write(json_str)
    return ALL_P_info



def pageInfoDict2CSV(info_dicts, save_csv=None):
    '''
    @brife:
        将 info_dict字典 转化为 DataFrame, 返回DF
    @para:
        info_dicts  :  视频的BV号, 就是视频链接后边那一段
        save_csv    :  保存的 csv 的文件, None则不保存
    @notice:
        
    '''
    info_dicts_copy = info_dicts.copy()
    for info_dict in info_dicts_copy:
        info_dict['dimen_width' ] = info_dict['dimension' ]['width']
        info_dict['dimen_height'] = info_dict['dimension' ]['height']
        info_dict['dimen_rotate'] = info_dict['dimension' ]['rotate']
        info_dict.pop("dimension")
    
    info_dicts_df = pd.DataFrame(info_dicts_copy)
    if save_csv is not None:
        info_dicts_df.to_csv(save_csv, index=False)
    
    return info_dicts_copy



if __name__ == '__main__':
    
    # 以下代码用于测试
    all_page_info = getPageInfo("BV1264y1b7uG", save_path="page_info.json")
    pageInfoDict2CSV(all_page_info, "info.csv")















