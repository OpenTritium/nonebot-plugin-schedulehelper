import re


class Parse:
    """用于处理配置文件，处理数据从而生成列表"""

    def __init__(self, config: dict):
        """初始化总时刻表，总课表索引，与设置

        Args:
            config (dict): 配置数据
        """
        self.current_week = None
        self.schedule = config["index"]
        self.time_set = config["time_set"]
        self.settings = config["settings"]

    def get_week(self, order: int) -> dict:
        """获取指定周数据

        Args:
            order (int): 周次

        Returns:
            dict: 指定周数据
        """
        index_str = "week_" + str(order)
        self.current_week = self.schedule[index_str]
        return self.current_week

    def get_day(self, order: int, day: str) -> dict:
        """获取指定日数据

        Args:
            order (int): 指定周次
            day (str): 指定星期几

        Returns:
            dict: 指定日数据
        """
        current_week = self.get_week(order)
        return current_week.get(day, None)

    def get_time_tuple(self) -> tuple:
        """获取格式化后的时刻字符串元组

        Returns:
            tuple: 时刻字符串元组
        """
        time_table = []
        for i in range(1, 7):
            index_str = "schedule_" + str(i)
            raw_time = self.time_set[index_str]
            formatted_time = re.match(r"[0-9]{2}:[0-9]{2}", str(raw_time))
            time_table.append(formatted_time.group())
        return tuple(time_table)

    def gen_perday_course_tuple(self, order: int, day: str) -> tuple:
        """生成指定天的课表

        Args:
            order (int): 指定周次
            day (str): 指定星期几

        Returns:
            tuple: 包含 None 元素的指定日课程元组
        """
        current_day = self.get_day(order, day)
        clist = []
        for i in range(1, 7):
            index_str = "class_" + str(i)
            clist.append(current_day.get(index_str, None))
        return tuple(clist)

    def gen_perweek_course_tuple(self, order: int) -> tuple:
        """生成指定周课表

        Args:
            order (int): 指定周次

        Returns:
            tuple: 包含 None 元素的指定周课程元组
        """
        week_tuple = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")
        clist = [self.gen_perday_course_tuple(order, i) for i in week_tuple]
        return tuple(clist)
