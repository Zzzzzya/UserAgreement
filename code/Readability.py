import cntext as ct
import pandas as pd

# 读取原始 Excel 文件
input_file = "../output/excel/协议数据汇总_清洗后.xlsx"
output_file = "../output/excel/协议数据汇总_可读性分析.xlsx"

df = pd.read_excel(input_file)

# 确保“内容”列存在
if '内容' not in df.columns:
    raise ValueError("输入的 Excel 文件中没有找到 '内容' 列")

# 初始化新列
df['r1'] = None
df['r2'] = None
df['r3'] = None

# 遍历每一行，计算可读性评分
for index, row in df.iterrows():
    content = row['内容']
    if pd.notnull(content):  # 确保内容不为空
        readability_scores = ct.readability(content, lang='chinese')
        df.at[index, 'r1'] = readability_scores['readability1']
        df.at[index, 'r2'] = readability_scores['readability2']
        df.at[index, 'r3'] = readability_scores['readability3']
        print(f"处理第 {index + 1} 行: r1={readability_scores['readability1']}, r2={readability_scores['readability2']}, r3={readability_scores['readability3']}")

# 将结果保存到新的 Excel 文件
df.to_excel(output_file, index=False)
print(f"可读性分析已完成，结果保存到 {output_file}")