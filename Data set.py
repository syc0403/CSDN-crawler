import pymysql
import pandas as pd
import jieba
import jieba.analyse
# 自然语言处理的库gensim，需要传入list of list的结构
from gensim import corpora, models, similarities
import gensim

# 创建连接
conn = pymysql.connect(host='localhost', user='root', password='333333', database='blog')
# 读取数据库
df = pd.read_sql('select * from train_data', conn)
# 把标题那一列拿出来转化list  当类别为python时
text = df.text.tolist()  # 将每条标题都组成列表
# 使用结巴分词器
with open('stopwords.txt', 'r', encoding='utf-8') as sw:
    stopwords = sw.read().split('\n')

text_s = []  # 存放分词后的结果
for line in text:
    current_segment = jieba.lcut(line)  # 把这句话分词
    # 确实有分词而却不包括换行符
    if len(current_segment) > 1 and current_segment != 'r\n':
        # 去空格
        L = []
        for v in current_segment:
            v = str.strip(v)
            if v:
                L.append(v)
        text_s.append(L)
text_clean = text_s
# 导入停用词
# index_col=False使panadas不用第一列作为行的名称
# sep:指定分隔符，默认是‘，’
# 不设置quoting，默认会去除英文双引号，只留下英文双引号内的内容，设置quoting = 3，会如实读取内容
# with open('stopwords.txt','r',encoding='utf-8') as sw:
#     stopwords = sw.read()
# print(stopwords)
#
# # 定义筛选函数
# def drop_stopwords(texts, stopwords):
#     text_clean = []  # 存放筛选后的
#     for line in texts:
#         line_clean = []
#         for word in line:
#             if word in stopwords:  # 如果出现在停词表中就过滤掉
#                 continue
#             line_clean.append(word)
#         text_clean.append(line_clean)
#     return text_clean
#
#
# # 把数据传入函数
# texts = df.text.values.tolist()
# text_clean = drop_stopwords(texts, stopwords)
# df_content=pd.DataFrame({'contents_clean':text_clean})
# print(df_content.head())
'''
TF-IDF用于评估一个字词对于语料库中一个文本的重要程度。
TF(词频)=在某一类文本中词条出现的次数/该类中所有词条数目
IDF(逆文本频率)=log(语料库中文本总数)/(包含该词条的文本数+1)
TF-IDF=TF*IDF
'''


def TF_IDF(index):
    # 提取关键字
    print(df['text'][index])
    text_s_str = ''.join(text_s[index])  # 将一开始分词后的结果中每篇文章的词库连接成字符串
    # 返回TF/IDF 权重最大的5个关键字  topk:选择几个关键词返回
    print('')
    print("关键词: ", " ".join(jieba.analyse.extract_tags(text_s_str, topK=5, withWeight=False)))


# TF_IDF(1)

'''
LDA主题模型是一种文档生成模型，是一种非监督机器学习技术。
它认为一篇文档是有多个主题的，而每个主题又对应着不同的词。
一篇文档的构造过程，首先是以一定的概率选择某个主题，然后再在这个主题下以一定的概率选出某一个词，
这样就生成了这篇文档的第一个词。不断重复这个过程，就生成了整篇文章

格式要求：list of list 形式，每篇文章每一篇文章都分好词
'''


def lda(text_clean):
    # 做映射，相当于词袋 将每一个词都分配一个id
    dictionary = corpora.Dictionary(text_clean)
    # 创建一个词袋向量,形如：[[(a11,b1),...,(a1n,b1n)],..,[(ann),..,(bnn)]]
    # a表示单个词id,b表示在此文本中出现次数
    corpus = [dictionary.doc2bow(sentence) for sentence in text_clean]

    # 建立一个lda模型
    lda = models.LdaModel(corpus=corpus, id2word=dictionary, num_topics=20)  # 传入词袋  传入词典   分成20个主题
    # 一号分类结果
    print(lda.print_topic(1, topn=5))  # 打印第一个主题用5个词表示
    # 打印20个主题
    for topic in lda.print_topics(num_topics=20, num_words=5):
        print(topic[1])


# lda(text_clean)

df_train = pd.DataFrame({'text_clean': text_clean, 'label': df['class']})
print(df_train.head())
print(df_train.label.unique())