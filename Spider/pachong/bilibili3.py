from bs4 import BeautifulSoup         #网页解析，获取数据
import re           #正则表达式，进行文字匹配
import urllib.request       #制定URL，获取网页数据
import xlwt         #进行excel操作
import sqlite3      #进行sqlite3数据库操作
import urllib.parse

def main():
    baseurl = "https://search.bilibili.com/all?keyword=%E6%88%90%E9%83%BD49%E4%B8%AD%E4%BA%8B%E4%BB%B6&page="
    datalist = getData(baseurl)
    savapath = "播放情况.xls"
    saveData(datalist,savapath)

#影片详情链接的规则
# findLink=re.compile(r'<a href="(.*?)">')  #创建正则表达式对象，表示规则（字符串模式）
# findImage=re.compile(r'<img.*src="(.*?)"',re.S)  #re.S:让换行符包括在字符中
# findTitle=re.compile(r'<span class="title">(.*)</span>')
# findRating=re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
# findJudge=re.compile(r'<span>(\d*)人评价</span>')
# findInq=re.compile(r'<span class="inq">(.*)</span>')
# findBd=re.compile(r'<p class="">(.*?)</p>',re.S)
findTitle=re.compile(r'<a class="img-anchor" href=".*?" target="_blank" title="(.*?)">')
findPlayTimes=re.compile(r'<span class=".*?" title="观看"><i class=".*?"></i>(.*?)</span>',re.S)
findDanMu=re.compile(r'<span class=".*?" title="弹幕"><i class=".*?"></i>(.*?)</span>',re.S)
findTime=re.compile(r'<span class=".*?" title="上传时间"><i class=".*?"></i>(.*?)</span>',re.S)
findUP=re.compile(r'<span class=".*?" title="up主"><i class=".*?"></i><a class="up-name" href=".*?" target="_blank">(.*?)</a></span>')
#爬取网页
def getData(baseurl):
    datalist=[]
    for i in range(0,28):    #调用获取页面信息的函数10次
        url=baseurl+str(i+1)
        html=askURL(url)    #保存获取的网页代码
        #2.逐一解析数据
        soup=BeautifulSoup(html,"html.parser")
        for item in soup.find_all('li',class_="video-item matrix"):
            #print(item)  #测试：查看电影item的全部信息
            data=[]  #保存一部电影的全部信息
            item=str(item)
            title=DoStr(str(re.findall(findTitle,item)))
            print(title)
            playTimes=DoStr(str(re.findall(findPlayTimes,item)))
            print(playTimes)
            danMu=DoStr(str(re.findall(findDanMu,item)))
            print(danMu)
            time=DoStr(str(re.findall(findTime,item)))
            print(time)
            UP=DoStr(str(re.findall(findUP,item)))
            print(UP)
            data.append(UP)
            data.append(title)
            data.append(playTimes)
            data.append(danMu)
            data.append(time)
            #影片详情链接
            # link=re.findall(findLink,item)[0]  #re库用来通过正则表达式来查找指定的字符串
            # data.append(link)                  #添加链接
            # image=re.findall(findImage,item)[0]
            # data.append(image)                 #添加图片
            # title=re.findall(findTitle,item)   #片名可能只有一个中文名，没有外国名
            # if(len(title)==2):
            #     ctitle=title[0]
            #     data.append(ctitle)             #添加中文名
            #     otitle=title[1].replace("/","") #去掉无关符号
            #     data.append(otitle)             #添加外文名
            # else:
            #     data.append(title[0])
            #     data.append(' ')                #外文名留空
            #
            # rating=re.findall(findRating,item)[0]
            # data.append(rating)                 #添加评分
            # judgeNum=re.findall(findJudge,item)[0]
            # data.append(judgeNum)              #添加评价人数
            # inq=re.findall(findInq,item)
            # if len(inq)!=0:
            #     inq=inq[0].replace("。","")
            #     data.append(inq)
            # else:
            #     data.append(" ")
            # bd=re.findall(findBd,item)[0]
            # bd=re.sub('<br(\s+)?>(\s+)?'," ",bd)
            # bd=re.sub('/'," ",bd)
            # data.append(bd.strip()) #去掉前后空格
            datalist.append(data)
    # print(datalist)

    return datalist
#保存数据
def DoStr(bd):
    bd=bd.replace("'","").replace("[","").replace("]","").replace("\\n","")
    bd=bd.strip()
    return bd
def saveData(datalist,savapath):
    pass
    book = xlwt.Workbook(encoding="utf-8",style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet(savapath,cell_overwrite_ok=True)
    col=("Up主","标题","播放量","弹幕量","发布时间")
    for i in range(0,5):
        sheet.write(0,i,col[i])
    for i in range(0,500):
        print(f'第{i+1}条')
        data = datalist[i]
        for j in range(0,5):
            sheet.write(i+1,j,data[j])
    book.save(savapath)

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
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return  html


if __name__=="__main__":
    main()
    print("爬取完毕！")