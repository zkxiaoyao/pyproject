from bs4 import BeautifulSoup         #网页解析，获取数据
import re           #正则表达式，进行文字匹配
import urllib.request       #制定URL，获取网页数据
import xlwt         #进行excel操作
import sqlite3      #进行sqlite3数据库操作
import urllib.parse
import gzip
from io import BytesIO
import random

def main():
    baseurl = "https://baijiahao.baidu.com/s?id=1699593666075935719&wfr=spider&for=pc"
    datalist = getData(baseurl)
    savapath = "bilibili.txt"
    saveData(datalist,savapath)

#影片详情链接的规则
findLink=re.compile(r'<a href="(.*?)">')  #创建正则表达式对象，表示规则（字符串模式）
findImage=re.compile(r'<img.*src="(.*?)"',re.S)  #re.S:让换行符包括在字符中
findTitle=re.compile(r'<span class="title">(.*)</span>')
findRating=re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findJudge=re.compile(r'<span>(\d*)人评价</span>')
findInq=re.compile(r'<span class="inq">(.*)</span>')
findBd=re.compile(r'<p class="">(.*?)</p>',re.S)
findText=re.compile(r'<p class="text">(.*?)</p>')
#爬取网页
def getData(baseurl):
    datalist=[]
    url=baseurl
    html=askURL(url)    #保存获取的网页代码
    #2.逐一解析数据
    soup=BeautifulSoup(html,"html.parser")
    for item in soup.find_all('div',class_="comment-list "):
        #print(item)  #测试：查看电影item的全部信息
        data=[]  #保存一部电影的全部信息
        item=str(item)
        text=re.findall(findText,item)
        # #影片详情链接
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
        datalist.append(text)
        print(datalist)

    return datalist
#保存数据
def saveData(datalist,savapath):
    for text in datalist:
        with open(savapath, 'a', encoding='utf-8') as f:
            f.write(text)
            f.write('')
            f.write('\n')


#得到一个制定URL的网页信息
def askURL(url):
    user_agent = [

        "Mozilla/5.0 (Windows NT6.1;WOW64)AppleWebKit/537.1(KHTML,likeGecko)Chrome/22.0.1207.1Safari/537.1",

        "Mozilla/5.0(WindowsNT6.1;WOW64)AppleWebKit/536.6(KHTML,likeGecko)Chrome/20.0.1092.0Safari/536.6",

        "Mozilla/5.0(WindowsNT6.2)AppleWebKit/536.6(KHTML,likeGecko)Chrome/20.0.1090.0Safari/536.6",
        "Mozilla/5.0(WindowsNT6.2;WOW64)AppleWebKit/537.1(KHTML,likeGecko)Chrome/19.77.34.5Safari/537.1",

        "Mozilla/5.0(WindowsNT6.0)AppleWebKit/536.5(KHTML,likeGecko)Chrome/19.0.1084.36Safari/536.5",

        "Mozilla/5.0(WindowsNT6.1;WOW64)AppleWebKit/536.3(KHTML,likeGecko)Chrome/19.0.1063.0Safari/536.3",

        "Mozilla/5.0(WindowsNT5.1)AppleWebKit/536.3(KHTML,likeGecko)Chrome/19.0.1063.0Safari/536.3",

        "Mozilla/5.0(WindowsNT6.2)AppleWebKit/536.3(KHTML,likeGecko)Chrome/19.0.1062.0Safari/536.3",

        "Mozilla/5.0(WindowsNT6.1;WOW64)AppleWebKit/536.3(KHTML,likeGecko)Chrome/19.0.1062.0Safari/536.3",

        "Mozilla/5.0(WindowsNT6.2)AppleWebKit/536.3(KHTML,likeGecko)Chrome/19.0.1061.1Safari/536.3",

        "Mozilla/5.0(WindowsNT6.1;WOW64)AppleWebKit/536.3(KHTML,likeGecko)Chrome/19.0.1061.1Safari/536.3",

        "Mozilla/5.0(WindowsNT6.1)AppleWebKit/536.3(KHTML,likeGecko)Chrome/19.0.1061.1Safari/536.3",

        "Mozilla/5.0(WindowsNT6.2)AppleWebKit/536.3(KHTML,likeGecko)Chrome/19.0.1061.0Safari/536.3",

        "Mozilla/5.0(WindowsNT6.2;WOW64)AppleWebKit/535.24(KHTML,likeGecko)Chrome/19.0.1055.1Safari/535.24"]
    headers = {

        "sec-fetch-dest": "empty",

        "sec-fetch-mode": "cors",

        "sec-fetch-site": "same-site",

        "origin": "https://www.bilibili.com",

        "referer": "https://www.bilibili.com/video/BV1Z5411Y7or?from=search&seid=8575656932289970537",

        "cookie": "_uuid=0EBFC9C8-19C3-66CC-4C2B-6A5D8003261093748infoc;buvid3=4169BA78-DEBD-44E2-9780-B790212CCE76155837infoc;sid=ae7q4ujj;DedeUserID=501048197;DedeUserID__ckMd5=1d04317f8f8f1021;SESSDATA=e05321c1%2C1607514515%2C52633*61;bili_jct=98edef7bf9e5f2af6fb39b7f5140474a;CURRENT_FNVAL=16;rpdid=|(JJmlY|YukR0J'ulmumY~u~m;LIVE_BUVID=AUTO4315952457375679;CURRENT_QUALITY=80;bp_video_offset_501048197=417696779406748720;bp_t_offset_501048197=417696779406748720;PVID=2",

        "user-agent": random.choice(user_agent), }
    head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
    }  # 用户代理，表示告诉豆瓣服务器‘我们是什么类型的机器、浏览器。’
    request=urllib.request.Request(url, headers=head)
    html=""
    try:
        response = urllib.request.urlopen(request)
        html = response.read()
        buff = BytesIO(html)
        f = gzip.GzipFile(fileobj=buff)
        html = f.read().decode('utf-8')
        print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return  html


if __name__=="__main__":
    main()
    print("爬取完毕！")