# UserAgreement

# Env
` pip install pandas matplotlib openpyxl`
` pip install cntext jieba gensim mittens nltk scikit-learn pdfdocx chardet`

# TODO
1. 清洗后（删掉爬下来的无关文字）统计每篇文档的字数，取每年所有协议字数的中位数
2. 计算可读性分数，不要直接使用可读性指标衡量每一篇的分数，而是让他对每个句子打分，打完后计算这篇协议里所有句子的平均分，作为这个句子的可读性指标（这个特别复杂，跑起来很慢，因为我们有好几百个文档和七万多个句子，我的电脑之前就没带动）
3. 计算相邻年份、相同平台协议【变化】的百分比，进行断点分析。这一步也需要处理一下，我之前的prompt：

  - 现在，我们想计算协议更新内容的百分比。参考这篇论文的做法：We measured the percentage of privacy policies updated in each interval. To determine if these changes align with shifts in the language of privacy policies, we also measured terms that have experienced changes in their usage at each interval.你需要完成以下事情：
    ①目前，我们收集和编码的所有平台协议都经过了去重操作，意味着采集的都是这个时间点【新出现（更新）的协议文本】。因此，需要以【单个平台】为单位分析，观察其每个版本协议与【上一个版本】协议的差异程度，计算更新内容的百分比。
    ②在对单个平台分析完后，将其按照年份、平台类别整理。计算出【每一年】这个类别下的协议，与【前一年】的平均差异程度是多少。
    ③如果该平台在两个相邻年份没有更新（例如只有2017年的协议记录，下一条记录就到2019年了），那么空缺年份（2018）的数据就不要将该平台包括在内。即：对每一年变化程度的研究，只研究【在该年与上一年均有记录】的协议文本变化程度。
    ④如果一年内有多次更新（多个记录），那么计算该年最后一次记录与上一年的变化程度。
  - 这里会有一些变化比例计算出来是0，为什么经过去重操作还会有0变化的呢？因为有些平台太勤快了，哪怕2023-2024两年完全没改协议内容，也会把协议最后落款的2023改成2024。。。醉了