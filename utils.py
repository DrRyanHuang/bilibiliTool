import json
import requests as r


def respon2dict(respon: r.Response):

    # 改为推荐编码 -> 改编码会报错故而注销, B站默认: 'utf-8'
    respon.encoding = respon.apparent_encoding
    # 转换成字典
    respon_dict = json.loads(respon.text)

    return respon_dict
