import sys
import os

# 添加目标路径到 sys.path
sys.path.append(os.path.abspath("../"))

# 导入模块
import utils  # 替换为模块的实际名称
import os 
# 二次清洗数据 每年每平台留存一份字数 并自动填充
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
# 1️⃣ 读取清洗后的协议数据
print("读取清洗后的协议数据...")
df = pd.read_excel("../../output/excel/协议数据汇总_清洗后.xlsx")

# 2️⃣ 时间字段转换为年份
df["年份"] = pd.to_datetime(df["时间"]).dt.year

# 平台名称列表
platform_terms = [
    "淘宝", "知乎", "新浪", "微博", "豆瓣", "微信", "抖音",
    "e家帮", "京东", "链家", "哔哩哔哩", "e家帮家政", "yy直播", "人民网", "优酷",
    "凤凰网", "唯品会", "喜马拉雅", "央视网", "快手", "我爱我家", "拼多多", "搜狗",
    "携程", "新浪微博", "晋江文学城", "滴滴", "滴答出行", "爱奇艺", "百度", "神州专车",
    "网易严选", "网易游戏", "美团外卖", "腾讯新闻", "腾讯视频", "起点中文网", "高德", "360"
]

result_data = []
for platform  in platform_terms:
    print(f"处理平台: {platform}")
    # 筛选包含此平台名称的数据
    platform_data = df[df['平台名称'].str.contains(platform, na=False)]

    if len(platform_data) == 0:
        print(f"  未找到'{platform}'平台的数据")
        continue

    begin_year = platform_data["年份"].min()

    last_record = None
    # 对于每一年
    for year in range(begin_year, 2026):  # 2010-2025
        # 获取当年该平台的数据
        year_data = platform_data[platform_data["年份"] == year]

        if len(year_data) > 0:
            # 如果当年有数据，取最晚的一条
            earliest_record = year_data.sort_values(by="时间").iloc[-1]
            result_data.append({
                "年份": year,
                "平台": platform,
                "平台性质": earliest_record["平台性质"],
                "内容": earliest_record["内容"],
                "字数": earliest_record["字数"]
            })
            last_record = earliest_record

        
result_df = pd.DataFrame(result_data)
result_df.to_excel("../../output/excel/协议数据汇总_每平台每年最晚一条.xlsx", index=False)