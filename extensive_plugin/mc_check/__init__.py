from nonebot import on_command
from services.log import logger
from utils.message_builder import image
from nonebot.adapters.onebot.v11 import (
  Bot,
  Event,
  MessageSegment,
  Message)
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.matcher import Matcher
from configs.config import Config
from .data_source import *
import base64, os, ujson

__zx_plugin_name__ = "我的世界查服"
__plugin_usage__ = """
usage：
    我的世界服务器状态查询
    用法：
        查服 [ip]:[端口] / 查服 [ip]
        设置语言 Chinese
        当前语言
    eg:
        minecheck ip:port / minecheck ip
        set_lang English
        lang_now
""".strip()
__plugin_des__ = "用法：查服 ip:port / minecheck ip:port"
__plugin_type__ = ("一些工具",)
__plugin_cmd__ = ["查服/minecheck","设置语言/set_lang","当前语言/lang_now"]
__plugin_version__ = 1.4
__plugin_author__ = "molanp"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["查服",'minecheck','设置语言','set_lang','当前语言','lang_now'],
}
__plugin_configs__ = {
    "JSON_BDS": {"value": False, "help": "基岩版查服是否显示json版motd|Bedrock Edition checks whether the JSON version of MODD is displayed", "default_value": False},
    "JSON_JAVA": {"value": False, "help": "JAVA版查服是否显示json版motd|Java Edition checks whether the JSON version of motd is displayed", "default_value": False},
    "LANGUAGE": {"value": "Chinese", "help": "Change the language(Chinese or English)", "default_value": "Chinese"}
}

def readInfo(file):
    with open(os.path.join(path, file), "r", encoding="utf-8") as f:
        return ujson.loads((f.read()).strip())

path = os.path.dirname(__file__)
lang = Config.get_config("mc_check", "LANGUAGE")
if lang == None: 
  lang = "Chinese"
lang_data = readInfo("language.json")

check = on_command("查服", aliases={'minecheck'}, priority=5, block=True)
lang_change = on_command("设置语言",aliases={'set_lang'},priority=5,block=True)
lang_now = on_command("当前语言",aliases={'lang_now'},priority=5,block=True)

@check.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()
    if plain_text:
        matcher.set_arg("host", args)

@check.got("host", prompt="IP?")
async def handle_host(host: Message = Arg(), host_name: str = ArgPlainText("host")):
  if "." not in host_name:
    await check.reject(host.template(lang_data[lang]["where_ip"]),at_sender=True)
  if len(host_name.strip().split(':')) == 2:
    if len(host_name.strip().split(':')[1]) > 5:
       await check.reject(lang_data[lang]["where_port"],at_sender=True)
  await get_info(host_name)

async def get_info(host_name: str):
    try:
        host = host_name.strip()
        ip = host.split(':')[0]
        try:
          port = host.split(':')[1]
          ms = MineStat(ip,int(port),timeout=1,resolve_srv=True)
        except:
          ms = MineStat(ip,timeout=1,resolve_srv=True)
        finally:
            if ms.online:
              if ms.connection_status == ConnStatus.SUCCESS:
                status = f'{ms.connection_status}|{lang_data[lang]["status_success"]}'
              elif ms.connection_status == ConnStatus.CONNFAIL:
                status = f'{ms.connection_status}|{lang_data[lang]["status_connfail"]}'
              elif ms.connection_status == ConnStatus.TIMEOUT:
                status = f'{ms.connection_status}|{lang_data[lang]["status_timeout"]}'
              elif ms.connection_status == ConnStatus.UNKNOWN:
                status = f'{ms.connection_status}|{lang_data[lang]["status_unknown"]}'
              if Config.get_config("mc_check", "JSON_JAVA"):
                result = f'\n{lang_data[lang]["version"]}{ms.version}\n{lang_data[lang]["slp_protocol"]}{ms.slp_protocol}\n{lang_data[lang]["address"]}{ms.address}\n{lang_data[lang]["port"]}{ms.port}\n{lang_data[lang]["delay"]}{ms.latency}ms\n{lang_data[lang]["motd"]}{ms.motd}\n{lang_data[lang]["players"]}{ms.current_players}/{ms.max_players}\n{lang_data[lang]["status"]}{status}\n'
              else:
                result = f'\n{lang_data[lang]["version"]}{ms.version}\n{lang_data[lang]["slp_protocol"]}{ms.slp_protocol}\n{lang_data[lang]["address"]}{ms.address}\n{lang_data[lang]["port"]}{ms.port}\n{lang_data[lang]["delay"]}{ms.latency}ms\n{lang_data[lang]["motd"]}{ms.stripped_motd}\n{lang_data[lang]["players"]}{ms.current_players}/{ms.max_players}\n{lang_data[lang]["status"]}{status}\n'
              # Bedrock specific attribute:
              #if ms.gamemode:
              if 'BEDROCK' in str(ms.slp_protocol):
                if Config.get_config("mc_check", "JSON_BDS"):
                  result = f'\n{lang_data[lang]["version"]}{ms.version}\n{lang_data[lang]["slp_protocol"]}{ms.slp_protocol}\n{lang_data[lang]["gamemode"]}{ms.gamemode}\n{lang_data[lang]["address"]}{ms.address}\n{lang_data[lang]["port"]}{ms.port}\n{lang_data[lang]["delay"]}{ms.latency}ms\n{lang_data[lang]["motd"]}{ms.motd}\n{lang_data[lang]["players"]}{ms.current_players}/{ms.max_players}\n{lang_data[lang]["status"]}{status}'
                else:
                  result = f'\n{lang_data[lang]["version"]}{ms.version}\n{lang_data[lang]["slp_protocol"]}{ms.slp_protocol}\n{lang_data[lang]["gamemode"]}{ms.gamemode}\n{lang_data[lang]["address"]}{ms.address}\n{lang_data[lang]["port"]}{ms.port}\n{lang_data[lang]["delay"]}{ms.latency}ms\n{lang_data[lang]["motd"]}{ms.stripped_motd}\n{lang_data[lang]["players"]}{ms.current_players}/{ms.max_players}\n{lang_data[lang]["status"]}{status}'
              # Send favicon
              if ms.favicon_b64 != None and ms.favicon_b64 != "":
                try:
                  base0 = str(ms.favicon_b64)
                  if base0 != None and base0 != '':
                    base = base0[22:]
                    img = base64.b64decode(base)
                except:
                  pass
                else:
                    result = Message ([
                    MessageSegment.text(f'{result}favicon:'),
                    MessageSegment.image(img)
                    ])
            else:
              result = lang_data[lang]["offline"]
        await check.send(Message(result), at_sender=True)
    except BaseException as e:
      error = f'ERROR:\n{format(e)}'
      logger.error(f'ERROR\n{format(e)}')
      await check.send(Message(error), at_sender=True)

@lang_change.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()
    if plain_text:
        matcher.set_arg("lang_", args)

@lang_change.got("lang_", prompt="Language?")
async def handle_host(lang_: Message = Arg(), language_name: str = ArgPlainText("lang_")):
  result = await change(language_name)
  await lang_change.finish(Message(result),at_sender=True)

async def change(language:str):
  global lang
  try:
    a = lang_data[language]
  except:
    return f'No language named "{language}"!'
  else:
    if language == lang:
      return f'The language is already "{language}"!'
    else:
      lang = language
      return f'Change to "{language}" success!'
    
@lang_now.handle()
async def _(bot: Bot, event: Event):
  await lang_now.send(Message(f' Language: {lang}.'),at_sender=True)
