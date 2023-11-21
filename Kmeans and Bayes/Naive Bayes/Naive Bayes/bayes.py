# encoding=utf8
__author__ = 'jingle'

from numpy import *
# 创建实验样本
def loadDataSet():
    postingList = [['我', '超级', '喜欢', '这款', '手机', '超', '薄'],
                   ['什么', '垃圾', '狗屁', '手机', '简直', '一无是处', '不', '想', '再', '用'],
                   ['非常', '好看', '而且', '好用', '手机', '放心', '购买'],
                   ['这么', '烂', '的', '二货', '手机', '谁', '买', '谁', '傻逼'],
                   ['功能', '挺', '多', '屏幕', '不', '好', '一般'],
                   ['还', '可以', '比', '苹果', '手机', '好']]
    classVec = [0, 1, 0, 1, 1, 0]
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
        else:
            print("the word: %s is not in my Vocabulary!" % word)
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
    myVocabList = createVocabList(listOPosts)
    trainMat = []
    for postinDoc in listOPosts:
        trainMat.append(setOfWords2Vec(myVocabList, postinDoc))
    # 获得训练参数，概率值
    p0V, p1V, pAb = trainNB0(array(trainMat), array(listClasses))
    testEntry = ['喜欢', '好用']
    # 将待分类文档进行词袋表示
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    # 调用分类器进行分类
    print(testEntry, 'classified as: ', classifyNB(thisDoc, p0V, p1V, pAb))
    testEntry = ['垃圾', '一无是处', '傻逼', '狗屁']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print(testEntry, 'classified as: ', classifyNB(thisDoc, p0V, p1V, pAb))


if __name__ == "__main__":
    testingNB()