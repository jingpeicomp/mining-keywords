# mining-keywords

关键词提取，使用多种方法提取给定语料中的关键词。步骤：

1. 对给定的语料使用 [结巴分词](https://github.com/fxsjy/jieba) 进行中文分词
2. 从分词后的词条中提取关键词

一共使用了四种方法提取关键词：

1. 词条数目统计
2. 结巴自带的 TF-IDF 算法、
3. 结巴自带的 TextRank 算法、
4. Scikit-Learn 包中的 TF-IDF 算法。

## 安装

依赖：

* Python (2.7)
* jieba (>= 0.39)
* scikit-learn (>=0.20.2)

## 使用

[data](/data) 目录中 origin.txt 文件是原始数据，执行 [keywords.py](/mining/keywords.py) 脚本后，输出关键词文件在 data 目录下。