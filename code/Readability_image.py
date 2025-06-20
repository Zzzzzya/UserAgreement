import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
# 读取生成的表格
input_file = "../output/excel/协议数据汇总_可读性分析.xlsx"
df = pd.read_excel(input_file)
df["年份"] = pd.to_datetime(df["时间"]).dt.year
df = df[(df["年份"] >= 2015) & (df["年份"] <= 2025)]
# 确保必要的列存在
required_columns = ['年份', '平台性质', 'r1', 'r2', 'r3']
for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"输入的 Excel 文件中没有找到 '{col}' 列")

# 按“年份”和“平台性质”分组，计算 r1, r2, r3 的平均值
grouped = df.groupby(['年份', '平台性质'])[['r1', 'r2', 'r3']].mean().reset_index()

# 增加“生活服务”2015年的数据，使其等于2016年的值
life_service_2016 = grouped[(grouped['年份'] == 2016) & (grouped['平台性质'] == '生活服务')]
if not life_service_2016.empty:
    life_service_2015 = life_service_2016.copy()
    life_service_2015['年份'] = 2015
    grouped = pd.concat([grouped, life_service_2015], ignore_index=True)

grouped = grouped.sort_values(by=['年份', '平台性质']).reset_index(drop=True)

# 将 grouped 数据保存为 Excel 文件
output_grouped_file = "../output/excel/可读性_历年平均值.xlsx"
grouped.to_excel(output_grouped_file, index=False)
print(f"分组后的数据已保存到 {output_grouped_file}")

# 设置中文字体
font_prop = FontProperties(fname=r"C:\Windows\Fonts\simhei.ttf")

# 创建折线图
def plot_metric(metric, title, output_path):
    plt.figure(figsize=(10, 6))
    for platform in grouped['平台性质'].unique():
        platform_data = grouped[grouped['平台性质'] == platform]
        plt.plot(platform_data['年份'], platform_data[metric], marker='o', label=platform)
    plt.title(title,fontproperties=font_prop)
    plt.xlabel('年份',fontproperties=font_prop)
    plt.ylabel(metric,fontproperties=font_prop)
    plt.xticks(range(2015, 2026))
    plt.legend(prop=font_prop)
    plt.grid(True)
    plt.savefig(output_path)
    plt.close()

# 绘制 r1, r2, r3 的折线图
plot_metric('r1', '每年每种平台性质的 r1 平均值', '../output/img/r1_avg_plot.png')
plot_metric('r2', '每年每种平台性质的 r2 平均值', '../output/img/r2_avg_plot.png')
plot_metric('r3', '每年每种平台性质的 r3 平均值', '../output/img/r3_avg_plot.png')

print("折线图已生成并保存到 ../output/img/")