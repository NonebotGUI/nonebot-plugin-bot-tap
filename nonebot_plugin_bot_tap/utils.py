from PIL import Image, ImageDraw, ImageFont
import re
from io import BytesIO

def get_color_for_match(match):
    text = match.group(0)
    if text == '[SUCCESS]':
        return (0, 255, 0)
    elif text == '[INFO]':
        return (255, 255, 255)
    elif text == '[WARNING]':
        return (255, 165, 0)
    elif text == '[ERROR]':
        return (255, 0, 0)
    elif text == '[DEBUG]':
        return (173, 216, 230)
    elif text in ['nonebot |', 'uvicorn |']:
        return (0, 128, 0)
    elif text in ['Env: dev', 'Env: prod', 'Config']:
        return (255, 165, 0)
    elif text.startswith('nonebot_plugin_') or text.startswith('"nonebot_plugin_'):
        return (255, 255, 0)
    elif text.startswith('Loaded adapters:') or text.startswith('使用 Python:') or text.startswith('Using python:'):
        return (0, 255, 0)
    elif text.startswith('Calling API'):
        return (128, 0, 128)
    elif '-' in text and ':' in text:
        return (0, 128, 0)
    else:
        return (255, 255, 255)

def draw_img(text, font_path, font_size):
    font = ImageFont.truetype(font_path, font_size)
    max_width = 1765
    lines = []

    for paragraph in text.split('\n'):
        words = paragraph.split(' ')
        line = ''
        for word in words:
            test_line = f'{line} {word}'.strip()
            if font.getlength(test_line) <= max_width:
                line = test_line
            else:
                lines.append(line)
                line = word
        lines.append(line)

    line_count = len(lines)

    # 获取字体的行高
    _, _, _, line_height = font.getbbox("a")
    # 增加行距
    line_height += 3
    # 获取画布需要的高度
    height = line_height * line_count + 20
    image = Image.new('RGBA', (max_width, height), (31, 28, 28, 255))
    draw = ImageDraw.Draw(image)

    regex = re.compile(r'(\[[A-Z]+\])|(nonebot \|)|(uvicorn \|)|(Env: dev)|(Env: prod)|(Config)|(nonebot_plugin_[\S]+)|("nonebot_plugin_[\S]+)|(使用 Python: [\S]+)|(Using python: [\S]+)|(Loaded adapters: [\S]+)|(\d{2}-\d{2} \d{2}:\d{2}:\d{2})|(Calling API [\S]+)')

    y = 10

    for line in lines:
        matches = list(regex.finditer(line))
        last_end = 0
        x = 10

        for match in matches:
            if match.start() > last_end:
                draw.text((x, y), line[last_end:match.start()], font=font, fill=(255, 255, 255, 255))
                x += font.getlength(line[last_end:match.start()])

            color = get_color_for_match(match)
            draw.text((x, y), match.group(0), font=font, fill=color)
            x += font.getlength(match.group(0))

            last_end = match.end()

        if last_end < len(line):
            draw.text((x, y), line[last_end:], font=font, fill=(255, 255, 255, 255))

        y += line_height

    buffered = BytesIO()
    image.save(buffered, format="PNG")
    buffered.seek(0)

    return buffered
