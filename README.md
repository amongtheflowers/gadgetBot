# gadgetBot
瞎搞！想到啥弄啥！基于[nonebot]框架的QQ机器人

[nonebot]: https://github.com/richardchien/nonebot

## 目前功能
1. 获取bilibili视频封面图片
2. 剑网3科举题
3. 智能聊天(基于腾讯ai)
4. 语音合成(后续合并到智能聊天里)
5. B站开播提醒
6. 5s游戏（跟[天亮前の黎明]大佬的一样的
8. 名片点赞
9. 刷屏禁言(感觉有点儿错误)
10. QQ空间发说说(多图只使用横排)
## TODO
#### 剑网3系列
1. 金价查询
2. 开服监控
3. 宠物查询
4. 。。。

#### B站系列
1. 在QQ跟弹幕聊天(好像会关小黑屋而且需要cookie暂时不做)
2. 。。。

#### 其他
1. 抽签
2. 签到
3. 。。。

## 引用
#### aio.requests 和 untils.fs 源码使用的是[aki]奶茶的源码(RCNB)

[aki]: https://github.com/cczu-osa/aki/tree/master/aki



## 聊天跟语音合成说明
智能聊天使用的是[腾讯ai开放平台]的接口,使用QQ登陆创建一个应用，接入智能闲聊能力，拿到的appid跟appkey填入config.py.
代码原有的不知道啥时候会过期还是自己申请一个比较好
```bash 
TX_CHAT_APPID = 'appid'
TX_CHAT_APPKEY = 'appkey'
```
语音合成使用的是百度语音合成的接口，还是跟上面一样在config.py里面配置
```bash
BD_CLIENT_ID = ''
BD_CLIENT_SECRET = ''
BD_TOKEN = '' #会通过ID跟SECRET自动获取这个不需要填写（）
```
[腾讯ai开放平台]:https://ai.qq.com/
#### 功能使用
##### 科举
```bash
触发方式 群聊,私聊
科举+空格+关键字
科举 青岩诗
```
##### B站封面
```bash
触发方式 群聊,私聊
封面+空格+av号
封面 av1234567
```

##### 聊天
```bash
触发方式 私聊,群艾特或者nickname
nickname可以在config.py配置
NICKNAME = {'猫'}
猫,你好呀来聊天吗?
```

##### 语音合成
```bash
触发方式 私聊,群聊
说 + 内容 不需要空格可指定男女
说你好呀
--------------
指定性别:说+内容+空格+性别
说你好呀 女
```

##### B站直播订阅
```bash
触发方式 群聊需管理员或群主 ,私聊
开播订阅房间号
开播订阅3
----------------
取消订阅房间号
取消订阅3
```

#### 5s游戏
5s 基于酷Q社区[天亮前の黎明]大佬源码修改

[天亮前の黎明]: https://cqp.cc/t/39520
```bash
触发方式 群聊
5s
```


#### 点赞
```bash
触发方式 赞我 点赞
```









