<h1 align="center">- Bilibili Tool -</h1>

<p align="center">
<img src="https://img.shields.io/badge/version-V0.2-green.svg?longCache=true&style=for-the-badge">
<img src="https://img.shields.io/badge/license-GPL%20(%3E%3D%202)-blue.svg?longCache=true&style=for-the-badge">
</p>



<p align="center">
<pre>
                      //
          \\         //
           \\       //
    ##DDDDDDDDDDDDDDDDDDDDDD##
    ## DDDDDDDDDDDDDDDDDDDD ##
    ## hh                hh ##
    ## hh    //    \\    hh ##
    ## hh   //      \\   hh ##
    ## hh                hh ##
    ## hh      wwww      hh ##
    ## hh                hh ##
    ## MMMMMMMMMMMMMMMMMMMM ##
    ##MMMMMMMMMMMMMMMMMMMMMM##
         \/            \/
    ________   ___   ___        ___   ________   ___   ___        ___
   |\   __  \ |\  \ |\  \      |\  \ |\   __  \ |\  \ |\  \      |\  \
   \ \  \|\ /_\ \  \\ \  \     \ \  \\ \  \|\ /_\ \  \\ \  \     \ \  \
    \ \   __  \\ \  \\ \  \     \ \  \\ \   __  \\ \  \\ \  \     \ \  \
     \ \  \|\  \\ \  \\ \  \____ \ \  \\ \  \|\  \\ \  \\ \  \____ \ \  \
      \ \_______\\ \__\\ \_______\\ \__\\ \_______\\ \__\\ \_______\\ \__\
       \|_______| \|__| \|_______| \|__| \|_______| \|__| \|_______| \|__|
</pre>
</p>



<h4 align="center">🛠️ 哔哩哔哩（B站）低(mei)级(yong)工具箱</h4>




#### `updataState.py`

用于获得B站上传状态，是拥挤还是爆满等

![state.png](./src/state.png)

爬取时需要用户手动提供`cookie`字符串
且勿关闭该cookies所属session, 即别关那个获得cookie的网页



#### `danMu.py`
爬取单个视频的弹幕，给定参数后可以保存到给定目录，不需要用户cookie，只需要BV视频的url


#### `Comment.py`
爬取单个视频的评论，给定参数后可以保存到给定目录，不需要用户cookie，只需要BV视频的url


#### `currentWatch.py`
获取该视频当前的观看人数，不需要用户cookie，只需要BV视频的url


#### `pageInfo.py`
获取该视频每一P的信息(包括名字, 播放时长等信息)，不需要用户cookie，只需要BV视频的url


#### `videoExtraInfo.py`
获取该视频的额外信息，比如`aid`、`bvid`、`view`(视频播放数)、`danmaku`(总弹幕数)、`reply`(评论数)、`share`(分享数)、`like`(点赞数)、`favorite`(收藏)、`coin`(投币数)，，不需要用户cookie，只需要BV视频的url


#### 一些心得
写爬取这些东西的代码是异常无聊的，有意思的也就是找到url，其他的无非就是导库，下载后读取，后处理保存

大部分网站都会将这些资源(如弹幕和评论等信息资源)，整为xml格式或者json格式的url，写本仓库这样简单的爬虫，难点就是找url，其他的就看Python基础掌握的好不好了

希望你能自己找到几个不同的字符串，如`BVid`、`aid`、`oid`(应该是有两个)和`cid`，找到他们分别对应哪些资源

爬取弹幕那一块，我希望你能自己把那些属性到底指的是什么想明白，希望能自己根据弹幕的样式，去猜属性的含义(话说，一年前那会儿还没有高级弹幕，我也不知道那个代码能不能有效应对高级弹幕)

我希望你能感觉到我写的过于冗余，然后用类封装好。时隔一年，我再一次看我之前写的代码，还是一样的想法，代码冗余太多，写成类就好了，初始化的时候将`BVid`、`aid`和`oid`等东西读入，之后用哪个拿哪个就好了

我还只是个写爬虫的新手，也只会找找简单的url，再往深走走，就可能涉及到逆向的知识，我已经停滞不前两三年了吧，没有什么进步hhh





