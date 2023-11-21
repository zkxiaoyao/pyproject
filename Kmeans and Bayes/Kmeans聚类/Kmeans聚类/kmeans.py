# encoding=utf8
from numpy import *
import matplotlib.pyplot as plt

# 计算两个点之间的欧氏距离
def euclDistance(vector1, vector2):
    # 向量的对应维度之差的平方的和的开根号
    return sqrt(sum(power(vector2 - vector1, 2)))


# 初始化k个随机的聚类中心点
def initCentroids(dataSet, k):
    # dataSet.shape是获取矩阵的行列数，返回行数和列数
    numSamples, dim = dataSet.shape
    # 生成k*dim维度的全0矩阵
    centroids = zeros((k, dim))
    for i in range(k):
        # 生成0到样本空间长度之间的随机值，每次生成的都不同
        # 该随机值用于从样本空间中任意取出k个点
        index = int(random.uniform(0, numSamples))
        # 将样本空间中的随机点作为聚类中心点
        centroids[i, :] = dataSet[index, :]
    return centroids


# k-means聚类
def kmeans(dataSet, k):
    # 样本空间的长度
    numSamples = dataSet.shape[0]
    # 生成 样本空间长度*2 的全0矩阵，称之为“样本类矩阵”
    # 第一列将存储样本所属的聚类索引，第二列存储样本与聚类中心的距离
    clusterAssment = mat(zeros((numSamples, 2)))
    # 用于表示聚类中心是否有改动，改动则需要重新计算，无改动则停止循环
    clusterChanged = True

    # 初始化k个聚类中心点
    centroids = initCentroids(dataSet, k)

    while clusterChanged:
        clusterChanged = False
        # 循环所有样本点，计算样本点到各聚类中心的距离，将样本点放入距离最小的类中
        for i in range(numSamples):
            # 初始化一个非常大的距离
            minDist = 100000.0
            # 离当前样本点最近的类索引，初始化为0
            minIndex = 0
            # 循环每一个聚类中心
            # 得到离样本最近的聚类中心点
            for j in range(k):
                # 计算样本与聚类中心的欧氏距离
                distance = euclDistance(centroids[j, :], dataSet[i, :])
                # 如果距离小于最小距离
                if distance < minDist:
                    # 将当前设置为样本到聚类中心的最小距离
                    minDist = distance
                    # 将当前类索引设置为最小类索引
                    minIndex = j

            # 样本类矩阵的第i行第0列，即当前样本的所属类
            # 如果当前样本的所属类的距离不是最小距离
            if clusterAssment[i, 0] != minIndex:
                # 样本需要需要更新聚类
                clusterChanged = True
                # 更新样本的所属聚类，第0列为所属类，第1列为欧氏距离的平方
                #clusterAssment[i, :] = minIndex, minDist ** 2

        # 更新每个聚类中心
        # 重新计算各个类的中心
        for j in range(k):
            # clusterAssment[:, 0].A 表示 样本类矩阵 的所有行第0列组成的单列矩阵的，一个样本长度，值为类索引的列矩阵
            # .A == j 将矩阵每个元素做判断，与j一样的将为True，否则为False，同样是样本长度，值为True/False的列矩阵
            # nonzero() 取出矩阵中值为True的行和列索引，只要取出行索引，因此取[0]
            # 从dataSet中取出所有j类的样本，组成新的矩阵
            pointsInCluster = dataSet[nonzero(clusterAssment[:, 0].A == j)[0]]
            # mean(pointsInCluster, axis=0) 矩阵平行上下相加取平均，即取样本各个维度的平均值
            centroids[j, :] = mean(pointsInCluster, axis=0)

    print('Congratulations, cluster complete!')
    return centroids, clusterAssment


# 画出聚类图
def showCluster(dataSet, k, centroids, clusterAssment):
    # 获得样本的行和列
    numSamples, dim = dataSet.shape
    # 如果列不是二维的则没法画图
    if dim != 2:
        print("Sorry! I can not draw because the dimension of your data is not 2!")
        return 1

    # 设置每个聚类中点的样式（颜色、形状等）
    mark = ['or', 'ob', 'og', 'ok', 'oy', '+r', 'sr', 'dr', '<r', 'pr']
    if k > len(mark):
        print("请增加几种mark")
        return 1

    # 绘制所有样本
    for i in range(numSamples):
        # 取出样本所属类样式索引
        markIndex = int(clusterAssment[i, 0])
        # 用样本的第0列和第1列作为x,y坐标，绘图
        plt.plot(dataSet[i, 0], dataSet[i, 1], mark[markIndex])

    # 设置聚类中心的样式
    mark = ['Dr', 'Db', 'Dg', 'Dk', 'Dy', '+b', 'sb', 'db', '<b', 'pb']
    # 绘制聚类中心
    for i in range(k):
        # markersize为标记的大小
        plt.plot(centroids[i, 0], centroids[i, 1], mark[i], markersize=12)

    plt.show()


def main():
    print("step 1: load data...")
    dataSet = []
    # 读入数据
    fileIn = open('data.txt')
    for line in fileIn.readlines():
        lineArr = line.strip().split('\t')
        dataSet.append([float(lineArr[0]), float(lineArr[1])])

    # 聚类
    print("step 2: clustering...")
    dataSet = mat(dataSet)
    print("请输入要生成的类别的数量：")
    k = (int)(input())
    centroids, clusterAssment = kmeans(dataSet, k)

    # 显示结果
    print("step 3: show the result...")
    showCluster(dataSet, k, centroids, clusterAssment)

if __name__ == "__main__":
    main()