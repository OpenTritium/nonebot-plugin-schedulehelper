# 智能的大学课程提示插件

使用本插件前，请配置好 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 与 [nonebot](https://v2.nonebot.dev/)，然后克隆本插件到用户插件目录（numbot/src/plugins）。

默认只测试过 archlinux 环境。

## 插件能力

- 使用 `课表` 命令式查询本周课表
- 使用 `课表<int>` 命令查询本学期第 `<int>` 周课表
- 早上定时提醒是否有早八
- 上课前自动提示什么课程，教室在哪里

## 软件依赖

- **wkhtmltopdf**（[预编译二进制文件下载](https://wkhtmltopdf.org/downloads.html)）
- **nonebot_plugin_apscheduler** （定时插件）
- **imgkit**（前者的 python 中间件）
- **rtoml** （toml 解析）
- **html-table** （html 生成）
- **nonebot** （QQ 机器人框架）

除了第一个，全都可以在 pip 中下载到。

为了使定时功能生效，你需要在 bot.py 中初始化该插件：

```python
nonebot.init(apscheduler_autostart=True)
nonebot.init(apscheduler_config={
    "apscheduler.timezone": "Asia/Shanghai"
})
```

## 插件配置

插件使用的是 toml 配置文件，名为 `config.toml`:

```toml
[settings]
# 你需要指定 wkhtmltoimage 二进制程序路径
imgkit_path = "/usr/bin/wkhtmltoimage"
# 上学期与下学期的开学日期
first_half_semester = "08-29"
second_half_semester = "02-28"
# 时间偏移量，通知会提前到 <int> 分钟
offset = 20

[time_set]
# 因为要遵循 toml 语法，故要精确到秒
schedule_1 = 08:40:00
schedule_2 = 10:30:00
schedule_3 = 14:00:00
schedule_4 = 15:40:00
schedule_5 = 18:20:00
schedule_6 = 20:00:00

[index]
# 课程索引表

[index.week_0]
# 周索引为 week_<int> 格式

[index.week_0.monday]
# 日索引，有效值为 <monday | tuesday | wednesday | thursday | friday | saturday | sunday>

[index.week_0.monday.class_3]
# 课索引为 class_<int> 格式
course = "课程名称"
room = "教室信息"
# 需要注意的是，即使你当天没有课程，也要保留对应的键
```
