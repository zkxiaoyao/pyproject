#-*- coding=utf-8 -*-
from bs4 import BeautifulSoup         #网页解析，获取数据
import re           #正则表达式，进行文字匹配
import urllib.request       #制定URL，获取网页数据
import xlwt         #进行excel操作
import sqlite3      #进行sqlite3数据库操作
import urllib.parse

def main():
    baseurl = "https://maoyan.com/films?showType=3&offset="

    datalist = getData(baseurl)

    savapath = "猫眼电影top.xls"
    saveData(datalist,savapath)
    # askURL(baseurl)
#创建正则表达式对象，表示规则（字符串模式）
findTitle=re.compile(r'<div class="movie-hover-title" title="(.*)"')

findLink=re.compile(r'<a.*href="(.*?)"',re.S)
findIntro=re.compile(r'<span class="dra">(.*)</span>',)
findTimeAndWhere=re.compile(r'<li class="ellipsis">(.*)</li>')



#爬取网页
def getData(baseurl):
    datalist=[]
    for i in range(0,1):    #调用获取页面信息的函数60次
        url=baseurl+str(i*30)
        html=askURL(url)

        soup=BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div',class_="movie-item film-channel"):
            #print(item)  #测试：查看电影item的全部信息
            data=[]  #保存一部电影的全部信息
            item=str(item)
            title = re.findall(findTitle, item)[0]
            data.append(title)
            print(title)
            link=re.findall(findLink,item)[0]
            s="https://maoyan.com" + str(link)
            smallhtml = askURL(s)
            print(s)
            smallsoup = BeautifulSoup(smallhtml, "html.parser")
            smallsoup=str(smallsoup)
            intro=re.findall(findIntro,smallsoup)
            if intro==[]:
                intro="暂无"
            else:
                intro=intro[0]
            data.append(intro)
            print(intro)
            timeAndPlace=re.findall(findTimeAndWhere,smallsoup)
            if timeAndPlace == []:
                timeAndPlace = "暂无"
            else:
                timeAndPlace = timeAndPlace[0]
            data.append(timeAndPlace)
            print(timeAndPlace)
            datalist.append(data)
    return datalist
#保存数据
def saveData(datalist,savapath):
    book = xlwt.Workbook(encoding="utf-8",style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet('猫眼电影top',cell_overwrite_ok=True)
    col=("电影名称","电影介绍","上映时间及地点")
    for i in range(0,3):
         sheet.write(0,i,col[i])
    for i in range(0,30):
        print(f'第{i+1}条')
        data = datalist[i]
        for j in range(0,3):
            sheet.write(i+1,j,data[j])
    book.save('猫眼电影top.xls')

#得到一个制定URL的网页信息
def askURL(url):
    head={  #模拟浏览器头部信息，向豆瓣服务器发送消息
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.60"
          }#用户代理，表示告诉服务器‘我们是什么类型的机器、浏览器。’
    request=urllib.request.Request(url, headers=head)
    html=""
    try:
        response=urllib.request.urlopen(request)
        html=response.read().decode("utf-8")
        #print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return  html


if __name__=="__main__":
    main()
    print("爬取完毕！")