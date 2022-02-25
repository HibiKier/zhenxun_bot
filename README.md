<div align=center><img width="320" height="320" src="https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/logo.png"/></div>

![maven](https://img.shields.io/badge/python-3.8%2B-blue)
![maven](https://img.shields.io/badge/nonebot-2.0.0-yellow)
![maven](https://img.shields.io/badge/go--cqhttp-1.0.0-red)

# 绪山真寻Bot
****
此项目基于 Nonebot2 和 go-cqhttp 开发，以 postgresql 作为数据库的QQ群娱乐机器人
## 关于
用爱发电，某些功能学习借鉴了大佬们的代码，因为绪山真寻实在太可爱了因此开发了
绪山真寻bot，实现了一些对群友的娱乐功能和实用功能（大概）。

如果该项目的图片等等侵犯猫豆腐老师权益请联系我删除！  

如果希望有个地方讨论绪山真寻Bot，或者有问题或建议，可以发送issues或加入[ <strong>[是真寻酱哒](https://jq.qq.com/?_wv=1027&k=u8PgBkMZ) </strong>]

## 声明
此项目仅用于学习交流，请勿用于非法用途

## Gitee

# [Gitee](https://gitee.com/two_Dimension/zhenxun_bot)

## 未完成的文档

# [传送门](https://hibikier.github.io/zhenxun_bot/)

## 真寻的帮助
请对真寻说: '真寻帮助' or '管理员帮助' or '超级用户帮助' or '真寻帮助 指令'

## 普通帮助图片
![x](https://github.com/HibiKier/zhenxun_bot/blob/0.0.8.2/docs_image/3238573864-836268675-E2FFBB2AC143EAF4DDDF150438508721.png)

## 提供符合真寻标准的插件仓库

[AkashiCoin/nonebot_plugins_zhenxun_bot](https://github.com/AkashiCoin/nonebot_plugins_zhenxun_bot)

## 来点优点？

  * 实现了许多功能，且提供了大量功能管理命令
  * 通过Config配置项将所有插件配置统计保存至config.yaml，利于统一用户修改
  * 方便增删插件，原生nonebot2 matcher，不需要额外修改，仅仅通过简单的配置属性就可以生成`帮助图片`和`帮助信息`
  * 提供了cd，阻塞，每日次数等限制，仅仅通过简单的属性就可以生成一个限制，例如：`__plugin_cd_limit__`
  * __..... 更多详细请通过`传送门`查看文档！__


## 功能列表
<details>
<summary>已实现的功能</summary>

### 已实现的常用功能
- [x] 昵称系统（群与群与私聊分开.）
- [x] 图灵AI（会把'你'等关键字替换为你的昵称），且带有 [AnimeThesaurus](https://github.com/Kyomotoi/AnimeThesaurus)，够味
- [x] 签到/我的签到/好感度排行/好感度总排行（影响色图概率和开箱次数，支持配置）
- [x] 发送某文件夹下的随机图片（支持自定义，默认：美图，萝莉，壁纸）
- [x] 色图（这不是基础功能嘛喂）
- [x] coser
- [x] 黑白草图生成器
- [x] 鸡汤/语录
- [x] 骂我（钉宫语音）
- [x] 戳一戳（概率发送美图，钉宫语音或者戳回去）
- [x] 模拟开箱/我的开箱/群开箱统计/我的金色/设置cookie（csgo，内置爬虫脚本，需要提前抓取数据和图片，需要session，可能需要代理，阿里云服务器等ip也许已经被ban了（我无代理访问失败），如果访问太多账号API调用可能被禁止访问api！）
- [x] 鲁迅说过
- [x] 构造假消息（自定义的分享链接）
- [x] 商店/我的金币/购买道具/使用道具
- [x] 8种手游抽卡 (查看 [nonebot_plugin_gamedraw](https://github.com/HibiKier/nonebot_plugin_gamedraw))
- [x] 我有一个朋友想问问..（借鉴pcrbot插件）
- [x] 原神黄历
- [x] 原神今日素材
- [x] 原神资源查询  (借鉴[Genshin_Impact_bot](https://github.com/H-K-Y/Genshin_Impact_bot)插件)
- [x] 原神便笺查询
- [x] 原神玩家查询
- [x] 原神树脂提醒
- [x] 原神签到/自动签到
- [x] 金币红包
- [x] 微博热搜
- [x] B站主播/UP/番剧订阅

- [x] pil对图片的一些操作
- [x] BUFF饰品底价查询（需要session）
- [x] 天气查询
- [x] 疫情查询
- [x] bt磁力搜索（咳咳，这功能我想dddd）
- [x] reimu搜索（上车） (使用[XUN_Langskip](https://github.com/Angel-Hair/XUN_Bot)的插件)
- [x] 靠图识番  (使用[XUN_Langskip](https://github.com/Angel-Hair/XUN_Bot)的插件)
- [x] 以图搜图 (使用[nonebot_plugin_picsearcher](https://github.com/synodriver/nonebot_plugin_picsearcher)插件)
- [x] 搜番
- [x] 点歌  [nonebot_plugin_songpicker2](https://github.com/maxesisn/nonebot_plugin_songpicker2)插件（删除了选歌和评论）
- [x] epic免费游戏
- [x] p站排行榜
- [x] p站搜图
- [x] 翻译（日英韩）
- [x] pix图库（一个自己的图库，含有增删查改，黑名单等命令）

- [x] 查看当前群欢迎消息
- [x] 查看该群自己的权限
- [x] 我的信息（只是为了看看什么时候入群）
- [x] 更新信息（如果继续更新的话）
- [x] go-cqhttp最新版下载和上传（不需要请删除）
- [x] 撤回
- [x] 滴滴滴-（用户对超级用户发送消息）
- [x] 金币红包/金币排行
- [x] 俄罗斯轮盘/胜场排行/败场排行/欧洲人排行/慈善家排行
- [x] 网易云热评
- [x] 念首古诗
- [x] 获取b站视频封面
- [x] 通过PID获取图片
- [x] 功能统计可视化

- [x] 关于

### 已实现的管理员功能
- [x] 更新群组成员信息
- [x] 95%的群功能开关
- [x] 查看群内被动技能状态
- [x] 自定义群欢迎消息（是真寻的不是管家的！）
- [x] .ban/.unban（支持设置ban时长）= 黑白名单
- [x] 刷屏禁言相关：刷屏检测设置/设置禁言时长/设置检测次数
- [x] 上传图片/连续上传图片 （上传图片至指定图库）
- [x] 移动图片  （同上）
- [x] 删除图片  （同上）
- [x] 群内B站订阅
- [x] 群词条
- [x] 休息吧/醒来

### 已实现的超级用户功能
- [x] 添加/删除权限（是真寻的管理员权限，不是群管理员）
- [x] 开启/关闭指定群的广播通知
- [x] 广播
- [x] 自检（检查系统状态）
- [x] 所有群组/所有好友
- [x] 退出指定群
- [x] 更新好友信息/更新群信息
- [x] /t（对用户进行回复或发送消息）
- [x] 上传/删除/修改商品（需要编写对应的商品功能）
- [x] 节日红包发送
- [x] 修改群权限
- [x] ban
- [x] 更新色图
- [x] 更新价格/更加图片（csgo开箱）
- [x] 重载原神/方舟/赛马娘/坎公骑冠剑卡池
- [x] 更新原神今日素材/更新原神资源信息
- [x] PIX相关操作
- [x] 检查更新真寻
- [x] 重启
- [x] 添加/删除/查看群白名单
- [x] 功能开关(更多设置)
- [x] 功能状态
- [x] b了
- [x] 执行sql
- [x] 重载配置
- [x] 清理临时数据
- [x] 增删群认证
- [x] 同意/拒绝好友/群聊请求
- [x] 配置重载

#### 超级用户的被动技能
- [x] 邀请入群提醒(别人邀请真寻入群)
- [x] 添加好友提醒(别人添加真寻好友)

### 已实现的被动技能
- [x] 进群欢迎消息
- [x] 群早晚安
- [x] 每日开箱重置提醒
- [x] b站转发解析（解析b站分享信息，支持bv，bilibili链接，b站手机端转发卡片，cv，b23.tv），且5分钟内不解析相同url
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
- [x] 群管理员监控，自动为新晋管理员增加权限，为失去群管理员的用户删除权限
- [x] 群权限系统
- [x] 定时更新权限
- [x] 自动配置重载
</details>

## 详细配置请前往文档，以下为最简部署和配置，如果你有基础并学习过nonebot2的话


## 简单部署

```

# 配置gocq

在 https://github.com/Mrs4s/go-cqhttp 下载Releases最新版本，运行后选择反向代理，
  后将gocq的配置文件config.yml中的universal改为universal: ws://127.0.0.1:8080/onebot/v11/ws

# 获取代码
git clone https://github.com/HibiKier/zhenxun_bot.git

# 进入目录
cd zhenxun_bot

# 安装依赖
pip install poetry      # 安装 poetry
poetry install          # 安装依赖

# 进行基础配置
####请查看 配置 部分####

# 开始运行
poetry shell            # 进入虚拟环境
python bot.py
```

## 简单配置

```
1.在.env.dev文件中

  SUPERUSERS = [""]   # 填写你的QQ

2.在configs/config.py文件中
  * 数据库配置

3.在configs/config.yaml文件中 # 该文件需要启动一次后生成
  * 修改插件配置项

```


## 使用Docker
__Docker 最新版本由 [Sakuracio](https://github.com/Sakuracio) 提供__
#### GitHub：[Sakuracio/zxenv](https://github.com/Sakuracio/zxenv)
#### DockerHub：[hibikier/zhenxun_bot](https://hub.docker.com/r/hibikier/zhenxun_bot)



## 更新

### 2022/2/25 \[v0.1.4]

* PIX提供配置MAX_ONCE_NUM2FORWARD：当单次发送图片超过指定张数且在群聊时，将转为合并消息
* 优化抽卡
* 修复点歌无法正确发送
* 修复我有一个朋友有时文本会包含CQ码
* 修复群欢消息被动控制文本未删除 [@pull/124](https://github.com/HibiKier/zhenxun_bot/pull/124)
* message_builder.image不再提供参数：abspath

### 2022/2/23

* 插件状态将从已加载插件模块中读取
* 修复b站订阅插件订阅失败问题
* 修复重启命令无法使用

### 2022/2/21 \[v0.1.3.2]

* 群权限为-1时，超级用户发送的命令依旧生效
* 当群权限为-1时，被动技能也将不会发送
* 修复功能开关，b站转发解析，复读 ignore无法使用
* 修复色图下载文件名与路径错误
* 修复被动技能提醒有时无法删除控制文本


### 2022/2/20 \[v0.1.3.1]

* 修复pix下载临时文件目录错误
* 修复AI，天气，发送图片ignore导致无法使用
* 修复纯文本被动技能提醒有时无法删除控制文本

### 2022/2/19 \[v0.1.3] (nonebot beta2！)

* 由于nonebot升级版本，提供更新建议（__该次升级将会导致nonebot.beta1以下的插件无法使用__
  * 保证services，utils，configs，plugins，basic_plugins，文件夹均为最新
  * 根目录有pyproject.toml与poetry.lock
  * 执行命令：
    * pip3 install poetry
    * poetry install
    * poetry shell
    * playwright install chromium
    * python3 bot.py


* 适配nonebot.beta2
* 删除图片搜索 nonebot_plugin_picsearcher
* 新增图片搜索 search_image
* 替换cos api
* 原神签到树脂提醒新增绑定群里，在某群绑定uid就会在某群发送提醒信息（有好友则私聊，需要重新绑定uid
* 修改update_info.json
* 修复原神资源查询下载数据失败时导致报错
* 优化BuildImage.circle()锯齿问题 [@pull/109](https://github.com/HibiKier/zhenxun_bot/pull/109)
* epic restful 替换 [@pull/119](https://github.com/HibiKier/zhenxun_bot/pull/119)
* fix: 修复远古时期残留的epic推送问题 [@pull/122](https://github.com/HibiKier/zhenxun_bot/pull/122)

### 2021/2/11

* 修复pix不使用反代无法下载图片

### 2021/2/10 \[v0.1.1]

* 修复购买道具出错

### 2021/2/9 \[v0.1]

* 新增原神自动签到和手动签到
* 新增原神树脂提醒
* 新增手动重载Config.yaml命令以及重载配置定时任务（极少部分帮助或配置可能需要重启
* 修改了发送本地图库的matcher，改为on_message
* register_use可以通过返回值发送消息
* 修复修改商品时限制时间出错
* 修复超时商品依旧可以被购买

### 2021/1/16 \[v0.0.9.0]

* Ai提供文本敏感词过滤器
* 疫情插件适配新版腾讯API
* 修复/t回复带空格切分
* 修复原神玩家查询缺少渊下宫和稻妻家园以及角色不完全
* 修复方法 text2image 中 padding 和 font 无法对纯文本生效
* 修复签到图片中信息并未使用配置文件中的色图概率
* 修改原神大地图合成方式，改为先压缩再合成
* bag_user弃用字段props（该字段会在下次更新删除），使用新字段property
* 数据库中所有belonging_group统一修改为group_id
* 商店将registered_use和register_goods更名为register_use何register_goods
* 商品注册提供了kwargs参数提供：
    * bot 
    * event
    * 特殊字段
      * “send_success_msg”(发送成功的交互信息->即：使用道具 {name} {num} 次成功)
      * “_max_num_limit”(该道具单次使用的最多个数，默认1)

### 2021/1/5 \[v0.0.8.2]

* 提供金币消费hook，可在plugins2settings.yaml中配置该功能需要消费的金币
* 商店插件将作为内置插件移动至basic_plugins
* 商店插件通过export提供了方法，不需要修改商店插件代码添加商品数据和生效方法
* 修改了hook插件顺序，主要以auth_hook为主
* 修改商店图片样式
* 取消每次启动更新城市列表（首次除外），采用定时更新，加快bot启动速度
* 取消每次启动时截取今日素材，采用调用时截取保存，加快bot启动速度
* 更新色图时当图片404时会删除并替换
* 疫情消息回复改为图片
* 修复商店折扣和限时时间无法生效
* 修复原神玩家查询尘歌壶缺少图片

### 2021/12/26

* 修复群词条问题 空格 会被录入导致不断回复
* 修复米游社app替换api导致无法正常查询

### 2021/12/24

* 支持国际疫情数据查询 [@pull/99](https://github.com/HibiKier/zhenxun_bot/pull/99)

### 2021/12/20

* 只有发布小于存储时间的新动态/视频的时候才获取并推送 [@pull/96](https://github.com/HibiKier/zhenxun_bot/pull/96)

### 2021/12/16 \[v0.0.7.0]

* 提供了真寻群聊功能总开关和对应默认配置项，命令：休息吧 醒来
* 新增原神玩家查询，原神便笺查询
* 群功能管理提供全部开启/关闭命令：开启/关闭全部功能
* 提供主要数据自动备份，且提供自定义配置项
* 提供命令：关于，用于介绍Bot之类的
* 新增命令exec，用于执行sql语句
* 签到提供参数 "all"，用于签到所有群聊
* Ban提醒提供cd
* 本地图库提供配置项SHOW_ID，用于设置发送图片时是否显示id
* 色图和PIX提供配置项SHOW_INFO，用于设置发送图片时是否显示图片信息
* 所有被动技能提供了进群默认状态配置项
* 修复添加权限第二种添加形式无法正确添加正确的权限
* 修复签到获取好感度卡时金币不会增加
* 修复当红包数量不合法时依旧扣除金币
* 修复金币红包再次使用塞红包时无法正确退回上次未开完的金币
* 修复 滴滴滴- 只包含图片时不会发送至管理员
* 修复添加权限等级错误
* 修复群词条以bot名称为开头时无法正确触发
* 修改了权限插件加载顺序防止小概率优先加载权限插件引起报错
* 本地图库新图库会统一建立在resource/img/image_management文件夹下，如果该文件夹内未找到图库，会从上级目录查找（即：resource/img/）

<br>

__..... 更多更新信息请查看文档__


## Todo
- [ ] web管理

## 感谢
[botuniverse / onebot](https://github.com/botuniverse/onebot) ：超棒的机器人协议  
[Mrs4s / go-cqhttp](https://github.com/Mrs4s/go-cqhttp) ：cqhttp的golang实现，轻量、原生跨平台.  
[nonebot / nonebot2](https://github.com/nonebot/nonebot2) ：跨平台Python异步机器人框架  
[Angel-Hair / XUN_Bot](https://github.com/Angel-Hair/XUN_Bot) ：一个基于NoneBot和酷Q的功能性QQ机器人  
[pcrbot / cappuccilo_plugins](https://github.com/pcrbot/cappuccilo_plugins) ：hoshino插件合集  
[MeetWq /nonebot-plugin-withdraw](https://github.com/MeetWq/nonebot-plugin-withdraw) ：A simple withdraw plugin for Nonebot2  
[maxesisn / nonebot_plugin_songpicker2](https://github.com/maxesisn/nonebot_plugin_songpicker2) ：适用于nonebot2的点歌插件  
[nonepkg / nonebot-plugin-manager](https://github.com/nonepkg/nonebot-plugin-manager) ：Nonebot Plugin Manager base on import hook  
[H-K-Y / Genshin_Impact_bot](https://github.com/H-K-Y/Genshin_Impact_bot) ：原神bot，这是一个基于nonebot和HoshinoBot的原神娱乐及信息查询插件  
[NothAmor / nonebot2_luxun_says](https://github.com/NothAmor/nonebot2_luxun_says) ：基于nonebot2机器人框架的鲁迅说插件  
[Kyomotoi / AnimeThesaurus](https://github.com/Kyomotoi/AnimeThesaurus) ：一个~~特二刺螈~~（文爱）的适用于任何bot的词库  
[Ailitonia / omega-miya](https://github.com/Ailitonia/omega-miya) ：基于nonebot2的qq机器人  
[KimigaiiWuyi / GenshinUID]("https://github.com/KimigaiiWuyi/GenshinUID") ：一个基于HoshinoBot/NoneBot2的原神UID查询插件
