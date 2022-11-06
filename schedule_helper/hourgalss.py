from datetime import datetime, timedelta
from os import path

import rtoml

from .parse_config import Parse

# 获取绝对路经
current_path = path.abspath(__file__)
current_dir = path.dirname(current_path)
# 导入配置，生成配置对象
config = rtoml.load(open(current_dir + "/config.toml", "r"))
scheme = Parse(config)


def get_week_order() -> int:
    """智能匹配学期，获取当前周次

    Returns:
        int: 当前周次
    """
    # 获取两个学期的开学时间
    semester_strings = (scheme.settings["first_half_semester"], scheme.settings["second_half_semester"])
    # 生成当前年的开学时间，由元组类型包裹
    semester_indicator = tuple(datetime.strptime(d_str, "%Y-%m-%d") for d_str in
                               [str(datetime.now().year) + "-" + d_str for d_str in semester_strings])
    current_beginning = None
    # 获取当前月份，来判断使用那个开学时间
    if current_month := datetime.now().month in (8, 9, 10, 11, 12, 1):
        current_beginning = semester_indicator[0]
    elif current_month in (2, 3, 4, 5, 6, 7):
        current_beginning = semester_indicator[1]
    # 计算周数
    today = datetime.today()
    diff_days = (today - current_beginning).days
    return diff_days // 7 + 1


def today_in_week() -> str:
    """获取今天星期几

    Returns:
        str: "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday" 中的其一
    """
    current_day = datetime.today()
    current_week_day = current_day.weekday()
    week_tuple = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")
    index_str = week_tuple[current_week_day]
    return index_str


def good_morning() -> bool:
    """早八函数，判断每天是否存在第一节课，来决定返回值

    Returns:
        bool: 早上是否有课
    """
    index_str = today_in_week()
    current_day_source = scheme.get_day(get_week_order(), index_str)
    # 检查器，若存在第一节课则返回其内容，不存在返回 None
    if current_day_source.get("class_1", None):
        return True
    else:
        return False


def ring_bell() -> tuple:
    """获取上课时间点

    Returns:
        tuple: 形式如同 ((<int>,<int>)…)，每个被包裹的元组里依次是小时与分钟
    """
    time_list = [scheme.time_set[f"schedule_{d}"] for d in range(1, 7)]
    time_convert = [(moment.hour, moment.minute) for moment in time_list]
    return tuple(time_convert)


def course_reflection() -> bool | str:
    """根据当前时间返回即将开始的课程

    Returns:
        str: 课程信息，包括课程名与教室
    """
    delta_time = datetime.now() + timedelta(minutes=scheme.settings["offset"])
    hour = delta_time.hour
    minute = delta_time.minute
    delta_tuple = (hour, minute)
    ring_times = ring_bell()
    course_hour_point = course_minute_point = None
    for moment in ring_times:
        # 判断小时
        if moment[0] == delta_tuple[0]:
            course_hour_point = moment[0]
            course_minute_point = moment[1]
    if course_hour_point is None:
        return False
    else:
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
        today_course = scheme.get_day(order=week_order, day=week_day_index)
        # 初始化课程信息
        course_info = ""
        # 获取当前时间点课程
        if current_course := today_course.get(index_str, None):
            course_info = str(current_course.get("course")) + "\n" + str(current_course.get("room"))
        return course_info
