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

# Nonebot2
<img style="height: 200px;width: 200px;" src="https://camo.githubusercontent.com/0ef71e86056da694c540790aa4a4e314396884d6c4fdb95362a7538b27a1b034/68747470733a2f2f76322e6e6f6e65626f742e6465762f6c6f676f2e706e67">

非常 [ **[NICE](https://github.com/nonebot/nonebot2)** ] 的OneBot框架

## 未完成的文档

# [传送门](https://hibikier.github.io/zhenxun_bot/)

## 真寻的帮助
请对真寻说: '真寻帮助' or '管理员帮助' or '超级用户帮助' or '真寻帮助 指令'

## 普通帮助图片
![x](https://github.com/HibiKier/zhenxun_bot/blob/0.0.8.2/docs_image/3238573864-836268675-E2FFBB2AC143EAF4DDDF150438508721.png)

## Web UI
[zhenxun_bot_webui](https://github.com/HibiKier/zhenxun_bot_webui)

## 一键安装脚本
[zhenxun_bot-deploy](https://github.com/AkashiCoin/zhenxun_bot-deploy)

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
- [x] 词云
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
#### GitHub：[Sakuracio/zhenxun_bot_docker](https://github.com/Sakuracio/zhenxun_bot_docker)
#### DockerHub：[hibikier/zhenxun_bot](https://hub.docker.com/r/hibikier/zhenxun_bot)



## 更新

### 2022/6/9

* 修复b站订阅同群二人以上相同订阅时发送多次信息
* 修复超级用户帮助中缺少了 ‘插件商店’ 相关帮助
* 昵称系统提供了详细帮助

### 2022/6/5 \[v0.1.5.9]

* webui修复plugin2setting中cmd从list转变为str
* 当命令`我的金币`被风控时将以图片形式发送
* fix gold_redbag [@pull/763](https://github.com/HibiKier/zhenxun_bot/pull/763)
* 金币红包功能增加更多封面 [@pull/764](https://github.com/HibiKier/zhenxun_bot/pull/764)

### 2022/6/3

* 插件仓库在已安装插件边上会提示\[已安装]
* 修复ShopRegister kwargs某些字段无效
* 调整了一下查看所有请求中的年龄绘制 [@pull/745](https://github.com/HibiKier/zhenxun_bot/pull/745)
* 修复原神树脂提醒bug [@pull/756](https://github.com/HibiKier/zhenxun_bot/pull/756)

### 2022/5/31

* 修复开启/关闭全部功能时帮助图片未重绘 [@pull/721](https://github.com/HibiKier/zhenxun_bot/pull/721)
* bot_friend_group将group_handle.修改为friend_handle. [@pull/711](https://github.com/HibiKier/zhenxun_bot/pull/711)
* 修复发红包图片背景未透明化;修复原神树脂提醒参数错误 [@pull/712](https://github.com/HibiKier/zhenxun_bot/pull/712)
* 修复抽卡插件：方舟更新UP池信息时，若公告的第一个池子过期会导致无法更新UP池信息 [@pull/707](https://github.com/HibiKier/zhenxun_bot/pull/707)
* 商店插件判断是否有requirements.txt文件 [@pull/705](https://github.com/HibiKier/zhenxun_bot/pull/705)
* 删除原神玩家查询api返回变更的多余键值
* 优化了text2image方法

### 2022/5/29 \[v0.1.5.8]

* 提供了真寻适配仓库的插件 安装/卸载 操作
* 暂时关闭了插件资源清空
* 通过指令安装插件时会在插件目录下生成plugin_info.json记录当前插件信息

### 2022/5/28

* 修复私聊无法添加昵称
* 修复原神玩家查询层岩巨渊地下矿区没开时报错
* 修复 ```休息吧``` 无法阻断戳一戳
* 当图库无图片时，戳一戳将略过发送图片
* 新增搜图提供配置项```ALLOW_GROUP_R18```：允许在群聊中使用r18参数
* 新增自动更新插件```UPDATE_REMIND```：新版本提醒，原配置项```AUTO_UPDATE_ZHENXUN```改为自动更新升级
* black_word新增当群权限为-1时不再检测该群
* 修复非超级用户绑定原神cookie会被black_word阻拦
* 修复webui中plugins2setting修改时会改变plugins2setting.cmd为字符串
* 修复微博热搜报错,发红包小bug [@pull/688](https://github.com/HibiKier/zhenxun_bot/pull/688)
* 更多的中文提示

### 2022/5/26

* 修复\[滴滴滴]会被转义成&#91;滴滴滴&#93;导致无法触发的问题
* 将一些错误以中文提示输出
* 更新BT搜索源地址 [@pull/668](https://github.com/HibiKier/zhenxun_bot/pull/668)
* 更新抽卡插件 [@pull/667](https://github.com/HibiKier/zhenxun_bot/pull/667)

### 2022/5/25

* 修复webui中CountLimit字段limit_type类型错误
* 修改nickname插件：一处文案错误，添加敏感词 [@pull/624](https://github.com/HibiKier/zhenxun_bot/pull/624)
* gamedraw的ba卡池搬运了过来并且进行了真寻的适配 [@pull/617](https://github.com/HibiKier/zhenxun_bot/pull/617)
* feat: stream downloading and progress [@pull/607](https://github.com/HibiKier/zhenxun_bot/pull/607)
* 修改翻译插件，添加缺失的冒号 [@pull/602](https://github.com/HibiKier/zhenxun_bot/pull/602)
* 修复碧蓝航线/明日方舟up池解析出错的问题 [@pull/610](https://github.com/HibiKier/zhenxun_bot/pull/602)

### 2022/5/24

* fix: 修正了签到时日期时间的显示不补齐零的bug （符合日期时间表示法 ISO 8601）[@pull/600](https://github.com/HibiKier/zhenxun_bot/pull/600)
* 更新"微博热搜"接口 [@pull/579](https://github.com/HibiKier/zhenxun_bot/pull/579)
* refactor&fix(manager): modify argument [@pull/576](https://github.com/HibiKier/zhenxun_bot/pull/576)
* 修复复读不能复读图片的问题 [@pull/573](https://github.com/HibiKier/zhenxun_bot/pull/573)
* 修复抽卡插件：方舟抽卡的抽取和显示问题 [@pull/581](https://github.com/HibiKier/zhenxun_bot/pull/581)

### 2022/5/23 \[v0.1.5.6]

* 修复"清除已删除插件数据" [@pull/545](https://github.com/HibiKier/zhenxun_bot/pull/545)
* 修复有置顶的up主B站动态获取失败 [@pull/552](https://github.com/HibiKier/zhenxun_bot/pull/552)
* 添加pixiv搜图多关键词支持;修复p站搜图数量参数问题 [@pull/441](https://github.com/HibiKier/zhenxun_bot/pull/441)
* 修复开箱更新价格错误传参
* 修复pix无法正确查询uid
* 新增色图插件添加配置项```ALLOW_GROUP_R18```：允许群聊中使用色图r
* 新增PIX插件添加配置项```ALLOW_GROUP_SETU```：允许非超级用户使用-s参数
* 新增PIX插件添加配置项```ALLOW_GROUP_R18```：允许非超级用户使用-r参数

### 2022/5/22 \[v0.1.5.4]

* 使用action自动更新poetry.lock [@pull/515](https://github.com/HibiKier/zhenxun_bot/pull/515)
* fix(bilibili_sub): card is None and timeout [@pull/516](https://github.com/HibiKier/zhenxun_bot/pull/516)
* 修复了epic有时获取新免费游戏消息时获取不到图片
* 修复好感度满时签到出错（虽然是不可能满的
* 修复原神资源图标下载路径错误
* 修复自动更新群组可能失败

### 2022/5/21

* 修复搜番无结果时报错无正确反馈
* 解锁了windows上无法使用playwright的限制
* 修复p搜对应pid有多张图时出错，改为连续发送图片
* 修复p搜对数字的错误判断
* 修复添加商品折扣无法正确添加
* 修复了bilibili订阅直播间订阅up名称不一致的问题
* 修复原神玩家查询没开地图时报错
* 最低priority修改为 999
* 修复刷屏检测失效
* 修复刷屏检测设置命令无法生效
* 优化刷屏显示设置禁言时长显示，并改为分钟
* 修复了多连开箱无法指定武器箱
* 修复识番链接无法正确获取
* 新增真寻入群时即刻刷新权限
* 提高了微博热搜截图的等待时间

### 2022/5/19

* fix: mihoyo bbs api changed [@pull/357](https://github.com/HibiKier/zhenxun_bot/pull/357)
* Add word_clouds [@pull/265](https://github.com/HibiKier/zhenxun_bot/pull/265)
* Fix wrong live streamer name [@pull/284](https://github.com/HibiKier/zhenxun_bot/pull/284)

### 2022/5/16

* 词条支持图片和@问题 [@pull/160](https://github.com/HibiKier/zhenxun_bot/pull/160)

### 2022/5/15

* 修复了商店商品无法正确添加
* 修复了多张色图无法正确发送

### 2022/5/14

* 修复B站动态生成失败的问题 [@pull/159](https://github.com/HibiKier/zhenxun_bot/pull/159)

### 2022/5/11

* fix: 更改p搜api，解决p搜无法使用的问题 [@pull/155](https://github.com/HibiKier/zhenxun_bot/pull/155)

### 2022/5/9 \[v0.1.5.3]

* 替换了疫情API
* 修复了私聊.ban/.unban出错

### 2022/5/5

* 修改bilibili_sub插件在windows平台下报错 [@pull/153](https://github.com/HibiKier/zhenxun_bot/pull/153)

### 2022/5/3 \[v0.1.5.2]

* 商品使用函数可以添加特定参数，例如：user_id, group_id, ShopParam等以及自己提供的参数
* 添加商品注册装饰器shop_register
* 修复商品函数kwargs无法获取参数值


### 2022/5/1

* 删除了`group_last_chat`插件（该功能可由`chat_history`替代
* 新增敏感词检测（全新反击系统，是时候重拳出击了

### 2022/4/26

* 修复了群白名单无法正确添加
* 优化了管理员帮助图片，背景图层将位于最下层
* 修复了树脂140时不断提醒（未测试
* 新增了消息记录的消息排行
* WebUI新增CPU，内存，磁盘监控
* WebUI新增资源文件夹统计可视化

### 2022/4/12

* 修复b了命令私聊出错

### 2022/4/10 \[v0.1.4.7]

* 新增消息记录模块
* 丰富处理请求操作提示
* web ui新增配置项修改

### 2022/4/9

* fix: 更新问题，戳一戳图片路径问题 [@pull/144](https://github.com/HibiKier/zhenxun_bot/pull/144)

### 2022/4/8

* 修复原神玩家查询

### 2022/4/6

* update search_type [@pull/143](https://github.com/HibiKier/zhenxun_bot/pull/143)

### 2022/4/5 \[v0.1.4.6]

* 修复web修改插件后帮助图片生成错误

### 2022/4/4 \[v0.1.4.5]

* 替换了bt搜索URL
* 优化使用playwright的相关代码
* 原神玩家查询新增层岩巨渊探索
* 修复原神便笺角色头像黑框
* 修复同意群聊请求错误
* 提供webui方面的api
* 新增web-ui（前端简易管理页面插件）插件

### 2022/3/21

* 修复statistics_handle.py乱码

### 2022/3/18 \[v0.1.4.4]

* 修复戳一戳无法功能关闭与ban禁用
* 新增图片搜索 search_image

### 2022/3/7

* 优化增删权限插件

### 2022/3/6

* 修复树脂提醒无法开启
* 修复p搜图片路径错误

### 2022/3/3 \[v0.1.4.3]

* 修复手动同意群聊请求依旧退出

### 2022/3/1 \[v0.1.4.2]

* 0.1.4内容

### 2022/2/27 \[v0.1.4.1]

* 优化抽卡

### 2022/2/25 \[v0.1.4]

* PIX提供配置MAX_ONCE_NUM2FORWARD：当单次发送图片超过指定张数且在群聊时，将转为合并消息
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
* 替换cos api
* 原神签到树脂提醒新增绑定群里，在某群绑定uid就会在某群发送提醒信息（有好友则私聊，需要重新绑定uid
* 修改update_info.json
* 修复原神资源查询下载数据失败时导致报错
* 优化BuildImage.circle()锯齿问题 [@pull/109](https://github.com/HibiKier/zhenxun_bot/pull/109)
* epic restful 替换 [@pull/119](https://github.com/HibiKier/zhenxun_bot/pull/119)
* fix: 修复远古时期残留的epic推送问题 [@pull/122](https://github.com/HibiKier/zhenxun_bot/pull/122)

### 2022/2/11

* 修复pix不使用反代无法下载图片

### 2022/2/10 \[v0.1.1]

* 修复购买道具出错

### 2022/2/9 \[v0.1]

* 新增原神自动签到和手动签到
* 新增原神树脂提醒
* 新增手动重载Config.yaml命令以及重载配置定时任务（极少部分帮助或配置可能需要重启
* 修改了发送本地图库的matcher，改为on_message
* register_use可以通过返回值发送消息
* 修复修改商品时限制时间出错
* 修复超时商品依旧可以被购买

### 2022/1/16 \[v0.0.9.0]

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

### 2022/1/5 \[v0.0.8.2]

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
[KimigaiiWuyi / GenshinUID](https://github.com/KimigaiiWuyi/GenshinUID) ：一个基于HoshinoBot/NoneBot2的原神UID查询插件
