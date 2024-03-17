import requests as r

from constants import HEADERS, URL_relation_stat_json
from utils import respon2dict


class BaseUpLoader:

    def __init__(self):

        self._mid = -1
        self._following = -1
        self._follower = -1

    @property
    def mid(self):
        return self._mid

    @mid.setter
    def mid(self, value):
        self._mid = value

    # -------- 关注数 --------
    @property
    def following(self):
        return self._following

    @following.setter
    def following(self, value):
        self._following = value

    # -------- 粉丝数 --------
    @property
    def follower(self):
        return self._follower

    @follower.setter
    def follower(self, value):
        self._follower = value


class UpLoader(BaseUpLoader):

    def __init__(self, mid=None):
        """
        一个UP主类

        mid:
            https://space.bilibili.com/517327498  # <----- 罗老师的主页, 数字就是 `mid`
        """

        super().__init__()

        self._mid = mid

        assert self._mid

        self.get_relation_stat_json()

    def get_relation_stat_json(self):
        """
        粉丝数, 关注数
        """
        url_relation_stat_json = URL_relation_stat_json.format(self.mid)
        relation_stat_json_respon = r.get(url_relation_stat_json, headers=HEADERS)
        relation_stat_dict = respon2dict(relation_stat_json_respon)["data"]

        self.following = relation_stat_dict.get("following", None)
        self.follower = relation_stat_dict.get("follower", None)


if __name__ == "__main__":

    luo = UpLoader(517327498)
    print("罗老师粉丝数:%d 关注数:%d" % (luo.follower, luo.following))
