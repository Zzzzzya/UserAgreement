import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
# 读取生成的表格
input_file = "../output/excel/协议数据汇总_可读性分析.xlsx"
df = pd.read_excel(input_file)
df["年份"] = pd.to_datetime(df["时间"]).dt.year
df = df[(df["年份"] >= 2011) & (df["年份"] <= 2025)]
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
    plt.figure(figsize=(8, 3))
    for platform in grouped['平台性质'].unique():
        color = platform_colors.get(platform, None)
        platform_data = grouped[grouped['平台性质'] == platform]
        plt.plot(platform_data['年份'], platform_data[metric], linestyle=line_styles.get(platform,None),label=platform, linewidth=2, color=color)
    plt.title(title,fontproperties=font_prop,fontsize=10)
    plt.xlabel('年份',fontproperties=font_prop,fontsize=10)
    plt.ylabel('可读性',fontproperties=font_prop,fontsize=10)
    plt.xticks(range(2011, 2026))
    plt.legend(prop=font_prop,framealpha=0.7)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.show()
    

# 绘制 r1, r2, r3 的折线图
plot_metric('r3', '平台协议可读性平均数演变趋势（2011-2025）', '../output/img/r3_avg_plot.png')


print("折线图已生成并保存到 ../output/img/")