# 智能的大学课程提示插件

## 插件能力

- 使用 `课表` 命令式查询本周课表
- 使用 `课表<int>` 命令查询本学期第 `<int>` 周课表
- 早上定时提醒是否有早八
- 上课前自动提示什么课程，教室在哪里（开发中）
- 自动爬取喜鹊儿课表（待开发）

## 软件依赖

- **wkhtmltopdf**（[预编译二进制文件下载](https://wkhtmltopdf.org/downloads.html)）
- **imgkit**（前者的 python 中间件）
- **rtoml** （toml 解析）
- **html-table** （html 生成）
- **nonebot** （QQ 机器人框架）

## 插件配置

插件使用的是 toml 配置文件，名为 `config.toml`:

```toml
[settings]
# 你需要指定 wkhtmltoimage 二进制程序路径
imgkit_path = "/usr/bin/wkhtmltoimage"
# 上半学期为 true，下半学期为 false
first_half_semester = "08-29"
second_half_semester = "02-28"
# 时间偏移量，通知会提前到 <int> 分钟
offset = 20

[time_set]
# 因为要遵循 toml 语法，故要精确到时间
schedule_1 = 08:40:00
schedule_2 = 10:30:00
schedule_3 = 14:00:00
schedule_4 = 15:40:00
schedule_5 = 18:20:00
schedule_6 = 20:00:00

[index]
# 课程索引表
# 体现在 python 里就是 keys

[index.week_0]
#周索引为 week_<int> 格式

[index.week_0.monday]
#日索引，有效值为 <monday | tuesday | wednesday | thursday | friday | saturday | sunday>

[index.week_0.monday.class_3]
#课索引为 class_<int> 格式
course = "离散数学"
room = "教1-424"
```

