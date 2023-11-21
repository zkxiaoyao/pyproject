from bs4 import BeautifulSoup         #网页解析，获取数据
import re           #正则表达式，进行文字匹配
import urllib.request       #制定URL，获取网页数据
import xlwt         #进行excel操作
import sqlite3      #进行sqlite3数据库操作
import urllib.parse

def main():
    baseurl = "file:///D:/daima/python/Naive%20Bayes/Naive%20Bayes/test.html"
    datalist = getData(baseurl)
    savapath = "test.txt"
    saveData(datalist,savapath)
findComent=re.compile(r'<div class="cmt_cnt adjust" ptag="">(.*?)</div>',re.S)
#爬取网页
def getData(baseurl):
    datalist=[]
    url=baseurl
    html=askURL(url)
    #print(html)
    #2.逐一解析数据
    soup=BeautifulSoup(html,"html.parser")
    #, id = "evalDet_summary"
    for item in soup.find_all('li'):
        item=str(item)
        cm=re.findall(findComent,item)  #re库用来通过正则表达式来查找指定的字符串
        datalist.append(str(cm))                  #添加链接
    for data in datalist:
        if data !=[]:
            datalist.remove(data)
    print(datalist)
    return datalist
#保存数据
def saveData(datalist,savapath):
    file=open(savapath,mode='w')
    for data in datalist:
            file.write(data+"\n")
    file.close()

#得到一个制定URL的网页信息
def askURL(url):
    head={  #模拟浏览器头部信息，向豆瓣服务器发送消息
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 Edg/86.0.622.69"
          }#用户代理，表示告诉豆瓣服务器‘我们是什么类型的机器、浏览器。’
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