from datetime import datetime
from os import path

import rtoml

from .parse_config import Parse

current_path = path.abspath(__file__)
current_dir = path.dirname(current_path)
config = rtoml.load(open(current_dir + "/config.toml", "r"))
scheme = Parse(config)


def get_week_order() -> int:
    """智能匹配学期，获取当前周次

    Returns:
        int: 当前周次
    """
    global scheme
    semester_strings = (scheme.settings["first_half_semester"], scheme.settings["second_half_semester"])
    semester_indicator = tuple(datetime.strptime(d_str, "%Y-%m-%d") for d_str in
                               [str(datetime.now().year) + "-" + d_str for d_str in semester_strings])
    current_beginning = None
    if current_month := datetime.now().month in (8, 9, 10, 11, 12, 1):
        current_beginning = semester_indicator[0]
    elif current_month in (2, 3, 4, 5, 6, 7):
        current_beginning = semester_indicator[1]
    today = datetime.today()
    diff_days = (today - current_beginning).days
    return diff_days // 7 + 1
