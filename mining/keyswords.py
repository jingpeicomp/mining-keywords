# coding=utf-8
import os
import sys
from re import match

import jieba
from jieba import analyse
from jieba.analyse import TextRank
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer

__author__ = 'liuzm'

TOKEN_REGEX = ur'[\u4e00-\u9fa5]+'
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), '../data')


def _cut(line):
    """
    使用结巴搜索引擎分词模式分词
    :param line: 文本数据
    :return:
    """
    return filter(lambda _token: match(TOKEN_REGEX, _token) and len(_token) > 1,
                  jieba.cut_for_search(line, HMM=True)) if line else []


def _get_tokens(path):
    """
    将文件每一行文本使用结巴进行分词
    :param path:
    :return:
    """
    with open(path) as f:
        return filter(lambda _: _, map(_cut, f))


def analyze_by_statistics(line_tokens):
    """
    使用词条统计的方式寻找关键词
    :param line_tokens:
    :return:
    """
    statics = {}
    for line_token in line_tokens:
        for token in set(line_token):
            if token in statics:
                statics[token] += 1
            else:
                statics[token] = 1
    sorted_tokens = sorted(statics.iteritems(), key=lambda (_token, _num): _num, reverse=True)
    with open(os.path.join(OUTPUT_PATH, 'keywords_statistics.txt'), 'w') as f:
        i = 0
        for (token, num) in sorted_tokens:
            token_desc = '{:<6} : {:4},    '.format(token, num)
            f.write(token_desc)
            i += 1
            if i == 10:
                f.write('\n')
                i = 0


def analyze_by_jieba_tfidf(line_tokens):
    """
    使用结巴分词自带的tfidf算法进行关键词分析
    :param line_tokens:
    :return:
    """
    sentences = map(lambda _line_token: ' '.join(_line_token), line_tokens)
    text = ' '.join(sentences)
    tags = jieba.analyse.extract_tags(text, topK=300)
    print 'analyze by jieba tfidf ', ', '.join(tags)
    with open(os.path.join(OUTPUT_PATH, 'keywords_jieba_tfidf.txt'), 'w') as f:
        i = 0
        for token in tags:
            f.write('{:<6},    '.format(token))
            i += 1
            if i == 10:
                f.write('\n')
                i = 0


def analyze_by_jieba_textrank(line_tokens):
    """
    使用结巴分词自带的TextRank算法进行关键词分析
    :param line_tokens:
    :return:
    """
    sentences = map(lambda _line_token: ' '.join(_line_token), line_tokens)
    text = ' '.join(sentences)
    textrank = TextRank()
    textrank.span = 10
    tags = textrank.extract_tags(text, topK=300, withWeight=True, allowPOS=('nv', 'vn'))
    format_tags = map(lambda (_word, _weight): '{:<6} : {:.3f}'.format(_word, float(_weight)), tags)
    print 'analyze by jieba textrank ', ', '.join(format_tags)
    with open(os.path.join(OUTPUT_PATH, 'keywords_jieba_textrank.txt'), 'w') as f:
        i = 0
        for token in format_tags:
            f.write(token + ',    ')
            i += 1
            if i == 10:
                f.write('\n')
                i = 0


def analyze_by_sl_tfidf(line_tokens):
    """
    使用scikit-learn tfidf 算法进行关键词提取
    :param line_tokens:
    :return:
    """
    sentences = map(lambda _line_token: ' '.join(_line_token), line_tokens)
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(sentences)
    transformer = TfidfTransformer(smooth_idf=False)
    tfidf = transformer.fit_transform(X)
    word = vectorizer.get_feature_names()
    weight = tfidf.toarray()
    with open(os.path.join(OUTPUT_PATH, 'keywords_tfidf.txt'), 'w') as f:
        for i in xrange(len(weight)):  # 每一行文本的权重
            word_and_weights = [(word[j], weight[i][j]) for j in xrange(len(word)) if weight[i][j] > 0]
            word_and_weights = sorted(word_and_weights, key=lambda (_word, _weight): _weight, reverse=True)
            line_keyword = ',    '.join(
                map(lambda (_word, _weight): '{:<6} : {:.3f}'.format(_word, _weight), word_and_weights))
            f.write(line_keyword)
            f.write('\n')


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    _line_tokens = _get_tokens(os.path.join(OUTPUT_PATH, 'origin.txt'))
    analyze_by_statistics(_line_tokens)
    analyze_by_jieba_tfidf(_line_tokens)
    analyze_by_jieba_textrank(_line_tokens)
    analyze_by_sl_tfidf(_line_tokens)
