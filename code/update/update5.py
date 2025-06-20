import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 读取清洗后的协议数据
df = pd.read_excel("../../output/excel/协议数据汇总_每平台每年相似度.xlsx")

# 过滤掉“相似度”为 0 的数据
filtered_df = df[df["相似度"] > 0]

# 按“年份”和“平台性质”分组，计算“相似度”的平均值
grouped = filtered_df.groupby(["年份", "平台性质"])["相似度"].median().reset_index()

# 保存结果为 Excel 文件
output_file = "../../output/excel/每年每种平台相似度平均值.xlsx"
grouped.to_excel(output_file, index=False)
print(f"每年每种平台的相似度平均值已保存到 {output_file}")

# 设置中文字体
font_prop = FontProperties(fname=r"C:\Windows\Fonts\simhei.ttf")

# 创建折线图
plt.figure(figsize=(12, 6))
for platform in grouped["平台性质"].unique():
    platform_data = grouped[grouped["平台性质"] == platform]
    plt.plot(platform_data["年份"], platform_data["相似度"], marker='o', label=platform)

# 图表设置
plt.title("每年每种平台的相似度平均值", fontproperties=font_prop)
plt.xlabel("年份", fontproperties=font_prop)
plt.ylabel("相似度", fontproperties=font_prop)
plt.xticks(range(2010, 2026))  # 设置横坐标为每一年
plt.legend(prop=font_prop)
plt.grid(True)

# 保存折线图
output_image = "../../output/img/每年每种平台相似度平均值.png"
plt.savefig(output_image)
print(f"折线图已保存到 {output_image}")

# 显示图表
plt.show()