HEADERS = {
    "User-Agent": "Mozilla/5.0",
}


# 格式:
# URL_内容_返回值

"""
following=关注数, 
follower=粉丝数, 
whisper
black
{"code":0,"message":"0","ttl":1,"data":{"mid":517327498,"following":19,"whisper":0,"black":0,"follower":30352069}}
"""
URL_relation_stat_json = "https://api.bilibili.com/x/relation/stat?vmid={}"
