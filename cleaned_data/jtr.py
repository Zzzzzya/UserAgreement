#可以跑通，但需要在终端中跑
#下次记得先【清洗】一下数据，把一些符号（URL格式）统一，避免遇到全角符号就崩溃的情况……

import os
import time
import pandas as pd
from readability_cn import ChineseReadability
from multiprocessing import Pool, cpu_count

# ===== 设置路径和文件 =====
input_file = "/Users/jitianran/Desktop/jtr/cleaned_data/协议数据汇总_清洗后.xlsx"
output_file = "/Users/jitianran/Desktop/jtr/cleaned_data/协议文本_可读性分析结果_multiprocessing.xlsx"
batch_size = 5  # 每批处理 5 条
num_workers = min(cpu_count(), 4)  # 设置最多使用的核数（保守选择）

# ===== 初始化分析器，用于获取自定义词表 =====
base_readability = ChineseReadability()
custom_words = [
    "知乎", "淘宝", "微信", "抖音", "京东", "新浪微博", "优酷", "拼多多", "快手", "美团外卖",
    "平台", "公司", "我们", "豆瓣", "网易", "e家帮", "链家", "哔哩哔哩", "人民网", "凤凰网",
    "唯品会", "喜马拉雅", "央视网", "我爱我家", "搜狗", "携程", "晋江文学城", "滴滴",
    "滴答出行", "爱奇艺", "百度", "神州专车", "网易严选", "网易游戏", "腾讯新闻", "腾讯视频",
    "起点中文网", "高德", "360", "小红书","唯品会","腾讯游戏","蘑菇屋","用户", "帐号", "您", "可", "可以", "有权", "享有", "拥有",
    "得以", "能够", "应", "应当", "不得", "承担", "负责", "履行", "必须", "保证", "不", "未",
    "没有", "不会", "不能", "并非", "无", "无需"
]
base_readability.add_custom_words(custom_words)

# ===== 子进程工作函数 =====
def analyze_text(index_text_pair):
    idx, text = index_text_pair
    readability = ChineseReadability()
    readability.add_custom_words(custom_words)

    try:
        if not isinstance(text, str) or len(text.strip()) < 10:
            return idx, None
        sentences = [s.strip() for s in readability.stnsplit.split(text) if s.strip()]
        score = readability.wanglei_readability(sentences)
        print(score)
        result = score

        if result is not None and result < -50:
            print(f"⚠️ 第 {idx + 1} 条为可疑文本，前200字：{text[:200]}")
        return idx, result
    except Exception as e:
        print(f"❌ 第 {idx + 1} 条处理失败：{e}")
        return idx, None

# ===== 主执行函数 =====
def main():
    df = pd.read_excel(input_file)

    # ===== 如果已存在结果则断点续跑 =====
    if os.path.exists(output_file):
        done_df = pd.read_excel(output_file)
        start_idx = len(done_df)
        results = done_df
        print(f"🔁 续跑模式：已完成 {start_idx} 条，从第 {start_idx} 条开始")
    else:
        start_idx = 0
        results = pd.DataFrame()
        print("🚀 新任务启动：从头开始分析。")

    total = len(df)
    for i in range(start_idx, total, batch_size):
        batch = df.iloc[i:i+batch_size].copy()
        index_text_pairs = [(i + j, row["内容_清洗"]) for j, row in batch.iterrows()]

        print(f"📦 正在处理第 {i+1} 到第 {i+len(batch)} 条，共 {len(batch)} 条")

        with Pool(processes=num_workers) as pool:
            score_results = pool.map(analyze_text, index_text_pairs)

        scores = [None] * len(batch)
        for idx, score in score_results:
            print("idx:", idx, "i:", i, "score:", score)
            local_j = idx - i
            scores[local_j] = score
            print(f"✅ 第 {idx+1} 条完成，得分：{score}")
            time.sleep(0.05)

        batch["可读性分数"] = scores
        results = pd.concat([results, batch], ignore_index=True)
        results.to_excel(output_file, index=False)
        print(f"💾 已保存到第 {i + len(batch)} 条\n")

    print("🎉 全部处理完成！")

# ===== 启动程序 =====
if __name__ == "__main__":
    main()