# 二次清洗数据 每年每平台留存一份字数 并自动填充
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import os

# 1️⃣ 读取清洗后的协议数据
print("读取清洗后的协议数据...")
median_word_count = pd.read_excel("../output/excel/字数_历年中位数.xlsx")


# 如果有缺失值，填充为0
median_word_count = median_word_count.fillna(0)

# 设置中文字体
font_prop = FontProperties(fname=r"C:\Windows\Fonts\simhei.ttf")

    # 为每个平台性质分配固定颜色
        # 为每个平台性质分配固定颜色
platform_colors = {
'信息资讯':  "#4d73b0",  # 浅薰衣草紫 # 冰川蓝
'网络销售':  "#F1B05F",  # 橘沙金
'社交娱乐': "#26A020",  # 牛油果绿,  # 柔淡紫
'生活服务':  "#F47E7E",  # 玫瑰红
}

# 为不同平台性质设置不同的线条样式
line_styles = {
    '信息资讯': '-',      # 实线
    '网络销售': '--',     # 虚线
    '社交娱乐': ':',      # 点线
    '生活服务': '-.'      # 点划线
}


# 绘图
plt.figure(figsize=(8,3))
for category in median_word_count.columns:
    if category != "年份":  # 排除"未知"类型
        # 使用指定颜色绘制折线，如果没有指定则使用默认颜色
        color = platform_colors.get(category, None)
        plt.plot(median_word_count['年份'], median_word_count[category], 
                  linewidth=2, label=category, color=color, linestyle=line_styles.get(category, '-'))

# 设置横坐标为每一年
years = range(2011, 2026)  # 2010 到 2025 年
plt.xticks(years, [str(year) for year in years], rotation=0)

plt.title("平台协议字数中位数演变趋势(2011-2025)", fontproperties=font_prop, fontsize=10)
plt.xlabel("年份", fontproperties=font_prop, fontsize=10)
plt.ylabel("协议字数中位数", fontproperties=font_prop, fontsize=10)
plt.legend(prop=font_prop)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

# 先保存图像
output_path = "../output/img/协议字数中位数趋势图.png"
plt.savefig(output_path, dpi=300, bbox_inches="tight")
print(f"✅ 图像已保存到: {output_path}")

# 最后显示图像
plt.show()