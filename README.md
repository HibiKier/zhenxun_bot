<div align=center><img width="320" height="320" src="https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/zhenxun.jpg"/></div>

![maven](https://img.shields.io/badge/python-3.8%2B-blue)
![maven](https://img.shields.io/badge/nonebot-2.0.0-yellow)
![maven](https://img.shields.io/badge/go--cqhttp-0.9.40--fix4-red)

# 绪山真寻Bot
****
此项目基于 Nonebot2 和 go-cqhttp 开发，以 postgresql 作为数据库的QQ群娱乐机器人
## 关于
用爱发电，某些功能学习借鉴了大佬们的代码，因为绪山真寻实在太可爱了因此开发了
绪山真寻bot，实现了一些对群友的娱乐功能和实用功能（大概）。

如果该项目的图片等等侵犯豆腐猫老师权益请联系我删除！

## 声明
此项目仅用于学习交流，请勿用于非法用途

## 真寻的帮助
请对真寻说: '真寻帮助' or '管理员帮助' or '超级用户帮助' or '对应指令 帮助'


## 功能列表
<details>
<summary>已实现的功能</summary>

### 已实现的常用功能
- [x] 昵称系统（群与群与私聊分开.）
- [x] 图灵AI（会把'你'等关键字替换为你的昵称），且带有 [AnimeThesaurus](https://github.com/Kyomotoi/AnimeThesaurus)，够味
- [x] 签到/我的签到/好感度排行（影响色图概率和开箱次数，支持配置）
- [x] 发送某文件夹下的随机图片（支持自定义，默认：美图，萝莉，壁纸）
- [x] 色图（可配置是否存储到本地，并会判断该色图是否已在本地，存在则跳过）
- [x] coser
- [x] 黑白草图生成器
- [x] 鸡汤/语录
- [x] 骂我（钉宫语音）
- [x] 戳一戳（概率发送美图，钉宫语音或者戳回去）
- [x] 模拟开箱/我的开箱/群开箱统计/我的金色/设置cookie（csgo，内置爬虫脚本，需要提前抓取数据和图片，需要session，可能需要代理，阿里云服务器等ip也许已经被ban了（我无代理访问失败），如果访问太多账号API调用可能被禁止访问api！）
- [x] 鲁迅说过
- [x] 构造假消息（自定义的分享链接）
- [x] 商店/我的金币/购买道具/使用道具
- [x] 原神/明日方舟/赛马娘的抽卡【原神抽卡设置小保底与大保底/重置原神抽卡次数】（根据bwiki自动更新）
- [x] 骰子娘（nb2商店插件）
- [x] 我有一个朋友想问问..（pcrbot插件..重构）
- [x] 原神黄历
- [x] 原神今日素材/天赋材料
- [x] 原神资源查询

- [x] pil对图片的一些操作
- [x] BUFF饰品底价查询（需要session）
- [x] 天气查询
- [x] 疫情查询
- [x] bt搜索
- [x] reimu搜索（上车）
- [x] 靠图识番
- [x] 以图搜图
- [x] 搜番
- [x] 点歌
- [x] epic免费游戏
- [x] p站排行榜（可含参数）
- [x] p站搜图（可含参数）
- [x] 翻译（日英韩）

- [x] 群内csgo服务器（如果没有csgo服务器请删除）
- [x] 查看当前群欢迎消息
- [x] 查看该群自己的权限
- [x] 我的信息（只是为了看看什么时候入群）
- [x] 更新信息（如果继续更新的话）
- [x] go-cqhttp最新版下载和上传（不需要请删除）
- [x] 滴滴滴-（用户对超级用户发送消息）

### 已实现的管理员功能
- [x] 更新群组成员信息
- [x] 95%的群功能开关
- [x] 查看群内被动技能状态
- [x] 自定义群欢迎消息（是真寻的不是管家的！）
- [x] .ban/.unban（支持设置ban时长）
- [x] 刷屏禁言相关：刷屏检测设置/设置禁言时长/设置检测次数
- [x] 上传图片 （上传图片至指定图库）
- [x] 移动图片  （同上）
- [x] 删除图片  （同上）

### 已实现的超级用户功能
- [x] 添加/删除管理
- [x] 开启/关闭指定群的广播通知
- [x] 广播
- [x] 自检（检查系统状态）
- [x] 所有群组/所有好友
- [x] 退出指定群
- [x] 更新好友信息/更新群信息
- [x] /t（对用户进行回复或发送消息）

### 已实现的被动技能
- [x] 进群欢迎消息
- [x] 群早晚安
- [x] 每日开箱重置提醒
- [x] b站转发解析（解析b站分享信息）
- [x] 丢人爬（爬表情包）
- [x] epic通知（每日发送epic免费游戏链接）
- [x] 原神黄历提醒
- [x] 复读

### 已实现的看不见的技能！
- [x] 刷屏禁言检测
- [x] 功能调用统计
- [x] 检测恶意触发命令（将被最高权限ban掉30分钟，只有最高权限(9级)可以进行unban）
- [x] 自动同意好友请求，加群请求将会提醒管理员，退群提示，加群欢迎等等
- [x] 群聊时间检测（当群聊最后一人发言时间大于当前36小时后将关闭该群所有通知（即被动技能））
- [x] 支持对各个管理员功能的权限配置
- [x] 群管理员监控，自动为新晋管理员增加权限，为失去群管理员的用户删除权限
</details>

## 部分功能展示
<details>
<summary>部分功能展示及说明</summary>

### 帮助以及开关（功能控制）

群帮助将会在功能左侧展示该功能的开关，带有√或×的功能代表可以开关
此插件使用 [nonebot_plugin_manager](https://github.com/Jigsaw111/nonebot_plugin_manager) 并魔改一点实现

![](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/help.PNG)
![](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/kg1.png)
![](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/kg3.png)
![](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/kg2.png)

<br>
如果你希望某功能暂时停用<br>
私聊发送 npm block xx （xx=功能名）来锁定<br>
使用npm unblock xx 进行解锁

![](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/ocgn.png)
![](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/ocgn2.png)

### 签到
普普通通的签到，设置影响开箱次数和涩图触发成功的概率（可配置）<br>
开箱次数 = 初始开箱数量 + 好感度 / 3<br>
金币 = random.randint(100) + random.randint(好感度)【好感度获取的金币不会超过200】

![](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/sign.png)

### 黑白草图

整活生成器（从未设想的道路）

![](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/w2b.png)

### 发送文件夹下随机图片

提供了 美图589（获取该图库下文件名589.jpg的图片）方法，图库内图片名称需要有序（如:0.jpg,1.jpg....）

![](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/send_img.png)

### 开箱（csgo模拟开箱）

我的开箱/群开箱统计/我的金色 功能是对开箱数据的统计展示 <br>

目前支持的武器箱（数据已备好）：
* 狂牙大行动武器箱
* 突围大行动武器箱
* 命悬一线武器箱
* 裂空武器箱
* 光谱武器箱
  <br>
  BUFF账号可能会因为短时间内访问api次数过多被禁止访问api！！
  如果是第一次启动请先使用命令 “更新价格”， “更新图片” （需要配置cookie！！如果经常超时请设置代理，配置文件中的 buff_proxy!）<br>
  如果需要配置新的箱子，请在.config.py中配置好该箱子中的皮肤，且列表名是箱子名称的大写拼音<br>
  示例：光谱武器箱 GUANGPU_CASE_KNIFE,GUANGPU_CASE_RED...后面的颜色代表皮肤品质

![](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/kaixiang.png)


### BUFF皮肤底价查询

需要配置cookie！！！！！！！！<br>
如果经常超时请设置代理，配置文件中的 buff_proxy!

![](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/buff.png)


### coser

![](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/coser.png)

### 鸡汤/语录

![](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/jitang.png)

### 骂我

![](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/mawo.png)

### 鲁迅说

此插件使用 [nonebot2_luxun_says](https://github.com/NothAmor/nonebot2_luxun_says)

![](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/luxun.png)

### 假消息

![](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/jiaxiaoxi.png)

### 商店系统

商店内的道具支持自定义，但需要写触发后的效果...整不出活，到头来也就增加好感度概率的商品

![](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/shop.png)
![](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/daoju.png)


### 昵称系统

养成方法第一步，让可爱的小真寻叫自己昵称！（替换ai中的'你'等等）

![](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/nicheng1.png)
![](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/nicheng2.png)

### 抽卡

已经上传至nb2商店，不再放图片了，项目地址：[nonebot_plugin_gamedraw](https://github.com/HibiKier/nonebot_plugin_gamedraw)

### 我有一个朋友...

使用大佬的插件 [cappuccilo_plugins](https://github.com/pcrbot/cappuccilo_plugins#%E7%94%9F%E6%88%90%E5%99%A8%E6%8F%92%E4%BB%B6)

![](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/one_firend.png)


### 原神黄历/今日素材/丘丘语翻译/地图资源查询

使用大佬的插件 [Genshin_Impact_bot](https://github.com/H-K-Y/Genshin_Impact_bot)

### 对图片的操作

只是一些简单对图片操作（娱乐整活）

![](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/tupian.png)

### 识番

使用大佬的插件 [XUN_Langskip](https://github.com/Angel-Hair/XUN_Bot)

![](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/shifan.png)


### 识图

使用nb2商店插件 [nonebot_plugin_cocdicer](https://github.com/abrahum/nonebot_plugin_cocdicer) （可配置图片返回的最大数量）

![](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/shitu.png)

### epic免费游戏

访问rsshub获取数据解析<br>可以不玩，不能没有

![](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/epic.png)


### P站排行/搜图

访问rsshub获取数据解析<br>自己试试吧（# #）

![](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/p_rank.png)
![](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/p_sou.png)


### 翻译

![](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/fanyi.png)

### 自定义群欢迎消息

关键字 [at] 判断是否艾特入群用户

![](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/qhyxx.png)

### 查看当前群欢迎消息

![](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/qunhuanying.png)

### 自检

![](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/check.png)

### .ban/.unban

![](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/ban.png)

### 查看被动技能（被动技能除复读外都提供了开关）

![](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/beidong.png)

### 自我介绍

只是一段简单自我介绍，但是，还是想放上来

![](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/jieshao.png)

### 我的信息/我的权限

![](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/info.png)

<br>

### 其他

点歌：使用 [nonebot_plugin_songpicker2](https://github.com/maxesisn/nonebot_plugin_songpicker2) 插件<br>
骰子娘：使用 [nonebot_plugin_cocdicer](https://github.com/abrahum/nonebot_plugin_cocdicer) 插件
<br><br>
## 其他功能请自己试一试 ）

</details>

## Todo
- [ ] 提供更多对插件的控制
- [ ] 明日方舟卡片式的签到..(大概)
- [ ] 更多的群管理功能

## 部署
```
# 获取代码
git clone https://github.com/Angel-Hair/XUN_Bot.git

# 安装依赖
pip install -r requirements.txt

# 进入目录
cd zhenxun_bot

# 进行基础配置
####请查看 配置 部分####

# 开始运行
python bot.py
```

## 配置
在 ./configs/config.py 中，默认为True

```
# 是否使用配置文件（为True时这将会生成三份配置文件
                 ./config.json：主要配置
                 ./configs/plugins2cmd_config.json: 功能模块与对应命令配置
                 ./configs/other_config.json: 一些插件配置）
                 
USE_CONFIG_FILE = True

# 如果不使用配置文件，将USE_CONFIG_FILE设置为False，可在./configs/config.py文件中修改配置，在./configs/path_config.py修改资源路径
# 已在./configs/config.py和./configs/path_config.py中为各个配置提供注解！
```

## 配置文件注解（如果使用配置文件的话）
<details>
<summary>配置文件注解</summary>
./config.json

```
{
    # 必填（影响功能运行）
    "apikey": {
        "LOLICON_KEY": "",      # loliconAPI，缺失会导致色图功能异常
        "TL_KEY": []            # 图灵Key（为什么要用列表？因为白嫖用户能拿5个apikey，每个apikey每日限制100条）
    },
    
    # （必填！！！）
    # 数据库配置（如果填写了bind，后面就不用再填了)只是帮你拼接好）
    # 示例："bind": "postgresql://user:password@127.0.0.1:5432/database"
    "sql": {
        "bind": "postgresql://hibiki:KEWang130123@hibiki0v0.cn:5432/hibikibot",
        "sql_name": "",
        "user": "",
        "password": "",
        "address": "",
        "port": "",
        "database": ""
    },
    
    # 路径设置（不填则使用默认）
    "path": {
        "IMAGE_PATH": "",   # 图片路径
        "VOICE_PATH": "",   # 音频路径
        "TXT_PATH": "",     # 文本路径
        "LOG_PATH": "",     # 日志路径
        "DATA_PATH": "",    # 数据路径
        "DRAW_PATH": ""     # 抽卡数据路径
        "TEMP_PATH": ""     # 临时图片路径
    },
    
    # 代理设置
    "proxy": {
        "system_proxy": "",     # 系统代理
        "buff_proxy": ""        # buff代理
    },
    
    # RSSHUB地址
    "rsshub": {
        "RSSHUBAPP": "https:\/\/docs.rsshub.app\/"
    },
    
    # 各个管理员功能 对应的 权限
    "level": {
        "DELETE_IMG_LEVEL": 7,
        "MOVE_IMG_LEVEL": 7,
        "UPLOAD_LEVEL": 6,
        "BAN_LEVEL": 5,
        "OC_LEVEL": 2,
        "MUTE_LEVEL": 5
    }
}
```

./configs/plugins2cmd_config.json
```
# 单个例子注解
"send_img": [
            "发送图片",
            "萝莉",
            "美图",
            "壁纸"
        ]
# 发送 关闭发送图片/关闭萝莉/关闭美图/关闭壁纸 都将触发命令 关闭send_img
```

./configs/other_config.json
```
{
    "base": {
        # 图库配置，会影响 上传/删除/移动/发送图片等功能
        "IMAGE_DIR_LIST": [
            "色图",
            "美图",
            "萝莉",
            "壁纸"
        ],
        "BAN_RESULT": "才不会给你发消息."   # 当被ban用户触发命令后发送的消息
    },
    
    "bool": {
        "AUTO_ADD_FRIEND": true,    # 是否自动添加好友
        "DOWNLOAD_SETU": true       # 是否下载bot发送过的色图（不会重复）
    },
    
    "max_count": {
        "MAXINFO_REIMU": 7,           # 上车(reimu)功能查找目的地的最大数
        "COUNT_PER_DAY_REIMU": 5,     # 每日上车(reimu)次数限制
        "MAXINFO_BT": 10,             # bt功能单次查找最大数
        "MAXINFO_PRIVATE_ANIME": 20,  # 私聊搜索动漫返回的最大数量
        "MAXINFO_GROUP_ANIME": 5,     # 群搜索动漫返回的最大数量
        "MAX_FIND_IMG_COUNT": 3,      # 识图最大返回数
        "MAX_SIGN_GOLD": 200          # 签到好感度加成额外获得的最大金币数
    },
    
    "probability": {
        "INITIAL_SETU_PROBABILITY": 0.7,    # 涩图触发的基础概率（触发概率 = 基础概率 + 好感度）
        "FUDU_PROBABILITY": 0.7             # 复读概率
    },
    
    # 注：即在 MALICIOUS_CHECK_TIME 时间内触发相同命令 MALICIOUS_BAN_COUNT 将被ban MALICIOUS_BAN_TIME 分钟
    "malicious_ban": {
        "MALICIOUS_BAN_TIME": 30,       # 恶意触发命令被ban的时长（分钟）
        "MALICIOUS_BAN_COUNT": 4,       # 恶意触发命令的规定次数
        "MALICIOUS_CHECK_TIME": 5       # 恶意触发命令的规定时间（秒）
    },
    "open_case": {
        "INITIAL_OPEN_CASE_COUNT": 20   # 每日开箱的基本数量（总数量=基本数量 + 好感度/3）
    },
    
    # 注：即在 MUTE_DEFAULT_TIME 内发送相似（包含）消息超过 MUTE_DEFAULT_COUNT 将会被 MUTE_DEFAULT_DURATION 分钟
    # 这只是默认配置，各个群可以自由设置群内刷屏检测配置
    "mute": {
        "MUTE_DEFAULT_COUNT": 10,       # 刷屏检测默认检测最大次数
        "MUTE_DEFAULT_TIME": 7,         # 刷屏检测默认规定时间（秒）
        "MUTE_DEFAULT_DURATION": 10     # 刷屏检测默认禁言时长（分钟）
    },
    "other": {
        "UPDATE_GOCQ_GROUP": [],      # 是否需要为某些群上传最新版的gocq？
        "ADMIN_DEFAULT_AUTH": 5       # 默认群管理员权限
    },
    
    # 管理员功能 和 对应的 权限
    "auth": {
        "admin_plugins_auth": {
            "admin_bot_manage": 2,
            "ban": 5,
            "delete_img": 7,
            "move_img": 7,
            "upload_img": 6,
            "admin_help": 1,
            "mute": 5
        }
    }
}
```
</details>




## 感谢
[Onebot](https://github.com/howmanybots/onebot)
<br>
[go-cqhttp](https://github.com/Mrs4s/go-cqhttp)
<br>
[nonebot2](https://github.com/nonebot/nonebot2)
<br>
[XUN_Langskip](https://github.com/Angel-Hair/XUN_Bot)
<br>
[cappuccilo_plugins](https://github.com/pcrbot/cappuccilo_plugins#%E7%94%9F%E6%88%90%E5%99%A8%E6%8F%92%E4%BB%B6)
<br>
[nonebot_plugin_cocdicer](https://github.com/abrahum/nonebot_plugin_cocdicer)
<br>
[nonebot_plugin_songpicker2](https://github.com/maxesisn/nonebot_plugin_songpicker2)
<br>
[nonebot_plugin_manager](https://github.com/Jigsaw111/nonebot_plugin_manager)
<br>
[Genshin_Impact_bot](https://github.com/H-K-Y/Genshin_Impact_bot)
<br>
[nonebot2_luxun_says](https://github.com/NothAmor/nonebot2_luxun_says)
<br>
[AnimeThesaurus](https://github.com/Kyomotoi/AnimeThesaurus)
