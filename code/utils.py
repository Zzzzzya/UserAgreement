import difflib
import re
import jieba
from collections import defaultdict

def compare_documents(text1, text2, key_terms=None):
    """
    比较两个中文文档的差异，提供详细的变更统计
    
    参数:
    text1: str - 旧版本文本
    text2: str - 新版本文本
    key_terms: list - 需要特别关注的关键术语列表
    """
    # 执行中文优化预处理
    text1_clean, text1_words = chinese_preprocess(text1)
    text2_clean, text2_words = chinese_preprocess(text2)
    
    # 计算字符级变更统计
    char_stats = calculate_text_changes(text1_clean, text2_clean)
    
    # 计算词语级变更统计
    word_stats = calculate_word_changes(text1_words, text2_words)
    
    # 关键术语变更统计
    term_changes = calculate_keyterm_changes(text1_clean, text2_clean, key_terms)
    
    return {
        "char_stats": char_stats,
        "word_stats": word_stats,
        "term_changes": term_changes
    }

def chinese_preprocess(text):
    """中文文本预处理：去除非中文字符、分词"""
    # 去除非中文字符和多余空格
    cleaned = re.sub(r'[^\u4e00-\u9fa5，。；：！？、\s]', '', text)
    cleaned = re.sub(r'\s+', '', cleaned)
    
    # 中文分词
    words = list(jieba.cut(cleaned))
    
    # 为比较创建单词序列字符串
    word_seq = " ".join(words)
    
    return cleaned, word_seq

def calculate_text_changes(old_text, new_text):
    """计算字符级别的变更统计"""
    seq_matcher = difflib.SequenceMatcher(None, old_text, new_text)
    
    # 初始化统计值
    stats = {
        'total_chars': len(old_text),
        'deleted_chars': 0,
        'inserted_chars': 0,
        'modified_chars': 0,
        'changed_chars': 0,
        'diff_blocks': []
    }
    
    # 解析所有差异操作
    for tag, i1, i2, j1, j2 in seq_matcher.get_opcodes():
        old_segment = old_text[i1:i2]
        new_segment = new_text[j1:j2]
        
        block = {
            'action': tag,
            'old_text': old_segment,
            'new_text': new_segment,
            'old_start': i1,
            'old_end': i2,
            'new_start': j1,
            'new_end': j2
        }
        
        stats['diff_blocks'].append(block)
        
        if tag == 'delete':
            stats['deleted_chars'] += (i2 - i1)
        elif tag == 'insert':
            stats['inserted_chars'] += (j2 - j1)
        elif tag == 'replace':
            del_len = i2 - i1
            ins_len = j2 - j1
            # 修改字符数取较小值
            modified = min(del_len, ins_len)
            stats['modified_chars'] += modified
            # 多余部分计为删除/新增
            stats['deleted_chars'] += max(0, del_len - modified)
            stats['inserted_chars'] += max(0, ins_len - modified)
    
    # 计算总变更字符数
    stats['changed_chars'] = (
        stats['deleted_chars'] + 
        stats['inserted_chars'] + 
        stats['modified_chars']
    )
    
    # 计算百分比
    if stats['total_chars'] > 0:
        stats['deleted_pct'] = (stats['deleted_chars'] / stats['total_chars']) * 100
        stats['inserted_pct'] = (stats['inserted_chars'] / stats['total_chars']) * 100
        stats['modified_pct'] = (stats['modified_chars'] / stats['total_chars']) * 100
        stats['total_change_pct'] = (stats['changed_chars'] / stats['total_chars']) * 100
    else:
        # 处理空文档的情况
        stats.update({
            'deleted_pct': 0,
            'inserted_pct': 0,
            'modified_pct': 0,
            'total_change_pct': 0
        })
    
    return stats

def calculate_word_changes(old_words, new_words):
    """计算词语级别的变更统计"""
    # 按空格分割单词序列
    old_word_list = old_words.split()
    new_word_list = new_words.split()
    
    seq_matcher = difflib.SequenceMatcher(None, old_word_list, new_word_list)
    
    stats = {
        'total_words': len(old_word_list),
        'deleted_words': 0,
        'inserted_words': 0,
        'changed_words': 0
    }
    
    # 识别变化的词语
    changed_words = {
        'deleted': [],
        'inserted': []
    }
    
    for tag, i1, i2, j1, j2 in seq_matcher.get_opcodes():
        if tag == 'delete':
            deleted = old_word_list[i1:i2]
            stats['deleted_words'] += len(deleted)
            changed_words['deleted'].extend(deleted)
        elif tag == 'insert':
            inserted = new_word_list[j1:j2]
            stats['inserted_words'] += len(inserted)
            changed_words['inserted'].extend(inserted)
        elif tag == 'replace':
            deleted = old_word_list[i1:i2]
            inserted = new_word_list[j1:j2]
            stats['deleted_words'] += len(deleted)
            stats['inserted_words'] += len(inserted)
            changed_words['deleted'].extend(deleted)
            changed_words['inserted'].extend(inserted)
    
    stats['changed_words'] = stats['deleted_words'] + stats['inserted_words']
    
    if stats['total_words'] > 0:
        stats['change_pct'] = (stats['changed_words'] / stats['total_words']) * 100
    else:
        stats['change_pct'] = 0
    
    stats['changed_word_list'] = changed_words
    
    return stats

def calculate_keyterm_changes(old_text, new_text, key_terms=None):
    """计算关键术语的出现频率变化"""
    if key_terms is None:
        # 默认隐私政策相关术语
        key_terms = []
    
    term_changes = {}
    
    for term in key_terms:
        old_count = old_text.count(term)
        new_count = new_text.count(term)
        change = new_count - old_count
        
        term_changes[term] = {
            'old_count': old_count,
            'new_count': new_count,
            'change': change
        }
    
    return term_changes

def calculate_fuzzy_similarity_with_preprocessing(text1, text2):
    """
    结合中文预处理的模糊相似度计算
    """
    import difflib
    
    # 使用您已有的中文预处理函数
    text1_clean, _ = chinese_preprocess(text1)
    text2_clean, _ = chinese_preprocess(text2)
    
    # 计算预处理后文本的相似度
    similarity = difflib.SequenceMatcher(None, text1, text2).ratio()
    return similarity

# 示例用法
if __name__ == "__main__":
    # 示例文档
    old_policy = """
    隐私政策更新说明
    我们非常重视用户的隐私保护。
    """
    
    new_policy = """
    隐私政策变更说明
    我们高度重视用户的隐私保护。
    """
    
    # 自定义关键术语列表
    key_terms = ["隐私", "收集", "信息", "使用", "数据", "保护"]
    
    # 执行比较
    results = compare_documents(old_policy, new_policy)
    
    # 打印字符级变更统计
    print("\n字符级变更统计:")
    for key, value in results["char_stats"].items():
        if key not in ["diff_blocks"]:  # 排除大块数据
            print(f"{key}: {value}")
    
    # 打印词语级变更统计
    print("\n词语级变更统计:")
    for key, value in results["word_stats"].items():
        if key not in ["changed_word_list"]:  # 排除详细词列表
            print(f"{key}: {value}")
    
    # 打印关键术语统计
    print("\n关键术语变更:")
    for term, data in results["term_changes"].items():
        print(f"{term}: 原频次={data['old_count']}, 新频次={data['new_count']}, 变化={data['change']}")