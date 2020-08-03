# -*- coding: utf-8 -*-
"""
@author: RyanHuang
@github: DrRyanHuang


@updateTime: 2020.8.3
@brife: 用于获取给定url的中国大学MOOC视频评论
@notice:
    If you have suggestions or find bugs, please be sure to tell me. Thanks!
    仅供交流学习, 请遵循法律法规, 本代码开源协议为 `GPL v3`
    
    务必查看, 当前时间的中国大学MOOC网站的 `robots.txt` !
"""

import json
import re
import time

import requests as r
import pandas as pd

    
class MOOCCommeCrawler:
    
    def __init__(self, course_link, headers=None):
        '''
        @Notice:
            为了使类内部函数方便拓展, 笔者函数之间尽量解耦合
        @Param:
            course_link : 你要爬取的课程链接，
                          比如: https://www.icourse163.org/course/BIT-268001
            headers     : 爬取需要的头文件
        '''
        self._course_link = course_link
        
        if headers is None:
            self.headers = {'User-Agent':'Mozilla/5.0'}
        else:
            self.headers = headers
        
        # 由于需要 `cookies`, 所以我们需要一个 session
        self.sess = r.Session()
        
        self.repose = self.sess.get(self._course_link, headers=self.headers)
        self.repose.encoding = self.repose.apparent_encoding
        
        self._course_ID = self.getCourseID()
        self._csrfKey_str = self.getCsrfKey_str()
        self._course_eval_dic = self.getCourseEvalNum()
  
    
    def getCourseID(self, match_rule=None, repose_text=None, match_after_func=None):
        '''
        @Brife:
            用于获得[中国大学MOOC]课程的ID号
        @Param:
            match_rule        : 正则表达式匹配规则, 已给出默认匹配方式
            repose_text       : 响应文本, 默认为 `__init__` 中的响应文本
            match_after_func  : 匹配过后的, 对结果的处理函数, 默认为本函数的处理方式
        @Return:
            返回课程ID号
        @Notice:
            笔者为了之后拓展方便, 故而将代码写成这样, 本来就一句话的事儿hhh
        '''
        
        if match_rule is None:
            match_rule = r'id:"(.*?)"'
            
        if repose_text is None:
            repose_text = self.repose.text
        
        courseID_raw = re.search(match_rule ,repose_text).group()
        
        if courseID_raw is None:
            raise ValueError('匹配规则有误')
        
        if match_after_func is None:
            courseID = courseID_raw.replace('id:"', '').replace('"', '')
            return courseID
        else:
            return match_after_func(courseID_raw)
        
        
    def getCsrfKey_str(self):
        '''
        @Brife:
            用于获得后续需要的 CsrfKey 字符串(该接口后可以继承后重写)
        @Param:
            None
        @Return:
            返回当前访问的 `csrfKey` 字符串
        @Notice:
            笔者为了之后拓展方便, 故而将代码写成这样, 本来就一句话的事儿hhh
        '''
        return self.sess.cookies['NTESSTUDYSI']


    def getCourseEvalNum(self, course_info_jsonURL=None):
        '''
        @Brife:
            用于获取课程的评价数据(实际上只有课程评分和课程评论数)
        @Param:
            course_info_jsonURL :  获得课程评价信息的URL
        @Return:
            返回一个字典, 包含一些评价数据
            其中键"evaluateCount"代表评论数, 
                键"avgMark"代表课程评分(5分满分)
                键"targetId"代表课程ID(和之前求取的课程ID相同)
        '''
        if course_info_jsonURL is None:
            
            course_info_jsonURL = \
            '''
            https://www.icourse163.org/web/j/mocCourseV2RpcBean.getEvaluateAvgAndCount.rpc?csrfKey={}
            '''.strip()
        
        info_url = course_info_jsonURL.format(self._csrfKey_str)
        
        data = {'courseId':self._course_ID}
        respon = self.sess.post(info_url, data=data, headers=self.headers)
        respon.encoding = respon.apparent_encoding
        
        info_dic = json.loads(respon.text)
        return info_dic["result"]


    def getComm1Page(self, form_data=None, comment_jsonURL=None):
        '''
        @Brife:
            用于获取课程的 **一页** 评论
        @Param:
            form_data       :  向指定页面提交的表单, dict
            comment_jsonURL :  评论json的url链接
        @Return:
            返回一个当前爬取情况的字典, dict
            返回一个评论列表, list, 列表元素为评论的内容信息字典
        '''
        if comment_jsonURL is None:
            
            comment_jsonURL = \
            '''
            https://www.icourse163.org/web/j/mocCourseV2RpcBean.getCourseEvaluatePaginationByCourseIdOrTermId.rpc?csrfKey={}
            '''.strip()
        
        info_url = comment_jsonURL.format(self._csrfKey_str)
        
        if form_data is None:
                
            form_data = {'courseId' : self._course_ID,
                         'pageIndex': 1,
                         'pageSize': 20,
                         'orderBy': 3}
        
        respon = self.sess.post(info_url, data=form_data, headers=self.headers)
        respon.encoding = respon.apparent_encoding
        
        comm_json = json.loads(respon.text)
        

        return comm_json['result']['query'], comm_json['result']['list']
        
    
    def getAllComments(self, save_path=None, intervals=0.2):
        '''
        @Brife:
            爬取当前连接的所有评论
        @Param:
            save_path  :  爬取数据的保存path, eg: 'temp/xx.csv'
            intervals  :  每次爬取的时间间隔
        @Notice:
            请遵守 `robots.txt` 不可将 `intervals` 设置的过小！
        '''
        query_info, comm_list = self.getComm1Page()
        totlePageCount = query_info['totlePageCount']
        
        form_data = {'courseId' : self._course_ID,
                     'pageIndex': 1,
                     'pageSize': 20,
                     'orderBy': 3}
        
        try:
            # 为了大家能看到爬取进度, 则使用 `tqdm` 
            from tqdm import tqdm
            iter_range = tqdm(range(2, totlePageCount+1))
        except ImportError:
            iter_range = range(2, totlePageCount+1)
        
        for i in iter_range:
            
            form_data['pageIndex'] = i
            comm_list += self.getComm1Page(form_data=form_data)[1]
            # 注意, 这里不能为了速度而注释掉这里, 请查看 `robots.txt` 获取详细内容
            time.sleep(intervals)
        
        self.all_comm_df = pd.DataFrame(comm_list)
        
        if save_path is None:
            pass
        else:
            self.all_comm_df.to_csv(save_path, index=False)
        
        return self.all_comm_df
        

# 以下是爬取实例
if __name__ == '__main__':
    
    # 课程链接, 嵩天老师应该不会怪我吧 hhh
    course_link = 'https://www.icourse163.org/course/BIT-268001'
    # 创建爬虫对象
    crawler = MOOCCommeCrawler(course_link)
    # 爬取全部评论, 注意爬取间隔设置, 不可过快！！！！！ 你的IP可能被封掉！！
    all_comm = crawler.getAllComments(save_path='BIT-268001.csv', intervals=0.5)
    
    # 最后在这里, 对中国大学MOOC表示真诚的感谢, 感谢其对中国教育事业做出的巨大贡献！比心！
    '''
    代码仅供学习和参考, 请遵守法律法规, 遵循开源协议, 务必查看 `robots.txt`
    放上我的镇楼之宝！违者会被电哦！！！

    
        quu..__
         $$$b  `---.__
          "$$b        `--.                          ___.---uuudP
           `$$b           `.__.------.__     __.---'      $$$$"              .
             "$b          -'            `-.-'            $$$"              .'|
               ".                                       d$"             _.'  |
                 `.   /                              ..."             .'     |
                   `./                           ..::-'            _.'       |
                    /                         .:::-'            .-'         .'
                   :                          ::''\          _.'            |
                  .' .-.             .-.           `.      .'               |
                  : /'$$|           .@"$\           `.   .'              _.-'
                 .'|$u$$|          |$$,$$|           |  <            _.-'
                 | `:$$:'          :$$$$$:           `.  `.       .-'
                 :                  `"--'             |    `-.     \
                :##.       ==             .###.       `.      `.    `\
                |##:                      :###:        |        >     >
                |#'     `..'`..'          `###'        x:      /     /
                 \                                   xXX|     /    ./
                  \                                xXXX'|    /   ./
                  /`-.                                  `.  /   /
                 :    `-  ...........,                   | /  .'
                 |         ``:::::::'       .            |<    `.
                 |             ```          |           x| \ `.:``.
                 |                         .'    /'   xXX|  `:`M`M':.
                 |    |                    ;    /:' xXXX'|  -'MMMMM:'
                 `.  .'                   :    /:'       |-'MMMM.-'
                  |  |                   .'   /'        .'MMM.-'
                  `'`'                   :  ,'          |MMM<
                    |                     `'            |tbap\
                     \                                  :MM.-'
                      \                 |              .''
                       \.               `.            /
                        /     .:::::::.. :           /
                       |     .:::::::::::`.         /
                       |   .:::------------\       /
                      /   .''               >::'  /
                      `',:                 :    .'
                                           `:.:'
         

    '''
        
        