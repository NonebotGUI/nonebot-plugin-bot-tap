<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-bot-tap

_✨ 在 NoneBot 中管理你的 NoneBot 吧！ ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/NonebotGUI/nonebot-plugin-bot-tap.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-bot-tap.svg">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-bot-tap.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">

</div>


## 📖 介绍

基于 [NoneBot Agent](https://github.com/NonebotGUI/nonebot-agent)的 NoneBot 插件，用于管理 NoneBot 机器人。

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-bot-tap

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-bot-tap
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-bot-tap
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-bot-tap
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-bot-tap
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_bot_tap"]

</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

| 配置项 | 必填 | 类型 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| bot_tap_token | 是 | str | None | 连接到Agent端的token |
| bot_tap_admin | 是 | list | [] | 权限组 |
| bot_tap_host | 否 | str | http://127.0.0.1 | 连接到Agent端的主机地址 |
| bot_tap_port | 否 | int | 2519 | 连接到Agent端的端口 |
| bot_tap_font_path | 否 | str | 自带的Microsoft_YaHei_Consolas_Regular.ttf | 字体文件路径 |
| bot_tap_font_size | 否 | int | 18 | 字体大小 |

> [!NOTE]
> 如果你的 `bot_tap_token` 为纯数字, 请在填写时多加上一层引号, 例如 `'"123456"'`

## 使用前请先配置好 Agent 端

点[这里](https://webui.nbgui.top/config/nba.html)查看配置方法，配置完成后可手动创建文件进行导入，也可以通过部署 [NoneBot WebUI](https://webui.nbgui.top/config/dashboard.html) 后快速导入，或者使用插件命令进行导入。

如果你想通过手动创建文件导入，请按照以下格式创建文件：

```json
{
    "name":"Bot名称",
    "path":"Bot路径(Windows请使用双反斜杠)",
    "time":"2025年1月5日12时34分32秒",
    "id":"uuid",
    "isRunning":false,
    "pid":"Null"
}
```
并将其保存在 Agent 端的 `bots` 文件夹下，文件名为 `uuid.json`，其中 `uuid` 为你为 Bot 设置的 `uuid`。


## 🎉 使用
/bot help 查看帮助

## 📑 支持的功能

- [X] Bot 列表
- [X] Bot 基本信息
- [X] Bot 启动/停止
- [X] Bot 日志
- [X] Bot 导入
- [X] 版本信息
- [ ] 插件启用/禁用
- [ ] 插件安装
- [ ] 插件卸载
- [ ] 插件列表
- [ ] 适配器安装
- [ ] 驱动器安装
- [ ] nbcli 本体管理