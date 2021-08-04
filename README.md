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

如果该项目的图片等等侵犯猫豆腐老师权益请联系我删除！

## 声明
此项目仅用于学习交流，请勿用于非法用途

## 真寻的帮助
请对真寻说: '真寻帮助' or '管理员帮助' or '超级用户帮助' or '真寻帮助 指令'


## 功能列表
<details>
<summary>已实现的功能</summary>

### 已实现的常用功能
- [x] 昵称系统（群与群与私聊分开.）
- [x] 图灵AI（会把'你'等关键字替换为你的昵称），且带有 [AnimeThesaurus](https://github.com/Kyomotoi/AnimeThesaurus)，够味
- [x] 签到/我的签到/好感度排行/好感度总排行（影响色图概率和开箱次数，支持配置）
- [x] 发送某文件夹下的随机图片（支持自定义，默认：美图，萝莉，壁纸）
- [x] 尝试搜索不色的图片 ↑↑
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
- [x] 我有一个朋友想问问..（pcrbot插件..彻底重写）
- [x] 原神黄历  (使用[Genshin_Impact_bot](https://github.com/H-K-Y/Genshin_Impact_bot)插件)
- [x] 原神今日素材 (原[Genshin_Impact_bot](https://github.com/H-K-Y/Genshin_Impact_bot)插件，彻底重写，实现方法改为网页截图)
- [x] 原神资源查询  (使用[Genshin_Impact_bot](https://github.com/H-K-Y/Genshin_Impact_bot)插件，资源下载优化为异步下载)
- [x] 金币红包

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
- [x] 撤回 (使用[nonebot-plugin-withdraw](https://github.com/MeetWq/nonebot-plugin-withdraw)插件)
- [x] 滴滴滴-（用户对超级用户发送消息）
- [x] 金币红包/金币排行
- [x] 俄罗斯轮盘/胜场排行/败场排行/欧洲人排行/慈善家排行
- [x] 网易云热评
- [x] 念首古诗
- [x] 获取b站视频封面
- [x] 通过PID获取图片
- [x] 功能统计可视化

### 已实现的管理员功能
- [x] 更新群组成员信息
- [x] 95%的群功能开关 (基于[nonebot_plugin_manager](https://github.com/Jigsaw111/nonebot_plugin_manager)插件修改)
- [x] 查看群内被动技能状态
- [x] 自定义群欢迎消息（是真寻的不是管家的！）
- [x] .ban/.unban（支持设置ban时长）= 黑白名单
- [x] 刷屏禁言相关：刷屏检测设置/设置禁言时长/设置检测次数
- [x] 上传图片 （上传图片至指定图库）
- [x] 移动图片  （同上）
- [x] 删除图片  （同上）

### 已实现的超级用户功能
- [x] 添加/删除管理（是真寻的管理员权限，不是群管理员）
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

#### 超级用户的被动技能
- [x] 邀请入群提醒(别人邀请真寻入群)
- [x] 添加好友提醒(别人添加真寻好友)

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
- [x] 群管理员监控，自动为新晋管理员增加权限，为失去群管理员的用户删除权限
- [x] 群权限系统
- [x] 定时更新权限
</details>

## 功能具体指令
<details>
<summary>功能具体指令说明</summary>

### 常用功能

| 功能                   |                    指令                 |        说明
| ----------------------| :--------------------------------------:| :------------------------:  
| 签到                   |         签到/我的签到/好感度排行/好感度总榜/好感度总榜\[显示我/屏蔽我]            |     普通的签到插件，可以获得好感度和金币<br>好感度影响开箱次数和涩图触发概率，金币用于购买道具，俄罗斯轮盘赌注以及金币红包<br>好感度总榜，显示所有群的群员好感度排行，可通过命令好感度总榜\[显示我/屏蔽我] 来设置是否隐藏
| 发送图片                |             美图/壁纸/萝莉 \[id](默认随机)/\[num]张图\[keyword]                 |      发送指定文件夹下的图片<br>示例：萝莉->发送img文件夹下luoli文件夹下的图片<br>在线搜索一些不色的图，示例：3张图米浴
| 色图                   |         色图/色图xx/n张色图/n张xx的色图/查色图(查询本地色图信息)/色图r【n<10】            |     色图r返回10张r18色图(仅私聊)，并限制每日次数(默认5次)<br>其他示例：色图 真寻 <br>5张真寻的色图
| 黑白草图                |         黑白草图/黑白图 \[文字] \[图片]            |   整活生成器，示例：黑白图 我喜欢真寻 \[图片]
| coser                 |         coser/cos/括丝                   |   coser图片，说实话挺失望的，太色了
| 骂我                   |          骂我                            |  就是发送钉宫的语音罢了
| 戳一戳                 |         戳一戳                         |   随机发送钉宫语音 or 美图 or 萝莉图 or 文本
| 模拟开箱               |         开箱 \[武器箱名称](默认随机)/N连开箱 \[武器箱名称](默认随机)/我的开箱/群开箱统计/我的金色           |   当不指定武器箱时默认随机，此功能需要先在/open_cases/config.py中编写指定武器箱数据，然后提前爬取价格，使用超级用户命令更新cookie后，再使用命令更新xx武器箱【注：未设置爬取频率，可能会被禁用api（请谨慎！！用小号！！）】
| 鲁迅说过               |         鲁迅说过 \[文本]              | 示例：鲁迅说过 真寻世界第一可爱
| 假消息                |         假消息 \[网址] \[标题] \[内容](可选) \[图片](可选)          |   构造虚假的分享消息
| 商店系统               |        商店/我的金币/购买道具 \[名称或序号] \[数量](默认1)/使用道具 \[名称或序号]        | 示例：<br>购买道具 1 3<br>购买道具 好感度双倍加持卡Ⅰ 3<br>使用道具 1<br>使用道具 好感度双倍加持卡Ⅰ
| 抽卡系统               |        原神/明日方舟/赛马娘/坎公骑冠剑/碧蓝航线/阴阳师/公主连结(pcr)/FGO N抽/一井        |  详细帮助请查看: [nonebot_plugin_gamedraw](https://github.com/HibiKier/nonebot_plugin_gamedraw) <br>示例：原神90抽
| 我有一个朋友           |         我有一个朋友他说/想问问/\[文本]         |  会将文本中的(他，她，它)替换成 '我'<br>示例：我有一个朋友想问问他喜不喜欢真寻
| 昵称系统              |         以后叫我\[昵称]/以后请叫我\[昵称]/我是谁/我叫什么          |  此昵称会替换与真寻聊天中 '你' 的名称(群名片)，群与群与私聊的昵称相互独立
| 原神黄历              |         原神黄历                        | 查看今日原神黄历，含有每日10:25的定时任务
| 原神材料               |        今日素材                             | 发送可莉特调的截图
| 丘丘语翻译            |          丘丘翻译/丘丘一下/丘丘语翻译          |  示例：丘丘一下 mimi
| 原神资源查询            |          原神资源查询 \[资源名称] \[路线]?/\[资源名称]在哪/哪里有\[资源名称]/原神资源列表    |  如果资源名称末尾添加‘路线’的话将生成残缺缺缺版的优先路径<br>示例：嘟嘟莲在哪<br>原神资源查询嘟嘟莲路线
| 俄罗斯轮盘             |        装弹\[子弹数] \[金额](默认200)/开枪/结算/我的战绩/胜场排行/败场排行/欧洲人排行/慈善家排行           | 紧张刺激的群内小游戏，使用每日签到的金币作为赌注，具体玩法请发送 真寻帮助 俄罗斯轮盘
| 红包系统              |         塞红包\[金额] \[数量](默认5)/抢/开/戳一戳/退回          | 仿微信明日方舟红包的样式（pil拼图大师！），每个红包金额随机生成，最多会是红包总金额的1/3，退回用于退回一分钟后还未开完的红包
| 金币排行              |         金币排行                                              |   字面意思
|网易云热评            |         到点了/12点了/网易云热评/网易云评论                      |     防下塔
| 古诗                |         念诗/念首诗/来首诗                                      |     突然文艺起来了
| pil对图片的操作        |         修改尺寸/等比压缩/旋转图片/水平翻转/铅笔滤镜/模糊效果/锐化效果/高斯模糊/边缘检测/底色替换                   |  选项较多，请直接发送 真寻图片帮助
| BUFF皮肤底价查询       |         查询皮肤 \[武器名称] \[皮肤名称]          | 网络不友好的话会经常超时<br>示例：查询皮肤 沙漠之鹰 印花集
| 天气查询             |          \[城市]天气                      | 非常常见的插件，第一个入门插件
| 疫情查询              |           疫情/查询疫情 \[城市名或省份名]        | 示例：疫情杭州
| bt磁力搜索            |           bt \[关键词] \[页数](默认第1页)         | 该功能仅仅提供给私聊，因为可以搜到一些色色的东西，示例：bt钢铁侠 5
| 上车                |                  略                      |  直接查看真寻帮助 上车，每日限制次数(默认5)
| 以图识番            |           识番 \[图片]                      | 以图搜翻，图片越清晰越完整正确率越高
| 以图搜图            |          识图 (asc)? \[图片]                | 参数asc更换搜索引擎为ascii2d，默认为saucenao
| 点歌                |             点歌 \[歌名]                   |  网易云点歌小助手
| 搜番              |             搜番 \[关键字]                     | 群聊只返回5个结果，私聊返回20个结果
| epic白嫖游戏通知   |              epic                          | 通知你又到了白嫖游戏的时候，可以不玩，不能没有
| P站排行榜           |             p站排行 \[排行类型参数](默认日榜) \[数量](可选) \[日期](可选)| 9种不同排行榜，r18类型仅可私聊，通过参数选择，查看真寻帮助p站排行<br>示例：p站排行榜 1 9 2018-4-25
| 搜图              |           搜图 \[关键词] \[数量](可选) \[排序方式](可选) \[r18](可选)| r18仅可私聊，查看真寻帮助搜图
| 通过PID搜索图片   |           p搜 [pid]                        |     在群内使用此功能会在30秒内撤回
| 翻译               |          英翻/日翻/韩翻/翻韩/翻日/翻英 \[文本]       | 三种语言互相翻译
| 获取b站视频封面    |         b封面 [链接/av/bv/cv/直播id]                |     快捷的封面获取方式
| 群欢迎消息         |           群欢迎消息/查看群欢迎消息/查看当前群欢迎消息         |     查看给真寻设置的群欢迎消息
| 自我介绍            |               自我介绍                         |  没错，一份正经的真寻自我介绍
| 我的权限            |               我的权限                           |  真寻内部定义的一套权限系统
| 我的信息           |                我的信息                      | 唯一的作用就是看看什么时候加入群
| 撤回              |               撤回 \[消息位置](默认为最新一条消息)   | 按顺序撤回发送的消息，示例：撤回 1
| 滴滴滴-            |             滴滴滴- \[文本]                    | 用于用户联系真寻的超级用户
|功能调用统计可视化  |               功能调用统计（自记录以来的功能调用统计）<br>周功能调用统计 [plugin_name]<br>月功能调用统计 [plugin_name]| 当plugin_name为空时为7天或30内的所有功能统计
| pix         |       pix/PIX [tags/uid/pid:pid] [num]         |     无参数时随机查看pix图库的图片(无r18)，num数量默认=1，tags：查看相关tags图片，uid：查找相关画师图片，pid:pid:指定查看pid图片<br>示例：pix原神 3<br>pix23493844<br>pixpid:29429933
| 添加pix关键词/uid/pid |  添加pix关键词/uid/pid *[关键词/uid/pid]| 添加关键词或uid或pid用于下次搜索，关键词搜索相关tag，uid会收录作者下收藏符合标准的作品，pid收录单张作品<br>示例：添加pix关键词 原神<br> 添加pixuid 123441<br>添加pixpid 2748937|
| 查看pix图库     |       查看pix图库 [tags]   |        查看已收录的tag相关图片数量<br>示例：查看pix图库 原神 莫娜
|显示pix关键词    |       显示pix关键词         |       查看已收录的所有关键词/UID/PID

### 管理员功能

**群主与群管理员默认5级权限**

| 功能            | 权限等级                           |                    指令                 |        说明
| -------------| --------------| :--------------------------------------:| :------------------------: 
| 更新群组成员信息 |    1   |      更新群组成员信息/更新群组成员列表         |   存储群员的基本信息，虽然有自动更新，但备个命令以防万一
| 群功能开关      |   2    |      开启/关闭\[指令名]功能                 |    群帮助中左边带有√的功能都可以通过此命令开启或关闭，示例：开启色图
| 查看群被动技能    |   2  |       群通知状态                         |    详细请查看被动技能列表
| 被动技能开关       |  2   |       开启/关闭被动技能                    |   有时候花里胡哨通知也会很烦人
| 自定义群欢迎消息    |  2  |       自定义群欢迎消息 \[文本] \[图片]        | 文本和图片至少需要一个，在文本内添加"\[at]"字符串可以用来设置艾特进群的新群员
| 黑名单          |   5   |        .ban/.unban \[at] \[小时](可选) \[分钟](可选)|  不提供具体时间的话则ban掉永久，且权限低的用户无法unban高权限用户的ban，同级权限也无法进行ban/unban <br>示例：.ban@笨蛋 1 50
| 刷屏检测相关     |   5   |        刷屏检测设置/设置检测时间 \[文本]/设置检测次数 \[文本]/设置禁言时长 \[分钟]| 非常讨厌刷屏的人，打算给他们一点教训
| 上传图片        |  6   |        上传图片 \[图库] \[图片]...           | 上传图片至指定图库，虽然并不打算开放给群员，但还是写了，支持批量图片<br>示例：上传图片 美图 \[图片]..
| 删除图片         | 6  |         删除图片 [图库] \[图片id]                    | 通过指定本地图片id来删除指定图库的图片<br>示例：删除图片 美图 1
| 移动图片       |    6   |       移动图片 \[移出的图库] \[移入的图库] \[图片id]    | 移动指定图库中的图片到指定的新图库中，移入的图片id更改为移入图库的最后一位，移除的图库中原本图片的id又最后一位图片替代<br>示例：移动图片 美图 萝莉 22

### 超级用户功能

| 功能                   |                    指令                 |        说明
| ----------------------| :--------------------------------------:| :------------------------: 
| 权限增删      |   添加/删除权限 \[at] \[level]<br>添加/删除权限 [qq] [group] [level]      | 用于添加或修改权限等级，且该权限不会被自动更新取消
| 查看群组/好友   |      查看群组/好友                |   查看真寻添加的群组与好友
| 广播          |     广播- [文本]                         | 广播所有群组
| 更新色图      |     更新色图                      | 更新群友搜索色图时保存的url
| 回复          |                 /t              | 命令较多，请查看/t帮助，省略群号则私聊用户(必须要有用户的好友)
| 更新cookie  |       更新cookie \[cookie]           | 用于更新开箱数据和查询buff皮肤
| 开启广播通知    |     开启/关闭广播通知 \[群号]        | 用于开启/关闭是否对某些群进行广播(上边的广播方法)
| 退群        |       退群 \[群号]                  | 用于退出某一些群
| 检查系统状态  |       自检                        | 略
| 更新好友/群组信息|     更新好友/群组信息              | 包含自动更新，被t出群等等有更好的可视信息
| 重载卡池    |         略                       | 重载抽卡的游戏卡池，请查看 \[nonebot_plugin_gamedraw](https://github.com/HibiKier/nonebot_plugin_gamedraw)
| 添加商品     |      添加商品 \[名称]-\[价格]-\[描述]-\[折扣](小数)(可选)-\[限时时间](分钟)(可选)   |  为真寻的商店添加一点点道具<br>示例：添加商品-昏睡红茶-300-一杯上好的奇怪红茶-0.9-60
| 删除商品    |       删除商品 \[名称或序号]           | 在真寻的商店中删除一点东西
| 修改商品   |        修改商品 -name \[名称或序号] -price \[价格] -des \[描述] -discount \[折扣] -time \[限时]| 注意空格，不需要的参数可以不加<br>示例：修改商品 -name 1 -price 900  【修改序号为1的商品的价格为900】
| 节日红包    |       节日红包 \[金额] \[数量] \[祝福语](可选) \[群号](可选)...  | 群号支持批量，使用空格隔开，不使用群号则对所有群发送节日红包，节日红包有效时间为24小时，祝福语默认为“恭喜发财 大吉大利”<br>示例：节日红包 10000 15 真寻真可爱 123324423 23423423
| 修改群权限 |       修改群权限 \[group] \[level]     |     所以说这功能是对内鬼的无奈，默认群权限为5，默认无法使用 色图/coser/p站排行/搜图（这些功能都要9级权限）
|更新原神今日素材|      更新原神今日素材              |     自动更新原神每日素材失败时可以手动触发
|更新原神资源信息|      更新原神资源信息                |     除了每日自动更新的资源外，额外更新大地图
| 清理数据    |        清理数据                 |       清理 temp，rar，r18_rar 文件夹的文件数据
|添加pix关键词/uid/pid |   添加pix关键词/uid/pid [keyword/pid:pid/uid:uid] [-f]?  |  与普通功能相同，额外可以通过参数 -f 强制通过检测
|删除pix关键词     |     删除pix关键词 *[keyword/uid/pid:pid]  |   删除已收录的keyword/uid/pid
|更新pix关键词     |     更新pix关键词 [keyword/pid:pid/uid:uid] [num]| 更新keyword，uid，pid或指定uid，pid，未指定时，则更新全部，当num未指定时为keyword/uid/pid更新全部<br>示例：更新pix关键词<br>更新pix关键词uid 8<br>更新pix关键词pid:83457477
|删除pix图片      |     删除pix图片 [*pid] [-b]?       | [-b]参数为删除的同时加入黑名单(不再更新)，虽然是pid，但是_p也可以<br>示例：删除pix图片3458344 8235234_p1 -b
|显示pix关键词     |     显示pix关键词              |   与普通功能相同，额外显示待收录和黑名单
|pix检测更新      |     pix检测更新 [update]?               |   检测从未更新过的pid或uid，-update参数将在检测后直接更新未更新过的pid或uid<br>示例：pix检测更新 update

</details>

## 部分功能展示
<details>
<summary>部分功能展示及说明</summary>

### 帮助以及开关（功能控制）

群帮助将会在功能左侧展示该功能的开关，带有√或×的功能代表可以开关<br>
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

### 色图

略，send_setu/check_setu_hash.py文件用于记录涩图hash和检测文件名是否连贯（例如：0.jpg, 1.jpg....）

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

### 抽卡（8种手游的抽卡）

已单独分离并上传至nb2商店，不再放图片了，项目地址：[nonebot_plugin_gamedraw](https://github.com/HibiKier/nonebot_plugin_gamedraw)

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

使用nb2商店插件 [nonebot_plugin_picsearcher](https://github.com/synodriver/nonebot_plugin_picsearcher) （可配置图片返回的最大数量）

![](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/shitu.png)

### epic免费游戏

访问rsshub获取数据解析<br>可以不玩，不能没有

![](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/epic.png)


### P站排行/搜图

访问rsshub获取数据解析

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

### 金币红包

![](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/redbag0.png)
![](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/redbag1.png)
![](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/redbag2.png)

### 俄罗斯轮盘
![](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/russian0.png)
![](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/russian1.png)
![](https://raw.githubusercontent.com/HibiKier/zhenxun_bot/main/docs/russian2.png)

<br>

### 其他

点歌：使用 [nonebot_plugin_songpicker2](https://github.com/maxesisn/nonebot_plugin_songpicker2) 插件<br>
<br><br>
## 其他功能请自己试一试 ）

</details>

## 部署

```

# 配置gocq

在 https://github.com/Mrs4s/go-cqhttp 下载Releases最新版本，运行后选择反向代理，
  后将gocq的配置文件config.yml中的universal改为universal: ws://127.0.0.1:8080/cqhttp/ws

# 获取代码
git clone https://github.com/HibiKier/zhenxun_bot.git

# 安装依赖
pip install -r requirements.txt

# 进入目录
cd zhenxun_bot

# 进行基础配置
####请查看 配置 部分####

# 开始运行
python bot.py
```

## 配置（暂时不更新 json 配置，请将USE_CONFIG_FILE设置为False）
在 configs/config.py 中的 USE_CONFIG_FILE，默认为False

```
1.在.env.dev文件中

  SUPERUSERS = [""]   # 填写你的QQ

2.在configs/config.py文件中
  必填：
    1. API KEY
    2.数据库配置

  在./configs/config.py中配置基本配置（除API KEY ，数据库和代理外都含有默认值）
  在./configs/path_config.py配置路径（含有默认配置）

  ########（暂时不更新 json 配置，请将USE_CONFIG_FILE设置为False，直接进入./configs/config.py进行配置）
  # 是否使用配置文件（为True时这将会生成三份配置文件
                   ./config.json：主要配置
                   ./configs/plugins2cmd_config.json: 功能模块与对应命令配置
                   ./configs/other_config.json: 一些插件配置）

  USE_CONFIG_FILE = True

  # 如果不使用配置文件，将USE_CONFIG_FILE设置为False
  #可在./configs/config.py文件中修改配置，在./configs/path_config.py修改资源路径
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
        "bind": "",
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
        "MAX_SIGN_GOLD": 200,         # 签到好感度加成额外获得的最大金币数
        "MAX_SETU_R_COUNT": 5,        # 每日色图r次数限制
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


## 更新

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
