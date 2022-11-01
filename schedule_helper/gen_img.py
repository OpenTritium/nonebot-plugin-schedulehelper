from os import path, makedirs

import imgkit
import rtoml
from HTMLTable import HTMLTable

from .parse_config import Parse


def create_rows(time_tuple: tuple, week_tuple: tuple) -> tuple:
    """创建数据表（嵌套元组）

    Args:
        time_tuple (tuple): 时刻元组
        week_tuple (tuple): 周课程元组

    Returns:
        tuple: 数据元组
    """
    rows = []
    for j in range(0, 6):
        temp_top = [str(j + 1)]
        temp_bottom = [time_tuple[j]]
        for i in range(0, 7):
            if week_tuple[i][j] is None:
                temp_top.append(None)
                temp_bottom.append(None)
            else:
                temp_top.append(week_tuple[i][j]["course"])
                temp_bottom.append(week_tuple[i][j]["room"])
        rows.append(tuple(temp_top))
        rows.append(tuple(temp_bottom))
    return tuple(rows)


def gen_week_img(order=1) -> bool:
    """生成周课程图片

    Args:
        order (int, optional): 周次. Defaults to 1.

    Returns:
        bool: 用于返回图片是否生成
    """
    current_path = path.abspath(__file__)
    current_dir = path.dirname(current_path)
    config = rtoml.load(open(current_dir + "/config.toml", "r"))
    scheme = Parse(config)
    time_tuple = scheme.get_time_tuple()
    week_tuple = scheme.gen_perweek_course_tuple(order - 1)
    table = HTMLTable(caption=f"第{order}周课表")
    form_header = (("时间/节数", "周一", "周二", "周三", "周四", "周五", "周六", "周日"),)
    table.append_header_rows(form_header)
    table.append_data_rows(create_rows(time_tuple, week_tuple))
    # 标题样式
    table.caption.set_style({
        'font-size': '24px',
        'background-color': '#131124',
        'color': '#e2e1e4',
    })
    # 表格样式
    table.set_style({
        'border-collapse': 'collapse',
        'word-break': 'keep-all',
        'white-space': 'nowrap',
        'font-size': '14px',
        'color': '#ccccd6',
        'background-color': '#74759b',
        'text-align': 'center',
    })
    # 单元格样式
    table.set_cell_style({
        'border-color': '#131124',
        'border-width': '3px',
        'border-style': 'solid',
        'padding': '5px',
    })
    # 表头样式
    table.set_header_row_style({
        'color': '#ccccd6',
        'background-color': '#302f4b',
        'font-size': '18px',
    })
    # 覆盖表头样式
    table.set_header_cell_style({
        'padding': '15px',
    })
    for i in range(1, 13):
        if i in (1, 2, 5, 6, 9, 10,):
            table[i].set_cell_style({
                'background-color': '#a7a8bd',
                'color': '#322f3b',
                'font-weight': 'bold',
            })
    html = table.to_html()
    imgkit_path = scheme.settings["imgkit_path"]
    options = {
        "encoding": "UTF-8",
        "quality": "30",
        "width": "920"
    }
    cache_dir = str(current_dir) + "/tmp"
    # 图片缓存目录不存在时，创建它
    if not path.exists(cache_dir):
        makedirs(cache_dir)
    img_path = str(current_dir) + "/tmp/" + f"{order}_week.jpg"
    cfg = imgkit.config(wkhtmltoimage=imgkit_path)
    # 生成图片
    if imgkit.from_string(html, img_path, options=options, config=cfg):
        return True
