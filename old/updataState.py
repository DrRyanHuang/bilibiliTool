# -*- coding: utf-8 -*-
"""
@author: RyanHuang
@github: DrRyanHuang


@updateTime: 2021.08.06
@brife: 使用cookies获取B站在一定时间内投稿队列状态，拥挤还是什么别的
@notice:
    If you have suggestions or find bugs, please tell me. Thanks!
"""

import os
import requests
import json
import time
import pandas as pd


def getCurrentState(user_cookie, data_url=None, headers=None):
    '''
    @brife:
        使用cookie获得B站当前投稿队列状态
        
        重要的事情说三遍:
            获得cookie后, 不能关闭该cookies所属session, 即别关那个获得cookie的网页
            获得cookie后, 不能关闭该cookies所属session, 即别关那个获得cookie的网页
            获得cookie后, 不能关闭该cookies所属session, 即别关那个获得cookie的网页

    @para:
        user_cookie : 用户cookie字符串(需要访问投稿页面)
        data_url    : 投稿页面接口json的url
        headers     : 可定制请求头
    @example:

        >>> getCurrentState(cookie_str)
        {'level': 3,
         'state': '拥挤',
         'comment': '预计稿件过审时间小于60分钟（剧集、活动投稿除外）',
         'time': 1589605497.4562373}
    '''
    
    # B站投稿json数据 url
    if data_url is None:
        data_url = 'https://member.bilibili.com/x/web/archive/pre?langs=cn'
    
    # 爬取所使用的 url
    if headers is None:
        headers = {
          'User-Agent':'Mozilla/5.0',
        }
    
    headers['cookie'] = user_cookie
    
    # 获取请求
    resp = requests.get(data_url, headers=headers)
    resp.encoding = resp.apparent_encoding
    
    data_dict = json.loads(resp.text)
    
    if data_dict['code'] == 0:
        # 添加时间
        data_return = data_dict['data']['video_jam'].copy()
        data_return['time'] = time.time()
        print(data_return['comment'])
    else:
        print("----- Cookie字符串异常, 无法获取 -----")
        data_return = [None]*3 + [time.time()]
        
    return data_return


def createStateCSV(cookie_str, csv_path=None, max_run_time=86400, crawl_interval=60):
    '''
    @brife:
        获取Bilibili上传文件状态的CSV文件, 按 ctrl + C 结束或者达到最大运行时间自动结束
    @para:
        cookie_str     : 响应的内容(Content of the response)
        csv_path       : 存csv数据的文件路径
        max_run_time   : 最大运行时间, 默认为爬取一天的数据, 86400s
        crawl_interval : 爬取间隔, 默认为一分钟爬取一次, 60s
    @example:
        >>> createStateCSV(cookie_str)
        >>> # 会在当前目录下生成数据文件
    '''
    # 获得初始运行时间戳
    start_time = time.time()
    if csv_path is None:
        # csv文件的生成路径
        csv_path = 'state_csv.csv'
    
    # 存放所有数据的列表
    data_list = []
    # 存入数据的df的表头
    columns = ['level', 'state', 'comment', 'time']
    
    try:
        while True:
            # 获得每一次的数据
            item = getCurrentState(cookie_str)
            data_list.append(item)
            
            if time.time() - start_time > max_run_time:
                # 如果爬取时间大于最大运行时间, 则读取保存一次
                
                csv_df = pd.DataFrame(data_list, columns=columns)
                # 如果不存在则直接保存
                if not os.path.exists(csv_path):
                    csv_df.to_csv(csv_path, index=False)
                
                else:
                    temp = pd.read_csv(csv_path)
                    csv_df = csv_df.append(temp)
                    csv_df.to_csv(csv_path, index=False)
                
                print('最大运行时间已到, 程序结束')
                break
                    
            time.sleep(crawl_interval)
        
    except KeyboardInterrupt:
        
        print('手动结束程序')
        csv_df = pd.DataFrame(data_list, columns=columns)
        # 如果手动中断
        if not os.path.exists(csv_path):
            csv_df.to_csv(csv_path, index=False)
        
        else:
            temp = pd.read_csv(csv_path)
            csv_df = csv_df.append(temp)
            csv_df.to_csv(csv_path, index=False)


if __name__ == "__main__":
    # 此代码用于测试
    
    cookie_str = "" # 此处传入你的字符串
    getCurrentState(cookie_str)
    createStateCSV(cookie_str, max_run_time=5, crawl_interval=0.5)

