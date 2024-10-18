<div align=center>

<img width="250" height="312" src="https://github.com/HibiKier/zhenxun_bot/blob/main/docs_image/tt.jpg"/>

</div>

<div align=center>

![python](https://img.shields.io/badge/python-v3.9%2B-blue)
![nonebot](https://img.shields.io/badge/nonebot-v2.1.3-yellow)
![onebot](https://img.shields.io/badge/onebot-v11-black)

</div>

<div align=center>

[![license](https://img.shields.io/badge/license-AGPL3.0-FE7D37)](https://github.com/HibiKier/zhenxun_bot/blob/main/LICENSE)
[![tencent-qq](https://img.shields.io/badge/%E7%BE%A4-是真寻酱哒-red?style=logo=tencent-qq)](https://jq.qq.com/?_wv=1027&k=u8PgBkMZ)
[![tencent-qq](https://img.shields.io/badge/%E7%BE%A4-真寻的技术群-c73e7e?style=logo=tencent-qq)](https://qm.qq.com/q/YYYt5rkMYc)

</div>

<div align=center>

[文档](https://hibikier.github.io/zhenxun_bot/)

</div>

<div align=center>

## 绪山真寻 Bot

</div>

<div align=center>

“真寻是<strong>[椛椛](https://github.com/FloatTech/ZeroBot-Plugin)</strong>的好朋友！”

:tada:喜欢真寻，于是真寻就来了！:tada:

本项目符合 [OneBot](https://github.com/howmanybots/onebot) 标准，可基于以下项目与机器人框架/平台进行交互

|                           项目地址                            | 平台 |         核心作者         | 备注 |
| :-----------------------------------------------------------: | :--: | :----------------------: | :--: |
|       [LLOneBot](https://github.com/LLOneBot/LLOneBot)        | NTQQ |        linyuchen         | 可用 |
|         [Napcat](https://github.com/NapNeko/NapCatQQ)         | NTQQ |         NapNeko          | 可用 |
| [Lagrange.Core](https://github.com/LagrangeDev/Lagrange.Core) | NTQQ | LagrangeDev/Linwenxuan04 | 可用 |

</div>

<div align=center>

![Star Trend](https://api.star-history.com/svg?repos=HibiKier/zhenxun_bot&type=Timeline)

</div>

## 真寻觉得你需要帮助

<div align=center>

<img width="350" height="350" src="https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs_image/help.png"/>
<img width="250" height="500" src="https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs_image/html_help.png"/>
<img width="180" height="450" src="https://github.com/HibiKier/zhenxun_bot/blob/dev/docs_image/zhenxun_help.png"/>

</div>

## 这是一份扩展

### 1. 体验一下？

这是一个免费的，版本为 dev 的 zhenxun，你可以通过 napcat 或拉格朗日等直接连接用于体验与测试  
（球球了测试君！）

```
Url： 43.143.112.57:11451/onebot/v11/ws
AccessToken: PUBLIC_ZHENXUN_TEST

注：你无法获得超级用户权限
```

### 2. 额外扩展

<div align=center>
  
“不要害怕，你的背后还有千千万万的 <strong>伙伴</strong> 啊！”

|                                项目名称                                | 主要用途 |                      仓库作者                       |             备注              |
| :--------------------------------------------------------------------: | :------: | :-------------------------------------------------: | :---------------------------: |
|      [插件库](https://github.com/zhenxun-org/zhenxun_bot_plugins)      |   插件   |    [zhenxun-org](https://github.com/zhenxun-org)    |     原 plugins 文件夹插件     |
| [插件索引库](https://github.com/zhenxun-org/zhenxun_bot_plugins_index) |   插件   |    [zhenxun-org](https://github.com/zhenxun-org)    |        扩展插件索引库         |
|    [一键安装](https://github.com/soloxiaoye2022/zhenxun_bot-deploy)    |   安装   | [soloxiaoye2022](https://github.com/soloxiaoye2022) |            第三方             |
|         [WebUi](https://github.com/HibiKier/zhenxun_bot_webui)         |   管理   |       [hibikier](https://github.com/HibiKier)       | 基于真寻 WebApi 的 webui 实现 |
|  [安卓 app(WebUi)](https://github.com/YuS1aN/zhenxun_bot_android_ui)   |   安装   |         [YuS1aN](https://github.com/YuS1aN)         |            第三方             |

<details>
<summary> <strong> WebUI </strong>后台示例图 </summary>

![x](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs_image/webui1.png)
![x](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs_image/webui2.png)
![x](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs_image/webui3.png)
![x](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs_image/webui4.png)
![x](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs_image/webui5.png)
![x](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs_image/webui6.png)
![x](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs_image/webui7.png)

</details>

<br/>

</div>

## ~~来点优点？~~ 可爱难道还不够吗

- 实现了许多功能，且提供了大量功能管理命令
- 通过 Config 配置项将所有插件配置统计保存至 config.yaml，利于统一用户修改
- 方便增删插件，原生 nonebot2 matcher，不需要额外修改，仅仅通过简单的配置属性就可以生成`帮助图片`和`帮助信息`
- 提供了 cd，阻塞，每日次数等限制，仅仅通过简单的属性就可以生成一个限制，例如：`PluginCdBlock` 等
- **..... 更多详细请通过[[传送门](https://hibikier.github.io/zhenxun_bot/)]查看文档！**

## 简单部署

```
# 获取代码
git clone https://github.com/HibiKier/zhenxun_bot.git

# 进入目录
cd zhenxun_bot

# 安装依赖
pip install poetry      # 安装 poetry
poetry install          # 安装依赖

# 开始运行
poetry shell            # 进入虚拟环境
python bot.py

# 首次后会在data目录下生成config.yaml文件
# config.yaml用户配置插件
```

## 简单配置

```
1.在.env.dev文件中

  SUPERUSERS = [""]   # 填写你的QQ

  PLATFORM_SUPERUSERS = '
  {
    "qq": [""],   # 在此处填写你的qq
    "dodo": [],
    "kaiheila": [],
    "discord": []
  }
  '
  # 此处填写你的数据库地址
  # 示例: "postgres://user:password@127.0.0.1:5432/database"
  # 示例: "mysql://user:password@127.0.0.1:5432/database"
  # 示例: "sqlite:data/db/zhenxun.db"   在data目录下建立db文件夹
  DB_URL = ""   # 数据库地址


2.在configs/config.yaml文件中 # 该文件需要启动一次后生成
  * 修改插件配置项

```

<!-- ## 功能列表 （旧版列表）

<details>
<summary>已实现的功能</summary>

### 已实现的常用功能

- [x] 昵称系统（群与群与私聊分开.）

- [x] 图灵 AI（会把'你'等关键字替换为你的昵称），且带有 [AnimeThesaurus](https://github.com/Kyomotoi/AnimeThesaurus)，够味
- [x] 签到/我的签到/好感度排行/好感度总排行（影响色图概率和开箱次数，支持配置）
- [x] 发送某文件夹下的随机图片（支持自定义，默认：美图，萝莉，壁纸）
- [x] 色图（这不是基础功能嘛喂）
- [x] coser
- [x] 黑白草图生成器
- [x] 鸡汤/语录
- [x] 骂我（钉宫语音）
- [x] 戳一戳（概率发送美图，钉宫语音或者戳回去）
- [x] 模拟开箱/我的开箱/群开箱统计/我的金色/设置 cookie（csgo，内置爬虫脚本，需要提前抓取数据和图片，需要 session，可能需要代理，阿里云服务器等 ip 也许已经被 ban 了（我无代理访问失败），如果访问太多账号 API 调用可能被禁止访问 api！）
- [x] 鲁迅说过
- [x] 构造假消息（自定义的分享链接）
- [x] 商店/我的金币/购买道具/使用道具
- [x] 8 种手游抽卡 (查看 [nonebot_plugin_gamedraw](https://github.com/HibiKier/nonebot_plugin_gamedraw))
- [x] 我有一个朋友想问问..（借鉴 pcrbot 插件）
- [x] 原神黄历
- [x] 原神今日素材
- [x] 原神资源查询 (借鉴[Genshin_Impact_bot](https://github.com/H-K-Y/Genshin_Impact_bot)插件)
- [x] 原神便笺查询
- [x] 原神玩家查询
- [x] 原神树脂提醒
- [x] 原神签到/自动签到
- [x] 金币红包
- [x] 微博热搜
- [x] B 站主播/UP/番剧订阅

- [x] pil 对图片的一些操作
- [x] BUFF 饰品底价查询（需要 session）
- [x] 天气查询
- [x] 疫情查询
- [x] bt 磁力搜索（咳咳，这功能我想 dddd）
- [x] reimu 搜索（上车） (使用[XUN_Langskip](https://github.com/Angel-Hair/XUN_Bot)的插件)
- [x] 靠图识番 (使用[XUN_Langskip](https://github.com/Angel-Hair/XUN_Bot)的插件)
- [x] 以图搜图 (使用[nonebot_plugin_picsearcher](https://github.com/synodriver/nonebot_plugin_picsearcher)插件)
- [x] 搜番
- [x] 点歌 [nonebot_plugin_songpicker2](https://github.com/maxesisn/nonebot_plugin_songpicker2)插件（删除了选歌和评论）
- [x] epic 免费游戏
- [x] p 站排行榜
- [x] p 站搜图
- [x] 翻译（日英韩）
- [x] pix 图库（一个自己的图库，含有增删查改，黑名单等命令）

- [x] 查看当前群欢迎消息
- [x] 查看该群自己的权限
- [x] 我的信息（只是为了看看什么时候入群）
- [x] 更新信息（如果继续更新的话）
- [x] go-cqhttp 最新版下载和上传（不需要请删除）
- [x] 撤回
- [x] 滴滴滴-（用户对超级用户发送消息）
- [x] 金币红包/金币排行
- [x] 俄罗斯轮盘/胜场排行/败场排行/欧洲人排行/慈善家排行
- [x] 网易云热评
- [x] 念首古诗
- [x] 获取 b 站视频封面
- [x] 通过 PID 获取图片
- [x] 功能统计可视化
- [x] 词云
- [x] 关于

### 已实现的管理员功能

- [x] 更新群组成员信息

- [x] 95%的群功能开关
- [x] 查看群内被动技能状态
- [x] 自定义群欢迎消息（是真寻的不是管家的！）
- [x] .ban/.unban（支持设置 ban 时长）= 黑白名单
- [x] 刷屏禁言相关：刷屏检测设置/设置禁言时长/设置检测次数
- [x] 上传图片/连续上传图片 （上传图片至指定图库）
- [x] 移动图片 （同上）
- [x] 删除图片 （同上）
- [x] 群内 B 站订阅
- [x] 词条设置
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
- [x] 更新价格/更加图片（csgo 开箱）
- [x] 重载原神/方舟/赛马娘/坎公骑冠剑卡池
- [x] 更新原神今日素材/更新原神资源信息
- [x] PIX 相关操作
- [x] 检查更新真寻
- [x] 重启
- [x] 添加/删除/查看群白名单
- [x] 功能开关(更多设置)
- [x] 功能状态
- [x] b 了
- [x] 执行 sql
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
- [x] b 站转发解析（解析 b 站分享信息，支持 bv，bilibili 链接，b 站手机端转发卡片，cv，b23.tv），且 5 分钟内不解析相同 url
- [x] 丢人爬（爬表情包）
- [x] epic 通知（每日发送 epic 免费游戏链接）
- [x] 原神黄历提醒
- [x] 复读

### 已实现的看不见的技能

- [x] 刷屏禁言检测

- [x] 功能调用统计
- [x] 检测恶意触发命令（将被最高权限 ban 掉 30 分钟，只有最高权限(9 级)可以进行 unban）
- [x] 自动同意好友请求，加群请求将会提醒管理员，退群提示，加群欢迎等等
- [x] 群聊时间检测（当群聊最后一人发言时间大于当前 36 小时后将关闭该群所有通知（即被动技能））
- [x] 群管理员监控，自动为新晋管理员增加权限，为失去群管理员的用户删除权限
- [x] 群权限系统
- [x] 定时更新权限
- [x] 自动配置重载

</details> -->

## [爱发电](https://afdian.net/@HibiKier)

<details>
<summary>爱发电 以及 感谢投喂 </summary>
<img width="365px" height="450px" src="https://user-images.githubusercontent.com/45528451/175059389-cfeb8174-fa07-4939-80ab-a039087a50f6.png">

### 感谢名单

(可以告诉我你的 **github** 地址，我偷偷换掉 0v|)

[shenqi](https://afdian.net/u/fa923a8cfe3d11eba61752540025c377)
[A_Kyuu](https://afdian.net/u/b83954fc2c1211eba9eb52540025c377)
[疯狂混沌](https://afdian.net/u/789a2f9200cd11edb38352540025c377)
[投冥](https://afdian.net/a/144514mm)
[茶喵](https://afdian.net/u/fd22382eac4d11ecbfc652540025c377)
[AemokpaTNR](https://afdian.net/u/1169bb8c8a9611edb0c152540025c377)
[爱发电用户\_wrxn](https://afdian.net/u/4aa03d20db4311ecb1e752540025c377)
[qqw](https://afdian.net/u/b71db4e2cc3e11ebb76652540025c377)
[溫一壺月光下酒](https://afdian.net/u/ad667a5c650c11ed89bf52540025c377)  
[伝木](https://afdian.net/u/246b80683f9511edba7552540025c377)  
[阿奎](https://afdian.net/u/da41f72845d511ed930d52540025c377)  
[醉梦尘逸](https://afdian.net/u/bc11d2683cd011ed99b552540025c377)  
[Abc](https://afdian.net/u/870dc10a3cd311ed828852540025c377)  
[本喵无敌哒](https://afdian.net/u/dffaa9005bc911ebb69b52540025c377)  
[椎名冬羽](https://afdian.net/u/ca1ebd64395e11ed81b452540025c377)  
[kaito](https://afdian.net/u/a055e20a498811eab1f052540025c377)  
[笑柒 XIAO_Q7](https://afdian.net/u/4696db5c529111ec84ea52540025c377)  
[请问一份爱多少钱](https://afdian.net/u/f57ef6602dbd11ed977f52540025c377)  
[咸鱼鱼鱼鱼](https://afdian.net/u/8e39b9a400e011ed9f4a52540025c377)  
[Kafka](https://afdian.net/u/41d66798ef6911ecbc5952540025c377)  
[墨然](https://afdian.net/u/8aa5874a644d11eb8a6752540025c377)
[爱发电用户\_T9e4](https://afdian.net/u/2ad1bb82f3a711eca22852540025c377)  
[笑柒 XIAO_Q7](https://afdian.net/u/4696db5c529111ec84ea52540025c377)  
[noahzark](https://afdian.net/a/noahzark)  
[腊条](https://afdian.net/u/f739c4d69eca11eba94b52540025c377)  
[ze roller](https://afdian.net/u/0e599e96257211ed805152540025c377)  
[爱发电用户\_4jrf](https://afdian.net/u/6b2cdcc817c611ed949152540025c377)  
[爱发电用户\_TBsd](https://afdian.net/u/db638b60217911ed9efd52540025c377)  
[烟寒若雨](https://afdian.net/u/067bd2161eec11eda62b52540025c377)  
[ln](https://afdian.net/u/b51914ba1c6611ed8a4e52540025c377)  
[爱发电用户\_b9S4](https://afdian.net/u/3d8f30581a2911edba6d52540025c377)  
[爱发电用户\_c58s](https://afdian.net/u/a6ad8dda195e11ed9a4152540025c377)  
[爱发电用户\_eNr9](https://afdian.net/u/05fdb41c0c9a11ed814952540025c377)
[MangataAkihi](https://github.com/Sakuracio)
[炀](https://afdian.net/u/69b76e9ec77b11ec874f52540025c377)
[爱发电用户\_Bc6j](https://afdian.net/u/8546be24f44111eca64052540025c377)  
[大魔王](https://github.com/xipesoy)
[CopilotLaLaLa](https://github.com/CopilotLaLaLa)  
[嘿小欧](https://afdian.net/u/daa4bec4f24911ec82e552540025c377)
[回忆的秋千](https://afdian.net/u/e315d9c6f14f11ecbeef52540025c377)  
[十年くん](https://github.com/shinianj)
[哇](https://afdian.net/u/9b266244f23911eca19052540025c377)  
[yajiwa](https://github.com/yajiwa)  
[爆金币](https://afdian.net/u/0d78879ef23711ecb22452540025c377)

</details>

<!-- ## 更新

### 2024/8/11

- 更新 dev -->

<!-- ### 2024/1/25

* 重构webui

### 2023/12/28

* 修复B站动态获取失败的时候，会发送空消息

### 2023/9/6

* 修正b站订阅

### 2023/8/28

* 重构`红包`功能， 允许一个群聊中有多个用户发起的红包，发送`开`等命令会开启群中所有条件允许的红包，新增`红包结算排行`，在红包退回或抢完时统计，在`塞红包`时at可以发送专属红包
* 开箱添加`更新武器箱图片`超级用户命令，用于导入数据表后更新图片

### 2023/8/20

* 修复词条回答包含at时使用模糊|正则等问时无法正确匹配问题
* 修复开箱时最后开箱日期数据未更新

### 2023/8/7

* 添加 本地图库插件 防吞图特性 [@pull/1468](https://github.com/HibiKier/zhenxun_bot/pull/1468)

### 2023/5/28

* 修复群聊数据无法初始化

### 2023/5/24

* 轮盘结算信息使用图片发送

### 2023/5/23

* 修复群聊数据无法初始化
* 修复修改图库配置重载后上传图片时提示的图库与配置不符

### 2023/5/22

* 群聊中B站订阅所有管理员共享增删操作
* 数据库中所有user_qq改名以及user_id和group_id改为字符串
* 修改查看词条图片等显示问题

### 2023/5/16

* 修复因明日方舟新增“中坚寻访”导致抽卡模拟不可用的问题 [@pull/1418](https://github.com/HibiKier/zhenxun_bot/pull/1418)

### 2023/4/16

* 修复开箱更新未登录时没有停止更新
* 修复更新色图问题
* fix bug [@pull/1368](https://github.com/HibiKier/zhenxun_bot/pull/1368)
* `BilibiliSub`的部分字段改为字符串

### 2023/4/5

* 词条正则回答中允许使用$1.$2..来获取()捕获组

### 2023/4/3

* 修复帮助命令`-super`无效

### 2023/4/1

* 修复开箱偶尔出现`未抽取到任何皮肤`
* 修改优化开箱显示图片

### 2023/3/28

* 补全注释`SCRIPT`中的sql语句
* 罕见物品更新时会收录所有包含该物品的箱子，可以通过`更新皮肤ALL1 -S`强制更新所有罕见物品所属箱子

### 2023/3/27

* 优化开箱更新

### 2023/3/25

* 删除BUFF_SKIN表约束，新增`skin_id`字段
* 开箱新增更新指定刀具皮肤命令(某些箱子金色无法通过api获取)
* 修复词条At时bug与模糊查询时无法替换占位符问题

### 2023/3/20

* 修复BuildImage类text居中类型bug [@pull/1301](https://github.com/HibiKier/zhenxun_bot/pull/1317)
* 修复原神今日素材有时发不出图片的问题 [@pull/1301](https://github.com/HibiKier/zhenxun_bot/pull/1317)
* 修复首次签到时使用道具后签到报错
* 修复词条添加错误

### 2023/3/19

* 优化代码
* 查看武器箱及皮肤添加更新次数
* 修复添加群认证会检测群聊是否存在
* 修复色图r连发时未检测当前会话是否为群聊

### 2023/3/18

* 修复色图重复发送相同图片
* 修复签到好感度进度条错误

### 2023/3/12 \[v0.1.6.7]

* 新增`更新武器箱ALL`命令来更新所有武器箱
* 新增`查看武器箱`命令
* 色图bug修复、增加指令 [@pull/1301](https://github.com/HibiKier/zhenxun_bot/pull/1301)

### 2023/3/9

* 更正sql语句 [@pull/1302](https://github.com/HibiKier/zhenxun_bot/pull/1302)
* 修改签到卡片中签到增加好感度显示错误 [@pull/1299](https://github.com/HibiKier/zhenxun_bot/pull/1299)

### 2023/3/5

* 更新开箱会记录箱子数据以及开箱时箱子价格加入花费
* 修复开箱BUG

### 2023/3/4

* 重写翻译，使用百度翻译API
* 新增开箱日志以及自动更新武器箱

### 2023/3/2

* 修复config.yaml中把False也当成None的问题 [@pull/1288](https://github.com/HibiKier/zhenxun_bot/pull/1288)
* 删除道具表无用字段(props) [@pull/1287](https://github.com/HibiKier/zhenxun_bot/pull/1287)
* 修复词云
* 修复我的签到签到图片
* 更正BuffSkin添加语句
* 修复词条单图片/表情/at无法添加

### 2022/3/1

* 重写开箱更新箱子，允许更新目前所有箱子的皮肤
* 修复消息统计

### 2023/2/28

* 把Config的type字段默认类型由str改为None [@pull/1283](https://github.com/HibiKier/zhenxun_bot/pull/1283)
* 修复同意群聊请求以及添加群认证 更新变成查询的问题 [@pull/1282](https://github.com/HibiKier/zhenxun_bot/pull/1282)

### 2023/2/26

* Config提供`type`字段确定配置项类型
* 重写开箱功能

### 2023/2/25

* 修复ys查询，尘歌壶背景尺寸与内容不匹配的问题 [@pull/1270](https://github.com/HibiKier/zhenxun_bot/pull/1275)
* 更换cos url [@pull/1270](https://github.com/HibiKier/zhenxun_bot/pull/1274)

### 2023/2/20

* chat_history部分字段调整为可null [@pull/1270](https://github.com/HibiKier/zhenxun_bot/pull/1270)

### 2023/2/19

* 修正了`重载插件`的帮助提示
* 修改BUG

### 2023/2/18

* 数据库舍弃`gino`使用`tortoise`
* 昵称提供命令`全局昵称设置`
* `manager_group`群管理操作中`退群`，`修改群权限`，`添加/删除群白名单`，`添加/删除群认证`在群聊中使用命令时且未指定群聊时，默认指定当前群聊
* 修复插件帮助命令不生效的问题 [@pull/1263](https://github.com/HibiKier/zhenxun_bot/pull/1263)
* 解决开红包经常误触的问题，有红包和未领取的时候才会触发“开”命令 [@pull/1257](https://github.com/HibiKier/zhenxun_bot/pull/1257)
* 细节优化，原神今日素材重写 [@pull/1258](https://github.com/HibiKier/zhenxun_bot/pull/1258)

### 2023/1/31

* 修复B站转发卡片BUG [@pull/1249](https://github.com/HibiKier/zhenxun_bot/pull/1249)

### 2023/1/27

* 替换pixiv反向代理地址 [@pull/1244](https://github.com/HibiKier/zhenxun_bot/pull/1244)

### 2022/12/31

* 修复epic报错，优化简介 [@pull/1226](https://github.com/HibiKier/zhenxun_bot/pull/1226)
* 修复词条在某些回答下出错
* 原神黄历改为PIL
* 允许真寻自身触发命令，提供配置项 `self_message:STATUS`

### 2022/12/27 \[v0.1.6.6]

* 添加权限检查依赖注入

### 2022/12/26

* 优化`gamedraw`插件
* 提供全局被动控制
* 群被动状态改为图片
* 修复epic获取到的简介不是中文的bug [@pull/1221](https://github.com/HibiKier/zhenxun_bot/pull/1221)

## 2022/12/24

* 修复群管理员权限检测会阻挡超级用户权限

### 2022/12/23

* 优化`管理员帮助`，`超级用户帮助`图片
* 重新移植`gamedraw`
* 修复pil帮助私聊时无法生成

### 2022/12/17

* 修复查看插件仓库当已安装插件版本不一致时出错

### 2022/12/15

* 修复自定义群欢迎消息无法使用

### 2022/12/13

* 修复.unban

### 2022/12/12

* 修改HTML帮助禁用提示文本错误
* 修复HTML帮助私聊无法生成

### 2022/12/11

* 词条问题支持真寻的昵称开头与at真寻开头并优化回复
* 帮助新增HTML生成（新布局），添加配置`TYPE`切换
* 更正私聊时功能管理回复错误
* 修复加入新群聊时初始化功能开关错误
* 添加单例注解
* 添加统计表

### 2022/12/10

* 重写帮助，删除 `详细帮助` 命令

### 2022/12/4

* 优化管理代码

### 2022/11/28

* 修复web_ui群组无法获取
* 修复web_ui修改插件数据时cmd格式错误

### 2022/11/28

* :bug: Fix a bug in open_cases to get vanilla knives' prices [@pull/1188](https://github.com/HibiKier/zhenxun_bot/pull/1188)

### 2022/11/24

* 修复管理员插件加载路径错误

### 2022/11/23

* 修复webui插件无法获取修改

### 2022/11/22

* fix switch_rule [@pull/1185](https://github.com/HibiKier/zhenxun_bot/pull/1185)

### 2022/11/21  \[v0.1.6.5]

* 优化manager, hook代码
* 修复pid搜图 [@pull/1180](https://github.com/HibiKier/zhenxun_bot/pull/1180)

### 2022/11/19

* 修改优化帮助图片生成逻辑

### 2022/11/18

* poetry添加适配器依赖，更新支持py3.10 [@pull/1176](https://github.com/HibiKier/zhenxun_bot/pull/1176)

### 2022/11/13

* 更新天气api
* 使用道具可以附带额外信息供函数使用
* 限制帮助图片最小宽度

### 2022/11/12

* 更新yiqing插件数据显示 [@pull/1168](https://github.com/HibiKier/zhenxun_bot/pull/1168)

### 2022/11/11

* fix: B站直播订阅的相关问题 [@pull/1158](https://github.com/HibiKier/zhenxun_bot/pull/1158)

### 2022/10/30

* 商店简介动态行数，根据文字长度自动换行

### 2022/10/28

* 为exec指令进行了SELECT语句适配,添加了查看所有表指令 [@pull/1155](https://github.com/HibiKier/zhenxun_bot/pull/1155)
* 修复复读 [@pull/1154](https://github.com/HibiKier/zhenxun_bot/pull/1154)

### 2022/10/23

* 复读修改回图片下载

### 2022/10/22

* 更新依赖注入

### 2022/10/16 \[v0.1.6.4]

* 修改商店道具icon可以为空

### 2022/10/15

* nonebot2版本更新为rc1
* 我的道具改为图片形式
* 商品添加图标与是否为被动道具（被动道具无法被主动使用）
* 商品添加使用前方法和使用后方法（类似hook），使用方法具体查看文档或签到商品文件中注册的例子
* 新增用户使用道具，花费金币(包括插件)及用途记录
* 更细致的金币使用依赖注入
* 更多的依赖注入（包含图片获取等等..
* 修复我的道具仅有被动或主动道具时图片显示错误
* 色图插件p站反向代理失效 [@pull/1139](https://github.com/HibiKier/zhenxun_bot/pull/1139)

### 2022/10/9

* 修复碧蓝档案角色获取问题，换源 [@pull/1124](https://github.com/HibiKier/zhenxun_bot/pull/1124)

### 2022/10/7

* 修复 B 站请求返回 -401 错误 [@pull/1119](https://github.com/HibiKier/zhenxun_bot/pull/1119)
* 关闭功能与被动时不再区分大小写，同名时仅被动关闭操作生效

### 2022/9/30

* 修改重置开箱的使用权限 [@pull/1118](https://github.com/HibiKier/zhenxun_bot/pull/1118)

### 2022/9/27

* 更新b站转发解析 [@pull/1117](https://github.com/HibiKier/zhenxun_bot/pull/1117)

### 2022/9/24

* 修复b站订阅 [@pull/1112](https://github.com/HibiKier/zhenxun_bot/pull/1112)
* fix: 重载赛马娘卡池失败 [@pull/1114](https://github.com/HibiKier/zhenxun_bot/pull/1114)

### 2022/9/19

* 更换bilibili_sub获取用户昵称用的API&尝试修了一下get_video() [@pull/1097](https://github.com/HibiKier/zhenxun_bot/pull/1097)
* 修复csgo每日开箱可以多开一次

### 2022/9/18

* 修复 bilireq 版本过低导致 B 站视频解析错误 [@pull/1090](https://github.com/HibiKier/zhenxun_bot/pull/1096)

### 2022/9/16

* fix: bilibili_sub, azur_draw_card [@pull/1090](https://github.com/HibiKier/zhenxun_bot/pull/1090)
* 修复原神资源查询查询完毕后图片存储错误
* b站订阅发送 与 b站订阅 使用相同开关，即：关闭b站订阅

### 2022/9/10

* 自定义群欢迎消息参数不完全时提示报错
* 修改bt插件的url地址 [@pull/1067](https://github.com/HibiKier/zhenxun_bot/pull/1067)

### 2022/9/8

* 添加插件数据初始化判断

### 2022/9/4

* 旧词条提供图片迁移（需要重新获取old_model文件，并将数据库中user_qq为0的数据删除）

### 2022/9/3

* 原神玩家查询增加须弥地区 [@pull/1053](https://github.com/HibiKier/zhenxun_bot/pull/1053)
* av号覆盖全面，且修复av号链接 [@pull/1033](https://github.com/HibiKier/zhenxun_bot/pull/1033)
* 修复词条含有CQ回答的模糊匹配无法被解析
* 禁言检测图片在内存中获取图片hash
* B站订阅在群里中任意群管理员可以统一管理（原来为管理员1无法删除管理员2的订阅）
* 修复原神资源查询地图api数据变更导致更新的地图不完全

### 2022/8/27

* 修复签到积分双倍后，日志记录获得积分变4倍问题 [@pull/1044](https://github.com/HibiKier/zhenxun_bot/pull/1044)

### 2022/8/26

* 修复群管理员无法添加词条
* 修复词条关键词"问"前空格问题

### 2022/8/23

* 修了下模糊匹配 issue#1026 [@pull/1026](https://github.com/HibiKier/zhenxun_bot/pull/1026)

### 2022/8/22

* 修复首次安装时词条旧表出错（因为根本就没有这张表！）
* 取消配置替换定时任务，统一存储
* 对米游社cookie进行判断，整合米游社签到信息 [@pull/1014](https://github.com/HibiKier/zhenxun_bot/pull/1014)
* 修正尘歌壶和质变仪图片获取地址 [@pull/1010](https://github.com/HibiKier/zhenxun_bot/pull/1010)
* 修复词库问答 **很多** 问题[@pull/1012](https://github.com/HibiKier/zhenxun_bot/pull/1012)

### 2022/8/21 \[v0.1.6.3]

* 重构群词条，改为词库Plus，增加 精准|模糊|正则 问题匹配，问题与回答均支持at，image，face，超级用户额外提供 全局|私聊 词库设置，数据迁移目前只提供了问题和回答都是纯文本的词条
* 修复b站转发解析av号无法解析
* B站订阅直播订阅支持短号
* 开箱提供重置开箱命令，重置今日所有开箱数据（重置次数，并不会删除今日已开箱记录）
* 提供全局字典GDict，通过from utils.utils import GDict导入
* 适配omega 13w张图的数据结构表（建议删表重导）
* 除首次启动外将配置替换加入单次定时任务，加快启动速度
* fix: WordBank.check() [@pull/1008](https://github.com/HibiKier/zhenxun_bot/pull/1008)
* 改进插件 `我有一个朋友`，避免触发过于频繁 [@pull/1001](https://github.com/HibiKier/zhenxun_bot/pull/1001)
* 原神便笺新增洞天宝钱和参量质变仪提示 [@pull/1005](https://github.com/HibiKier/zhenxun_bot/pull/1005)
* 新增米游社签到功能，自动领取（白嫖）米游币 [@pull/991](https://github.com/HibiKier/zhenxun_bot/pull/991)

### 2022/8/14

* 修复epic未获取到时间时出错
* 修复订阅主播时动态获取的id是直播间id

### 2022/8/8

* 修复赛马娘重载卡池失败的问题 [@pull/969](https://github.com/HibiKier/zhenxun_bot/pull/969)

### 2022/8/3

* 修复 bili动态链接在投稿视频时URL和分割线连在一起 [@pull/951](https://github.com/HibiKier/zhenxun_bot/pull/961)
* 更新 Epic 免费游戏商城链接拼接规则 [@pull/957](https://github.com/HibiKier/zhenxun_bot/pull/957)

### 2022/8/6

* 修复了原神自动签到返回invalid request的问题，新增查看我的cookie命令 [@pull/971](https://github.com/HibiKier/zhenxun_bot/pull/971) -->

<br>

**..... 更多更新信息请查看文档**

## Todo

- [x] web 管理

## 感谢

[botuniverse / onebot](https://github.com/botuniverse/onebot) ：超棒的机器人协议  
[Mrs4s / go-cqhttp](https://github.com/Mrs4s/go-cqhttp) ：cqhttp 的 golang 实现，轻量、原生跨平台.  
[nonebot / nonebot2](https://github.com/nonebot/nonebot2) ：跨平台 Python 异步机器人框架  
[Angel-Hair / XUN_Bot](https://github.com/Angel-Hair/XUN_Bot) ：一个基于 NoneBot 和酷 Q 的功能性 QQ 机器人  
[pcrbot / cappuccilo_plugins](https://github.com/pcrbot/cappuccilo_plugins) ：hoshino 插件合集  
[MeetWq /nonebot-plugin-withdraw](https://github.com/MeetWq/nonebot-plugin-withdraw) ：A simple withdraw plugin for Nonebot2  
[maxesisn / nonebot_plugin_songpicker2](https://github.com/maxesisn/nonebot_plugin_songpicker2) ：适用于 nonebot2 的点歌插件  
[nonepkg / nonebot-plugin-manager](https://github.com/nonepkg/nonebot-plugin-manager) ：Nonebot Plugin Manager base on import hook  
[H-K-Y / Genshin_Impact_bot](https://github.com/H-K-Y/Genshin_Impact_bot) ：原神 bot，这是一个基于 nonebot 和 HoshinoBot 的原神娱乐及信息查询插件  
[NothAmor / nonebot2_luxun_says](https://github.com/NothAmor/nonebot2_luxun_says) ：基于 nonebot2 机器人框架的鲁迅说插件  
[Kyomotoi / AnimeThesaurus](https://github.com/Kyomotoi/AnimeThesaurus) ：一个~~特二刺螈~~（文爱）的适用于任何 bot 的词库  
[Ailitonia / omega-miya](https://github.com/Ailitonia/omega-miya) ：基于 nonebot2 的 qq 机器人  
[KimigaiiWuyi / GenshinUID](https://github.com/KimigaiiWuyi/GenshinUID) ：一个基于 HoshinoBot/NoneBot2 的原神 UID 查询插件
