import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np
import statsmodels.api as sm

grouped = pd.read_excel("../../output/excel/每年每种平台变化率平均值.xlsx")

# 设置中文字体
font_prop = FontProperties(fname=r"C:\Windows\Fonts\simhei.ttf")

# 创建折线图
plt.figure(figsize=(8, 3))

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

for platform in grouped['平台性质'].unique():
        color = platform_colors.get(platform, None)
        platform_data = grouped[grouped['平台性质'] == platform]
        plt.plot(platform_data['年份'], platform_data['变化率'], linestyle=line_styles.get(platform,None),label=platform, linewidth=2, color=color)


plt.axvline(x=2017, color="#000000", linestyle='--', alpha=0.7)
plt.axvline(x=2021, color="#000000", linestyle='--', alpha=0.7)

# 图表设置
plt.title("平台协议变化率平均数演变趋势（2012-2025）", fontproperties=font_prop,fontsize=10)
plt.xlabel("年份", fontproperties=font_prop,fontsize=10)
plt.ylabel("变化率", fontproperties=font_prop,fontsize=10)
plt.xticks(range(2012, 2026))  # 设置横坐标为每一年
plt.legend(prop=font_prop)
plt.grid(True, linestyle='--', alpha=0.7)

# 保存折线图
output_image = "../../output/img/平台协议变化率平均数演变趋势（2012-2025）.png"
plt.savefig(output_image, dpi=300)
print(f"带断点分析的折线图已保存到 {output_image}")

# 显示图表
plt.show()
