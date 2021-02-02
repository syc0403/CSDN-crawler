import pymysql
import pandas as pd
import jieba
import jieba.analyse
# 自然语言处理的库gensim，需要传入list of list的结构
from gensim import corpora, models
from sklearn.model_selection import train_test_split

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
    if current_segment != 'r\n':
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
'''
Fit():
解释：简单来说，就是求得训练集X的均值啊，方差啊，最大值啊，最小值啊这些训练集X固有的属性。可以理解为一个训练过程

Transform(): 
解释：在Fit的基础上，进行标准化，降维，归一化等操作（看具体用的是哪个工具，如PCA，StandardScaler等）。

Fit_transform():
解释：fit_transform是fit和transform的组合，既包括了训练又包含了转换。
'''


# 用贝叶斯多项式模型分类并输出分类结果
def bys(ss):
    df_train = pd.DataFrame({'text_clean': text_clean, 'label': df['class']})
    # 当前这一列有多少个不重复的值
    print(df_train.label.unique())
    # 将类别做一个映射
    i = 0
    label_mapping = {}
    for value in df_train.label.unique():
        i += 1
        label_mapping[value] = i
    # 将label映射放入dataframe,也就是将label值用数值代替
    df_train['label'] = df_train['label'].map(label_mapping)

    # 将数据划分成训练集和测试集
    x_train, x_test, y_train, y_test = train_test_split(df_train.text_clean.values, df_train.label.values,
                                                        random_state=1)
    # print(x_train,x_test,y_train,y_test)
    # 将训练集中的每个文本词库的词用空格连接成一段字符串，后续需要把每条text转换为对应的向量，通过sklearn中的向量构造器
    words = []
    for line_index in range(len(x_train)):
        try:
            # 需要把list转换为string格式，可以用.join形式组合，并且用‘ ’空格取分开
            # join()用法参考：https://blog.csdn.net/weixin_40475396/article/details/78227747
            words.append(' '.join(x_train[line_index]))  # words里面是训练数据
        except:
            print(line_index, word_index)
    # 构造一个文本向量的训练集,有了上面的words的标准格式的内容，开始构建特征向量
    from sklearn.feature_extraction.text import CountVectorizer
    vec = CountVectorizer(max_features=4000, lowercase=False)
    # fit一下
    vec.fit(words)
    words_train = vec.transform(words)
    # 导入在sklearn中，把beyes拿出来，有输入特征，还有label值
    from sklearn.naive_bayes import MultinomialNB
    # 实例化分类器对象
    classifier = MultinomialNB()
    # 把word向量传入classifier
    classifier.fit(words_train, y_train)
    MultinomialNB(alpha=1.0, class_prior=None, fit_prior=True)
    # 试集同样的3步处理操作：内容转换为string，
    # 空格分开 ---
    # 把内容转换为特征向量 ----
    # 导入贝叶斯模型传入（输入特征向量与label值）
    test_words = []
    for line_index in range(len(x_test)):
        try:
            test_words.append(' '.join(x_test[line_index]))
        except:
            print(line_index, word_index)
    test_words[0]
    # 学习原始文档中所有标记的词汇表，并将测试集转换为文本向量
    words_test = vec.transform(test_words)
    # 基于词频向量的，进行贝叶斯结果
    accracy1 = classifier.score(words_test, y_test)  # 返回分类的准确率
    print('词频模型预测准确率为:', accracy1)
    # 检测模型
    print(classifier.predict(vec.transform(test_words)[ss]))
    print(y_test[ss])
    print(x_test[ss])
    # 另一种构造向量的方式，不采用词频，采用TF-IDF模式构造向量
    # from sklearn.feature_extraction.text import TfidfVectorizer
    # vectorizer = TfidfVectorizer(analyzer='word', max_features=4000, lowercase=False)
    # vectorizer.fit(words)  # 从原始文本中学习tf和idf
    # # 训练朴素多项分布贝叶斯模型
    # classifier = MultinomialNB()
    # classifier.fit(vectorizer.transform(words), y_train)
    # MultinomialNB(alpha=1.0, class_prior=None, fit_prior=True)
    # # 执行当前的结果，贝叶斯分类器的精度
    # accracy2 = classifier.score(vectorizer.transform(test_words), y_test)
    # print('TF-IDF模型预测准确率为:',accracy2)


if __name__ == '__main__':
    bys(ss=111)
