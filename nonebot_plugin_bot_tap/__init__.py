from io import BytesIO
from nonebot import on_command, logger, require, get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot.params import CommandArg
from nonebot.rule import to_me
from .config import Config
from nonebot.adapters import Message
require("nonebot_plugin_saa")
require("nonebot_plugin_session")
from nonebot_plugin_session import SessionId, SessionIdType
from nonebot.plugin import inherit_supported_adapters
import httpx
from nonebot_plugin_saa import Image, Text
from .utils import draw_img
config = get_plugin_config(Config)

__plugin_meta__ = PluginMetadata(
    name="BotTap",
    description="✨在 NoneBot 中管理你的 NoneBot 吧！✨",
    usage="/bot help查看完整帮助",
    type="application",
    homepage="https://github.com/NonebotGUI/nonebot-plugin-bot-tap",
    config=Config,
    supported_adapters=inherit_supported_adapters("nonebot_plugin_session", "nonebot_plugin_saa"),
)


# 读取配置
admin = config.bot_tap_admin
host = config.bot_tap_host
port = config.bot_tap_port
token = str(config.bot_tap_token)
font_path = config.bot_tap_font_path
font_size = config.bot_tap_font_size


if not token:
    logger.error("请设置 Token！")



bot_tap_help = on_command("bot", aliases={'bot help'}, priority=1, block=False)
bot_tab_getid = on_command("bot getid", priority=1, block=False)
bot_tap_list = on_command("bot list", priority=1, block=False)
bot_tap_info = on_command("bot info", priority=1, block=False)
bot_tap_log = on_command("bot log", priority=1, block=False)
bot_tap_run = on_command("bot run", priority=1, block=False)
bot_tap_stop = on_command("bot stop", priority=1, block=False)
bot_tap_restart = on_command("bot restart", priority=1, block=False)
bot_tab_status = on_command("bot status", priority=1, block=False)
bot_tap_import = on_command("bot import", priority=1, block=False)



@bot_tap_help.handle()
async def handle():
    help = """
/bot getid - 获取当前会话下的用户ID
/bot help - 查看帮助
/bot list - 查看所有 Bot
/bot info id - 查看 Bot 信息
/bot run id - 运行 Bot
/bot stop id - 停止 Bot
/bot restart id - 重启 Bot
/bot log id - 查看 Bot 日志
/bot import name path - 导入 Bot
/bot status - 查看Agent端状态
"""
    await bot_tap_help.finish(help)


@bot_tab_getid.handle()
async def handle(uid: str = SessionId(SessionIdType.USER)):
    await Text(uid).finish(reply=True)

@bot_tap_list.handle()
async def handle(uid: str = SessionId(SessionIdType.USER)):
    if uid not in admin:
        await Text("你还没有权限，请使用/bot getid拿到id后联系管理员添加").finish(reply=True)
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{host}:{port}/nbgui/v1/bot/list", headers={"Authorization": f"Bearer {token}"})
        names = []
        for i in r.json():
            names.append(i["name"])

        formatted_names = [f"{index + 1}.{name}" for index, name in enumerate(names)]
        result = "\n".join(formatted_names)
        await Text('Bot 列表：\n' + result).finish(reply=True)

@bot_tap_info.handle()
async def handle(uid: str = SessionId(SessionIdType.USER), id: Message = CommandArg()):
    if uid not in admin:
        await Text("你还没有权限，请使用/bot getid拿到id后联系管理员添加").finish(reply=True)
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{host}:{port}/nbgui/v1/bot/list", headers={"Authorization": f"Bearer {token}"})
        bot_list = r.json()
        id = int(str(id).strip())
        if id < 1 or id > len(bot_list):
            await Text("无效的ID，请检查后重试").finish(reply=True)
        bot = bot_list[id - 1]
        name = bot["name"]
        status = bot["isRunning"]
        pid = bot["pid"]
        time = bot["time"]
        uuid = bot["id"]
        res = f"Bot 信息：\n名称：{name}\n状态：{'运行中' if status else '未运行'}\nPID：{pid}\n创建时间：{time}\nUUID：{uuid}"
        await Text(res).finish(reply=True)


@bot_tap_log.handle()
async def handle(uid: str = SessionId(SessionIdType.USER), id: Message = CommandArg()):
    if uid not in admin:
        await Text("你还没有权限，请使用/bot getid拿到id后联系管理员添加").finish(reply=True)
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{host}:{port}/nbgui/v1/bot/list", headers={"Authorization": f"Bearer {token}"})
        bot_list = r.json()
        id = int(str(id).strip())
        if id < 1 or id > len(bot_list):
            await Text("无效的ID，请检查后重试").finish(reply=True)
        bot = bot_list[id - 1]
        id = bot["id"]
        r = await client.get(f"{host}:{port}/nbgui/v1/bot/log/{id}", headers={"Authorization": f"Bearer {token}"})
        log = r.text
        img_bytesIO = draw_img(log, font_path, font_size)
        await Image(img_bytesIO).finish(reply=True)

@bot_tap_run.handle()
async def handle(uid: str = SessionId(SessionIdType.USER), id: Message = CommandArg()):
    if uid not in admin:
        await Text("你还没有权限，请使用/bot getid拿到id后联系管理员添加").finish(reply=True)
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{host}:{port}/nbgui/v1/bot/list", headers={"Authorization": f"Bearer {token}"})
        bot_list = r.json()
        id = int(str(id).strip())
        if id < 1 or id > len(bot_list):
            await Text("无效的ID，请检查后重试").finish(reply=True)
        bot = bot_list[id - 1]
        id = bot["id"]
        r = await client.post(f"{host}:{port}/nbgui/v1/bot/run/{id}", headers={"Authorization": f"Bearer {token}"})
        await Text("Bot 已启动").finish(reply=True)


@bot_tap_stop.handle()
async def handle(uid: str = SessionId(SessionIdType.USER), id: Message = CommandArg()):
    if uid not in admin:
        await Text("你还没有权限，请使用/bot getid拿到id后联系管理员添加").finish(reply=True)
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{host}:{port}/nbgui/v1/bot/list", headers={"Authorization": f"Bearer {token}"})
        bot_list = r.json()
        id = int(str(id).strip())
        if id < 1 or id > len(bot_list):
            await Text("无效的ID，请检查后重试").finish(reply=True)
        bot = bot_list[id - 1]
        id = bot["id"]
        r = await client.post(f"{host}:{port}/nbgui/v1/bot/stop/{id}", headers={"Authorization": f"Bearer {token}"})
        await Text("Bot 已停止").finish(reply=True)


@bot_tap_restart.handle()
async def handle(uid: str = SessionId(SessionIdType.USER), id: Message = CommandArg()):
    if uid not in admin:
        await Text("你还没有权限，请使用/bot getid拿到id后联系管理员添加").finish(reply=True)
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{host}:{port}/nbgui/v1/bot/list", headers={"Authorization": f"Bearer {token}"})
        bot_list = r.json()
        id = int(str(id).strip())
        if id < 1 or id > len(bot_list):
            await Text("无效的ID，请检查后重试").finish(reply=True)
        bot = bot_list[id - 1]
        id = bot["id"]
        r = await client.post(f"{host}:{port}/nbgui/v1/bot/restart/{id}", headers={"Authorization": f"Bearer {token}"})
        await Text("Bot 已重启").finish(reply=True)

@bot_tab_status.handle()
async def handle(uid: str = SessionId(SessionIdType.USER)):
    if uid not in admin:
        await Text("你还没有权限，请使用/bot getid拿到id后联系管理员添加").finish(reply=True)
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{host}:{port}/nbgui/v1/system/status", headers={"Authorization": f"Bearer {token}"})
        status = r.json()
        cpu_usage = status["cpu_usage"]
        ram_usage = status["ram_usage"]
        r = await client.get(f"{host}:{port}/nbgui/v1/system/platform", headers={"Authorization": f"Bearer {token}"})
        platform = r.json()["platform"]
        r = await client.get(f"{host}:{port}/nbgui/v1/version", headers={"Authorization": f"Bearer {token}"})
        version = r.json()["version"]
        nbcli = r.json()["nbcli"]
        python = r.json()["python"]
        res = f"Agent 端状态：\nCPU 使用率：{cpu_usage}\n内存使用率：{ram_usage}\n平台：{platform}\n版本：{version}\nNoneBot CLI：{nbcli}\nPython：{python}"
        await Text(res).finish(reply=True)

@bot_tap_import.handle()
async def handle(uid: str = SessionId(SessionIdType.USER), args: Message = CommandArg()):
    if uid not in admin:
        await Text("你还没有权限，请使用/bot getid拿到id后联系管理员添加").finish(reply=True)
    async with httpx.AsyncClient() as client:
        args = str(args).split()
        if len(args) != 2:
            await Text("参数错误，请检查后重试").finish(reply=True)
        name = args[0]
        path = args[1]
        data = {
            "name": name,
            "path": path
        }
        data = str(data).replace('\n','\\n').replace("'","\"").replace('"','\"')
        r = await client.post(f"{host}:{port}/nbgui/v1/bot/import", headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, data=data)
        if r.status_code == 200:
            await Text("导入成功").finish(reply=True)
        else:
            await Text("导入失败").finish(reply=True)