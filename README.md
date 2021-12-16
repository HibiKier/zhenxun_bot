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

## 未完成的文档

[传送门](https://hibikier.github.io/zhenxun_bot/)

## 真寻的帮助
请对真寻说: '真寻帮助' or '管理员帮助' or '超级用户帮助' or '真寻帮助 指令'

## 提供符合真寻标准的插件仓库

[AkashiCoin/nonebot_plugins_zhenxun_bot](https://github.com/AkashiCoin/nonebot_plugins_zhenxun_bot)


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
</details>

## 详细配置请前往文档，以下为最简部署和配置，如果你有基础并学习过nonebot2的话


## 简单部署

```

# 配置gocq

在 https://github.com/Mrs4s/go-cqhttp 下载Releases最新版本，运行后选择反向代理，
  后将gocq的配置文件config.yml中的universal改为universal: ws://127.0.0.1:8080/cqhttp/ws

# 获取代码
git clone https://github.com/HibiKier/zhenxun_bot.git

# 进入目录
cd zhenxun_bot

# 安装依赖
pip install -r requirements.txt

# 进行基础配置
####请查看 配置 部分####

# 开始运行
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




## 更新

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

### 2021/12/1 \[v0.0.6.5/6]

* 群权限-1时超级用户命令依旧生效
* 修复以真寻为开头的词条不会被回复
* 修复购买道具可以为负数
* P站排行/搜图提供配置项，将略过大于指定张数的作品
* 昵称提供关键词屏蔽配置项，会将指定关键词替换为“*”
* 取消了自动更新，改为自动检测版本
* 自动更新不再覆盖config.py和移动config.yaml

### 2021/11/29 \[v0.0.6.4]

* 新增cos图撤回配置项
* 新增默认群权限配置项
* 修复权限等级类配置无法正常应用

### 2021/11/24 \[v0.0.6.3]

* 修复在线搜索色图出错
* 修复pix无法正确获取HIBIAPI

### 2021/11/23 \[v0.0.6.2]

* 替换cos API
* 提供私聊b了，即跨群b了用户
* 修复游戏抽卡导入角色失败(原神)
* 修复无Pixiv代理时报错
* 将项目中大部分aiohttp替换为httpx
* 删除了丘丘人翻译插件
* 新增群词条
* 修复游戏抽卡碧蓝航线bwiki格式更改导致获取报错
* 首次启动会生成配置文件后停止程序，配置后再次启动即可

### 2021/11/18

* 修复超级用户无法正确拉真寻入群

### 2021/11/14
  
* 修复功能总开关无法正确开启

### 2021/11/12

* 修复PIX无法url无法正确获取

### 2021/11/10

* 修复PIX表重复创建导致首次无法运行
* 检测Omage图库改为命令方式：检测omega图库

### 2021/11/9

* 修复管理员帮助无法正常响应
* 修复被ban时会一直回复被ban提醒

### 2021/11/5

* 修复ai没有图灵key时报错
* 提供图片路径resource/img/background/check

### 2021/11/4

* 通用排行榜改用图片消息，且可以自定义排行榜人数
* 优化CreateMat排行榜数据显示
* 修复了pix更新多余参数导致失败的问题
* 修复滴滴滴-注入风险
* 修复无法正常关闭滴滴滴，戳一戳
* 添加了发送图片撤回配置项WITHDRAW_IMAGE_TIME
* 修复了天气regex文本过长时会正则匹配过久导致nb卡顿
* message_build新增custom_forward_msg用于快捷生成转发消息
* 插件配置改为yaml存储，新增Config，用于获取和新增插件配置
* 新增 当插件加载失败时，会发送消息提醒超级用户，且在功能状态中对应失败插件写上[ERROR]
* 修复当查看-spuer插件帮助时无法正确回复
* 群内帮助图片会随群内功能开关和插件总开关变化
* 自检改为图像形式
* 更新色图删除了rar_setu，r18_rar和rar文件夹，压缩将统一在temp文件夹
* 更新色图只有在有更新数量或报错时才会提醒超级用户
* 群欢迎消息加入cd
* 加入资源管理resources_manager
* 新增 好友请求/群聊邀请 控制命令

### 2021/10/15

* 适配了原神资源查询米游社地图返回的新格式

### 2021/10/8

* 修复疫情省份查询失效
* 修复功能调用统计全局下统计可能发生错误

### 2021/10/4

* 修复了功能调用统计失效问题
* 当色图库中没有色图时，会在线搜索色图而不是‘没找到符合条件的色图...’
* 快速更新权限再给超级用户发送错误日志
* 修复疫情未加载省份城市无法正常使用

### 2021/10/3

* 对插件进行分离
* 重写了插件与限制管理器以及帮助获取
* 修改一些插件目录和数据存储目录
* 插件通用配置与限制数据将以ymal文件存储 \[路径：data/configs]
* 所有商店相关操作调用统计合并为商店（包括之前已经保存的数据，会先进行备份）
* 简化了点歌的代码相关
* 修复了碧蓝航线抽卡新框导致报错无法正常初始化
* 修复了P站排行/搜图在PC端无法正常显示
* 添加了插件对超级用户是否限制的配置 ‘limit_superuser’
* 添加命令 ‘重载插件配置’，用于生效手动修改配文件
* 超级用户帮助可以添加 -super 来显示该插件的超级用户帮助，示例：帮助.ban -super
* 原神黄历改为网页截图
* 修改了鲁迅说逻辑结构
* 修改了统计图表样式，改为自定义CreateMat
* 节日红包不再被24小时限制，群内多个节日红包将会覆盖
* 当群权限为-1时，不会对群发送修改权限通知，并屏蔽此群一切命令（包括提醒）
* 修复了红包数量可以过大或为负数，红包数量大于群员数量时会修改为群员数量
* 修复了负数开箱
* 签到最低好感度设置为0.01 [@pull/53](https://github.com/HibiKier/zhenxun_bot/pull/53)
* pip安装新依赖 ruamel.yaml
* 修复功能 EPIC [@pull/58](https://github.com/HibiKier/zhenxun_bot/pull/58)

### 2021/9/10

* 修复撤回消息有时无法正确获取消息id

### 2021/9/9

* 替换coser API
* 修复签到uid可能不默认为0
* 修复签到可能重复的问题
* 修复无订阅时递归出错
* 启用了plugins2info_dict, plugins2cd_dict, plugins2exists_dict配置文件，通过USE_CONFIG_FILE=True开启
* 修复涩图local_id会被固定为50
* 优化图库数量查询
* 修复原神大地图过大无法打开报错
* 修复无法显示正确的涩图上限

### 2021/9/7

* 修改 update_info.json
* 修改 更新信息 图片大小
* 修复 查看订阅 命令 UP和番剧无法正常显示
* 修复订阅推送无法正确推送
* 修复搜图返回列表为空时无法正确回复 [@pull/40](https://github.com/HibiKier/zhenxun_bot/pull/40)

### 2021/9/5
* 添加配置PIX_IMAGE_SIZE，调整PIX下载图片大小，当设置的图片404时，改为原图
* 新增配置DEFAULT_GROUP_LEVEL，默认群等级
* 新增超级用户功能 super ban，将屏蔽被ban用户的所有消息，指令：b了
* b站转发解析支持纯BV号解析，且五分钟内不会解析相同url
* 俄罗斯轮盘新增 连胜/最高连胜/连败/最高连败 纪录，新增 最高连胜排行榜/最高连败排行榜
* 增加扩展图库 OmegaPixivIllusts，不想自己找图的人福音（[Ailitonia](https://github.com/Ailitonia) 佬的高质量精品手筛图库）([传送门](https://github.com/Ailitonia/omega-miya/blob/master/archive_data/db_pixiv.7z) )，可以手动导入图库，也可以将解压文件放在bot.py同级目录重启bot
* 增加配置PIX_OMEGA_PIXIV_RATIO，PIX功能发送PIX图库和扩展图库OmegaPixivIllusts图片的比例，如果没有使用扩展图库OmegaPixivIllusts，请设置为(10, 0)
* 增加配置WITHDRAW_PIX_TIME，用于配置在开关PIX图片在群私聊的自动撤回
* 上传图库cases， 开箱 也可以连抽（未更新过没有价格）
* 新增命令 查看群白名单
* plugins2info_dict新增键"default_status"，设置加入新群时功能的默认开关状态
* 增加配置plugins2exists_dict，可自定义是否阻塞某命令同时触发多次
* 增加配置plugins2cd_dict，可自定义为命令添加cd
* 新增B站订阅（直播/番剧/UP）[测试]，提供命令：添加订阅 [主播/UP/番剧] [id/链接/番名]，删除订阅 [id]，查看订阅
* 优化pix和色图的数据库查询
* 触发已关闭的功能的正则时不再触发ai
* 更换coser API
* PIX搜索pid功能在群聊无法搜索PIX图库的r18和OmegaPixivIllusts的r15以及r18，超级用户除外
* PIX单次搜索的图片张数超级用户限制为至多30张，普通用户10张
* PIX超级用户新增-s，-r，可以通过pix -s 查看图库的涩图，pix -r查看图库的r18图，支持搜索，当然，pix图库只区分了r18和非r18，如果-s查询到不色的图也问题不大
* 优化P站排行和搜图，现在需要艾特，改为使用HIBIAPI，在群内时将使用合并消息（群聊搜图会屏蔽R-18）
* win10下playwright相关功能无法使用，但是不再需要删除文件
* 签到大改，优化签到方式与逻辑，改为图片形式发送，有概率额外获得随机道具（好感度有加成）
* 修改撤回功能，改为回复撤回，回复发送撤回
* 更改logging为loguru
* 删除了 发送图片 中的 [N]张图[keyword] 功能
* 修复私聊 关闭[功能] 默认不为 全部 而要添加参数 ‘a’
* 修复0权限用户可以修改禁言检测相关设置

### 2021/8/17

* 新增配置CHECK_NOTICE_INFO_CD，修改群权限，个人权限检测各种检测的提示消息cd
* 新增功能‘连续上传图片’功能，直到输入‘stop’停止
* 新增功能维护时白名单以及对应命令（白名单中的群聊不受维护限制）
* 新增ALAPI功能，微博热搜，可以通过序号来查看部分热搜内容
* 新增配置NICKNAME，偶尔也想换换名字的说（自我介绍仅当NICKNAME=真寻时生效）
* 提供 更新信息 命令，可以使群员查看更新内容（可开关，与其他功能无异，但不会被统计，该命令图片由自动更新生成）
* 超级用户可以通过私聊来对指定qq进行ban/unban
* 超级用户帮助改为图片形式
* 公开图库删除‘色图’
* 群权限检测，个人权限检测，功能开关检测合并，权限检测顺序：个人权限 > 群权限 > 插件开关 >超级用户禁用某群插件 > 超级用户限制群里插件 > 插件维护检测
* 重写群功能管理，超级用户可对群/私聊分别禁用，也可禁用指定群指定功能，新增命令‘功能状态’，超级用户关闭功能提供参数(默认ALL)：group/g（群聊），private/p（私聊）
* 超级用户不会被任何权限等检测阻挡
* 不会重复复读，复读消息只会发送一次
* b站转发解析支持b23.tv，www.bilibili.com链接，cv专栏(playwright截图，压缩倍率0.5，较慢且文字可能不清晰，后优化)
* 我有一个朋友功能，当艾特一个对象时，‘朋友’改为艾特对象的群名片或昵称
* 修复‘上传/删除/移动图片’目录不正确
* 修复天气功能，当城市名在‘天气’后时报错
* 修复配置INITIAL_SETU_PROBABILITY不生效

### 2021/8/10

* 重复的好友请求和邀群提示在5分钟内不会重复提示
* 疫情会优先检查城市，城市省份市区重名时请添加‘市’
* 添加命令‘原神资源查找’，‘设置cookie’
* 添加配置AUTO_UPDATE_ZHENXUN，是否自动更新真寻，默认True
* 添加配置MAX_RUSSIAN_BET_GOLD，俄罗斯轮盘赌注最大金额，默认1000
* 检查更新真寻定时任务时间改为12 : 00
* 添加功能能不能好好说话(nbnhhsh)
* 添加功能随机roll，无参为数字，有参为随机参数
* 添加linux重启脚本以及重启命令‘重启’（建议首次生成restart.sh先查看命令是否正确）
* 修复管理员功能的权限检测
* 修复丢人爬开关

### 2021/8/6

* 天气查询会优先遍历城市
* 添加自动更新真寻命令

##### 如果你的版本为 2021/8/4，可以直接复制plugins/check_zhenxun_update后，通过指令来更新真寻

### 2021/8/4

* 修改天气与疫情城市数据，改为api获取，丰富疫情的回复消息
* 原神资源查询，大地图将被压缩至9M，且启动时当大地图存在时不再自动更新地图
* 下载数据库内色图时将直接存储至_setu，不再存储至临时文件
* 重复的好友请求或邀请请求在一定时间不会重复发送提醒
* 添加每日自动清理临时图片定时任务
* 修复金币排行显示
* 修复无法正常关闭戳一戳功能

### 2021/7/30

* 重构代码，进行优化，添加注释，删除冗余代码，降低代码耦合
* 添加功能：PIX（一套快捷的pixiv存图命令，自建图库存储url等信息？意在获取自己或群友xp的图）
* 添加功能：清理临时图片文件（temp/rar/r18_rar文件夹）
* 添加额外定时任务（5分钟检测一次），解决加入新群时无法及时为管理员提供权限
* 添加配置ALAPI_AI_CHECK，开关AI回复文本检测
* 添加配置IMPORT_DEFAULT_SHOP_GOODS，控制是否导入内置的三个商品（好感度加持卡ⅠⅡⅢ）
* 添加配置ONLY_USE_LOCAL_SETU，仅仅使用本地色图（有的话），提升速度，但无法在线搜索色图和保存链接
* 添加配置WITHDRAW_SETU_TIME，是否需要延迟撤回色图，可配置仅群里，私聊或全部
* 好友请求，入群请求，滴滴滴-，/t，被踢出群提醒，的提示消息更加丰富
* 彻底重写原神资源查找，添加规划路线（路线残缺缺缺缺版，有空补）添加命令‘更新原神资源信息’，强制更新地图等资源
* 优化色图和P站排行/搜图检测用户是否正在触发命令代码
* 当群最后发言大于36小时，也会关闭广播通知
* 功能维护时超级用户依然可以调用（苦了谁都不能苦了自己）
* 修复获取赛马娘UP公告
* 重写 色图/更新色图
  * 色图数据存储改为数据库，启动时会更新之前的色图数据(有的话)，更新完毕后会删除原数据文件，如果需要保留请提前备份，
  * lolicon api改为v2
  * 取消r18次数限制
  * 单次搜索至多保存100条链接
  * 添加定时撤回
  * 暂时取消上传/删除色图
*
* 更新建议（不要替换你的data和resources文件夹！）
  * 删除configs，plugins，services，utils，models文件夹重新clone
  * 删除多余文件夹，resources/img/genshin/seek_god_eye
  * 清空resources/img/genshin/genshin_icon文件夹，仅保留box.png和box_alpha.png
  * 替换bot.py

### 2021/7/27

* 原神今日素材改为单张截图+拼图，更新文件utils/img_utils.py及plugins/genshin/material_remind/__init__.py

### 2021/7/26

* 修复原神今日素材稻妻城开放后截图不完整的问题

### 2021/7/14

* 原神今日素材自动更新时间由 00:01 -> 04:01 [#issues7](https://github.com/HibiKier/zhenxun_bot/issues/7)
* 小问题的修复和优化

### 2021/7/12

* 修复开箱功能单抽出金时存储格式错误导致 ‘我的金色’ 无法正常发送图片
* 小问题的修复和优化

### 2021/7/6

* 识番功能 trace.moe 替换为新API（旧API已失效）
* 小问题的修复和优化

### 2021/6/30

* 将plugin2name和plugin2level合并为plugin2info
* util改为utils（。。！）
* 修复当用户发送速度极快时开箱会突破每日限制
* 新增功能：通过PID获取图片
* 发送图片新增功能：搜索图片
* 功能统计可视化
* 新增命令：好感度总排行
* 原神每日素材改为从"可莉特调"截图，提供命令‘更新原神每日素材’和定时任务
* 修复月功能统计错误的问题

### 2021/6/24

* 添加了一些ALAPI：网易云热评，获取b站视频封面，古诗（需要填写ALAPI_TOKEN）
* 如果填写了ALAPI_TOKEN，将会检测备用接口回复的文本是否合规
* 优化了色图，当搜索色图下载失败时，会从本地色图库中发送相关tag色图
* 当网易云点歌繁忙时会尝试多次点歌

### 2021/6/23

* 添加功能：群权限（所以说内鬼都快爬，可以在configs/config.py中修改各个功能的权限等级）
* 优化了数据统计，将以7天，30天为周期，为将来更方便实现数据可视化
* 更新坎公骑冠剑UP卡池
* 修复赛马娘UP卡池
* 修复一些小问题

### 2021/6/18

* 修复p站排行，搜图因网络问题爆炸时没有具体回复
* 更换色图显示方式为 id，title，author，pid
* 修复修改商品后商品顺序改变
* 滴滴滴- 和 /t支持图片回复
* 将/t回复更加简单(可以通过序号)，且可以直接发送群
* 修复bt功能无法交互

### 2021/6/17

* 修复p站排行，搜图因网络问题爆炸时没有具体回复
* 更换色图显示方式为 id，title，author，pid

### 2021/6/15
* 修改了‘帮助’功能，具体为‘帮助 指令名’，未指定指令名时则为查看全部功能列表
* 修改了色图的存储数据格式
* 色图功能搜索的色图改为随机从urls中随机抽取
* 将商品数据存储入数据库，提供 '增加/删除/修改商品' 指令
* 商店列表图片不再使用固定背景图，改为直接拼图
* 增加功能：俄罗斯轮盘/胜场排行/败场排行/欧洲人排行/慈善家排行
* 增加功能：金币红包（节日红包与群红包相互独立）
* 金币排行
* 重写一个朋友插件
* 其他微小调整

### 2021/6/4
* 重写BT功能
* 进行一些BUG修复和微小调整
* 添加撤回功能[nonebot-plugin-withdraw](https://github.com/MeetWq/nonebot-plugin-withdraw)
* 为色图功能添加额外的 上传色图 和 删除色图方法（影响hash）

### 2021/5/26
* 将语录源更换为一言api


## Todo
- [ ] 提供更多对插件的控制
- [ ] 明日方舟卡片式的签到..(大概)
- [ ] 更多的群管理功能
- [ ] 数据清理控制
- [ ] docker容器

## 感谢
[Onebot](https://github.com/howmanybots/onebot)  
[go-cqhttp](https://github.com/Mrs4s/go-cqhttp)  
[nonebot2](https://github.com/nonebot/nonebot2)  
[XUN_Langskip](https://github.com/Angel-Hair/XUN_Bot)  
[cappuccilo_plugins](https://github.com/pcrbot/cappuccilo_plugins#%E7%94%9F%E6%88%90%E5%99%A8%E6%8F%92%E4%BB%B6)  
[nonebot-plugin-withdraw](https://github.com/MeetWq/nonebot-plugin-withdraw)  
[nonebot_plugin_songpicker2](https://github.com/maxesisn/nonebot_plugin_songpicker2)  
[nonebot_plugin_manager](https://github.com/Jigsaw111/nonebot_plugin_manager)  
[Genshin_Impact_bot](https://github.com/H-K-Y/Genshin_Impact_bot)  
[nonebot2_luxun_says](https://github.com/NothAmor/nonebot2_luxun_says)  
[AnimeThesaurus](https://github.com/Kyomotoi/AnimeThesaurus)  
[omega-miya](https://github.com/Ailitonia/omega-miya)
