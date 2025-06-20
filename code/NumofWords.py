# 二次清洗数据 每年每平台留存一份字数 并自动填充
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import os

# 1️⃣ 读取清洗后的协议数据
print("读取清洗后的协议数据...")
df = pd.read_excel("../output/excel/协议数据汇总_清洗后.xlsx")

# 2️⃣ 时间字段转换为年份
df["年份"] = pd.to_datetime(df["时间"]).dt.year

# 3️⃣ 筛选合理年份区间（2015-2025）
df = df[(df["年份"] >= 2015) & (df["年份"] <= 2025)]

# 平台名称列表
platform_terms = [
    "淘宝", "知乎", "新浪", "微博", "豆瓣", "微信", "网易", "抖音",
    "e家帮", "京东", "链家", "哔哩哔哩", "e家帮家政", "yy直播", "人民网", "优酷",
    "凤凰网", "唯品会", "喜马拉雅", "央视网", "快手", "我爱我家", "拼多多", "搜狗",
    "携程", "新浪微博", "晋江文学城", "滴滴", "滴答出行", "爱奇艺", "百度", "神州专车",
    "网易严选", "网易游戏", "美团外卖", "腾讯新闻", "腾讯视频", "起点中文网", "高德", "360"
]

# 年份范围
years_range = list(range(2015, 2026))  # 2015-2025

print(f"开始处理{len(platform_terms)}个平台的数据...")

# 创建结果数据列表
result_data = []

# 遍历每个平台
for platform in platform_terms:
    print(f"处理平台: {platform}")
    # 筛选包含此平台名称的数据
    platform_data = df[df['平台名称'].str.contains(platform, na=False)]
    
    if len(platform_data) == 0:
        print(f"  未找到'{platform}'平台的数据")
        # 没有数据的平台，每年添加一条字数为0的记录
        for year in years_range:
            result_data.append({
                "年份": year,
                "平台": platform,
                "平台性质": "未知",
                "字数": 0
            })
        continue
        
    # 对于每一年
    for year in years_range:
        # 获取当年该平台的数据
        year_data = platform_data[platform_data["年份"] == year]
        
        if len(year_data) > 0:
            # 如果当年有数据，取最早的一条
            earliest_record = year_data.sort_values(by="时间").iloc[0]
            result_data.append({
                "年份": year,
                "平台": platform,
                "平台性质": earliest_record["平台性质"],
                "字数": earliest_record["字数"]
            })
        else:
            # 如果当年没数据，向前找最近的年份
            previous_years = [y for y in years_range if y < year]
            previous_years.sort(reverse=True)  # 从近到远排序
            
            found = False
            for prev_year in previous_years:
                prev_data = platform_data[platform_data["年份"] == prev_year]
                if len(prev_data) > 0:
                    # 找到之前年份的最早记录
                    earliest_record = prev_data.sort_values(by="时间").iloc[0]
                    result_data.append({
                        "年份": year,
                        "平台": platform,
                        "平台性质": earliest_record["平台性质"],
                        "字数": earliest_record["字数"]
                    })
                    found = True
                    break
            
            if not found:
                # 如果之前都没有记录，字数为0
                # 使用该平台的主要性质分类
                if len(platform_data) > 0:
                    platform_type = platform_data["平台性质"].mode().iloc[0]
                else:
                    platform_type = "未知"
                    
                result_data.append({
                    "年份": year,
                    "平台": platform,
                    "平台性质": platform_type,
                    "字数": 0
                })

# 创建整理后的DataFrame
result_df = pd.DataFrame(result_data)

# 确保输出目录存在
os.makedirs("../output/excel", exist_ok=True)
os.makedirs("../output/img", exist_ok=True)

# 保存到Excel
output_excel_path = "../output/excel/协议数据_按年份平台整理.xlsx"
result_df.to_excel(output_excel_path, index=False)
print(f"✅ 数据已保存到: {output_excel_path}")

filtered_df = result_df[result_df["字数"] > 0]  # 过滤掉字数为0的记录
median_word_count = filtered_df.groupby(["年份", "平台性质"])["字数"].median().unstack()


# 将 grouped 数据保存为 Excel 文件
output_grouped_file = "../output/excel/字数_历年中位数.xlsx"
median_word_count.to_excel(output_grouped_file, index=False)
print(f"分组后的数据已保存到 {output_grouped_file}")

# 如果有缺失值，填充为0
median_word_count = median_word_count.fillna(0)

# 设置中文字体
font_prop = FontProperties(fname=r"C:\Windows\Fonts\simhei.ttf")

# 绘图
plt.figure(figsize=(14, 7))
for category in median_word_count.columns:
    if category != "未知":  # 排除"未知"类型
        plt.plot(median_word_count.index, median_word_count[category], marker='o', linewidth=2, label=category)

# 设置横坐标为每一年
years = median_word_count.index.tolist()
plt.xticks(years, [str(year) for year in years], rotation=0)

plt.title("2015–2025 各类平台协议字数中位数变化趋势", fontproperties=font_prop, fontsize=16)
plt.xlabel("年份", fontproperties=font_prop, fontsize=12)
plt.ylabel("协议字数中位数", fontproperties=font_prop, fontsize=12)
plt.legend(prop=font_prop)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

# 先保存图像
output_path = "../output/img/协议字数中位数趋势图.png"
plt.savefig(output_path, dpi=300, bbox_inches="tight")
print(f"✅ 图像已保存到: {output_path}")

# 最后显示图像
plt.show()