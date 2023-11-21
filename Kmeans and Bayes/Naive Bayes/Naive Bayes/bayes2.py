# encoding=utf8
__author__ = 'jingle'
import  jieba
from numpy import *
# 创建实验样本
def loadDataSet():
    fileIn = open('comments.txt')
    classVec = []
    postingList=[]
    for line in fileIn.readlines():
        lineArr = line.strip().split(' ')
        classVec.append(int(lineArr[0]))
        with open('stopwords.txt', 'r+') as fp:
            stopwords = fp.read().split('\n')  # 将停用词词典的每一行停用词作为列表中的一个元素
        word_list = []  # 用于存储过滤停用词后的分词结果
        seg_list = jieba.cut(lineArr[1])
        for seg in seg_list:
            if seg not in stopwords:
                word_list.append(seg)
        postingList.append(list(word_list))
    return postingList, classVec


# 创建词表
def createVocabList(dataSet):
    # 创建空集
    vocabSet = set([])
    for document in dataSet:
        # 将文档的词集合求并集
        vocabSet = vocabSet | set(document)
    return list(vocabSet)


# bag of words 词向量表示
def setOfWords2Vec(vocabList, inputSet):
    # 创建一个全0的向量
    returnVec = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            # returnVec[vocabList.index(word)] = 1
            # 对应词维度+1
            returnVec[vocabList.index(word)] += 1
            #print("the word: %s is  in my Vocabulary!" % word)
        else:

            pass
    return returnVec


# 训练参数
def trainNB0(trainMatrix, trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    # 求得p(y=1)概率
    pAbusive = sum(trainCategory) / float(numTrainDocs)
    # 避免某一维度概率为0，初始化一个词表长度的单位矩阵
    p0Num = ones(numWords)
    p1Num = ones(numWords)
    # 相当与K*lambda
    p0Denom = 2.0
    p1Denom = 2.0

    for i in range(numTrainDocs):
        # 如果训练数据类别为1
        if trainCategory[i] == 1:
            # 将所有训练X矩阵相加，得到每个维度词出现的频次
            p1Num += trainMatrix[i]
            # 计算所有词的频次之和
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    # log相加等于相乘
    # 求分类1的各维度概率矩阵
    p1Vect = log(p1Num / p1Denom)
    # 求分类0的各维度概率矩阵
    p0Vect = log(p0Num / p0Denom)
    return p0Vect, p1Vect, pAbusive


# 朴素贝叶斯分类器
def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    # 求p(y=1|x)的分子部分
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)
    p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
    if p1 > p0:
        return 1
    else:
        return 0


def testingNB():
    listOPosts, listClasses = loadDataSet()
    i=len(listOPosts)
    for l in listOPosts:
        pass
        #print(list(l))
    #print(listClasses)
    myVocabList = createVocabList(listOPosts)
    trainMat = []
    for postinDoc in listOPosts:
         trainMat.append(setOfWords2Vec(myVocabList, postinDoc))
    # 获得训练参数，概率值
    p0V, p1V, pAb = trainNB0(array(trainMat), array(listClasses))
    # testEntry = ['喜欢', '好']
    # # 将待分类文档进行词袋表示
    # thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    # # 调用分类器进行分类
    # print(testEntry, 'classified as: ', classifyNB(thisDoc, p0V, p1V, pAb))
    # testEntry = ['辣鸡', '一无是处', '傻逼', '狗屁']
    # thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    # print(testEntry, 'classified as: ', classifyNB(thisDoc, p0V, p1V, pAb))
    testList=[]
    fileOut=open("test.txt")
    for line in fileOut.readlines():
        line = line.replace('[', '').replace(']','').replace('\'','').replace('\n','')

        with open('stopwords.txt', 'r+') as fp:
            stopwords = fp.read().split('\n')  # 将停用词词典的每一行停用词作为列表中的一个元素
        word_list = []  # 用于存储过滤停用词后的分词结果
        seg_list = jieba.cut(line)
        for seg in seg_list:
            if seg not in stopwords:
                word_list.append(seg)
        testList.append(word_list)
    for test in testList:
        testEntry=list(test)
        thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
        print(testEntry, 'classified as: ', classifyNB(thisDoc, p0V, p1V, pAb))

if __name__ == "__main__":
    testingNB()