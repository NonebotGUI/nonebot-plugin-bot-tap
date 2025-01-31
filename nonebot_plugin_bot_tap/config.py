from pydantic import BaseModel
from os import path

class Config(BaseModel):

    # Agent 端地址
    bot_tap_host: str = "http://127.0.0.1"

    # 端口
    bot_tap_port: int = 2519

    # Token
    bot_tap_token: str = ""

    # 管理员
    bot_tap_admin: list = []

    # 字体文件路径
    bot_tap_font_path: str = str(
        path.join(path.dirname(path.abspath(__file__)), "Microsoft_YaHei_Consolas_Regular.ttf")
    )

    # 字体大小
    bot_tap_font_size: int = 18