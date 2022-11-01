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


def today_in_week() -> str:
    current_day = datetime.today()
    current_week_day = current_day.weekday()
    week_tuple = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")
    index_str = week_tuple[current_week_day]
    return index_str


def good_morning() -> bool:
    index_str = today_in_week()
    current_day_source = scheme.get_day(get_week_order(), index_str)
    # 检查器，若存在第一节课则返回其内容，不存在返回 None
    if current_day_source.get("class_1", None):
        return True
    else:
        return False


def ring_bell() -> tuple:
    time_list = [scheme.time_set[f"schedule_{d}"] for d in range(1, 7)]
    time_convert = [(moment.hour, moment.minute) for moment in time_list]
    return tuple(time_convert)


def course_reflection() -> tuple:
    hour = datetime.now().hour
    minute = datetime.now().minute
    now_tuple = (hour, minute)
    ring_times = ring_bell()
    course_hour_point = course_minute_point = None
    for moment in ring_times:
        if moment[0] < now_tuple[0]:
            course_hour_point = moment[0]
            course_minute_point = moment[1]
    if course_minute_point < 10:
        course_minute_point = "0" + str(course_minute_point)
    if course_hour_point < 10:
        course_hour_point = "0" + str(course_hour_point)
    formatted_time = f"{course_hour_point}:{course_minute_point}"
    time_tuple = scheme.get_time_tuple()
    index_str = ""
    for i in range(0, 6):
        time_str = time_tuple[i]
        if time_str.startswith(formatted_time):
            index_str = "class_" + str(i + 1)
    week_order = get_week_order()
    week_day_index = today_in_week()
    today_cource = scheme.get_day(order=week_order, day=week_day_index)
    return today_cource.get(index_str, None)
