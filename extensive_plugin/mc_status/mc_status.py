import base64
import io,sys,os
from mcstatus import JavaServer
from PIL import Image, ImageDraw, ImageFilter,ImageFont

fontPath = '.\\extensive_plugin\\mc_status\\Arial-Unicode-Regular.ttf'

# 状态函数
def mc_status_get(ip):

    server = JavaServer.lookup(ip)
    try:
        status = server.status()
        # ping值 保留小数点后3位
        ping = str("PING \n" + '{:0.3f}'.format(status.latency) + "ms")
        # 版本
        version = str(status.version.name)
        # 在线人数
        onp = "{status.players.online}/{status.players.max}".format(status=status)
        onlineCount = "在线人数： " + str(onp)
        # MOTD
        discribe = str(status.description)
        # 替换掉样式代码 klnmor
        discribe = discribe.replace('§k','').replace('§l','').replace('§m','').replace('§n','').replace('§o','').replace('§r','')
        # logo
        pic = base64.b64decode(status.favicon[22::])
        open('logo1.png', 'wb').write(pic)
        fr = Image.open('logo1.png').resize((100,100))
        frame = Image.new("RGB", (700, 128), (25, 25, 25))
        frame.paste(fr, (10 , 14))
        draw = ImageDraw.Draw(frame)
        # 字体函数定义
        def draw_text(x, y,text, fill,fontsize,):
            # import os
            # print("路径为："+os.getcwd())
            font = ImageFont.truetype(fontPath, fontsize)
            draw.text((x, y), text, fill=fill, font=font)

        # draw_text(128, 25, discribe, fill=(255,170,0), fontsize=15)
        # 更新为支持分节符的版本
        def colorful_describe():

            font_ = ImageFont.truetype(fontPath, 17)

            # Define the text to be added to the image

            # Define the color codes
            color_codes = {
                '§0': (0, 0, 0),
                '§1': (0, 0, 170),
                '§2': (0, 170, 0),
                '§3': (0, 170, 170),
                '§4': (170, 0, 0),
                '§5': (170, 0, 170),
                '§6': (255, 170, 0),
                '§7': (170, 170, 170),
                '§8': (85, 85, 85),
                '§9': (85, 85, 255),
                '§a': (85, 255, 85),
                '§b': (85, 255, 255),
                '§c': (255, 85, 85),
                '§d': (255, 85, 255),
                '§e': (255, 255, 85),
                '§f': (255, 255, 255),
                '§g': (221, 214, 5)
            }

            # Split the text by the key identifier
            parts = discribe.split("§")
            print(parts)

            # Set the starting x and y position for the text
            x = 128
            y = 15

            # Loop through the parts of the text
            for part in parts:
                if part:
                    # Get the color code for the current part
                    
                    color_code = part[0]
                    color = color_codes.get(f"§{color_code}", (0, 0, 0))

                    # Get the text for the current part (excluding the color code)
                    text_ = part[1:]

                    # Draw the text on the image
                    draw.text((x, y), u'{}'.format(text_) , fill=color, font=font_)

                    # Get the width and height of the text
                    width, height = draw.textsize(text_, font=font_)
                    if '\n' in part:
                        y += height
                        x = 128
                        continue

                    # Update the x position for the next piece of text
                    x += width
        
        colorful_describe()
        draw_text(570, 25, ping, fill=(124,255,0), fontsize=14)
        draw_text(120, 95, onlineCount , fill=(160, 32, 240), fontsize=17)
        draw_text(335, 95, "版本: ", fill=(130, 120, 100), fontsize=16)
        # 处理version长度过长的问题
        if (len(version) > 80):
            version = version[:40] + "\n"   + version[40:80:] + "\n" + version[80::]
            draw_text(375, 75, version, fill='white', fontsize=15)
        elif(len(version) > 40):
            version = version[:40] + "\n"   + version[40::]
            draw_text(375, 85, version, fill='white', fontsize=15)
        else:
            draw_text(375, 95, version, fill='white', fontsize=15)
        # 图片写入内存流 并转换为 base64
        buffer = io.BytesIO()
        frame.save(buffer,"PNG")
        buf_bytes=buffer.getvalue()
        base64_data=str(base64.b64encode(buf_bytes))[2:-1:]
        
        return base64_data 
    except Exception as e:
        print(f"异常为:{e}")
        frame = Image.new("RGB", (350, 100), (5, 5, 5))
        draw = ImageDraw.Draw(frame)
        draw.text((40, 10), ip + "\n服务器不存在或离线", fill='white', font=ImageFont.truetype(fontPath, 30))
        buffer = io.BytesIO()
        frame.save(buffer,"PNG")
        buf_bytes=buffer.getvalue() # 从内存中取出bytes类型的图片
        base64_data=str(base64.b64encode(buf_bytes))[2:-1:] # 将bytes类型按base64进行编码，返回值还是bytes类型
        
        return base64_data
def mc_player_list_get(ip):
    server = JavaServer.lookup(ip)
    try:
        status = server.status()
        player_list = "玩家列表（一部分）：\n"
        # 在线列表
        for j in status.players.sample:
            
            player = str(j.name) +" - "+ str(j.id)
            player_list += player + "\n"
        return player_list
    except:
        return "服务器不存在或离线\n或者服务器没有开启玩家列表"


base64.b64decode(mc_status_get('mc.magicst.cn'))