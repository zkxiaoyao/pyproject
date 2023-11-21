﻿#coding:utf-8
import re
import requests
import bs4
import openpyxl
def open_url(url):
    headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537'
                           '.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'}
    res=requests.get(url,headers=headers)
    return  res
def fine_data(res):
    data=[]
    soup=bs4.BeautifulSoup(res.text,"html.parser")
    content=soup.find(id="Cnt-Main-Article-QQ")
    target=content.find_all("p",style="TEXT-INDENT: 2em")
    target=iter(target)
    for each in target:
        if each.text.isnumeric():
            data.append([re.search(r'\[(.+)\]', next(target).text).group(1),
                         re.search(r'\d.*', next(target).text).group(),
                         re.search(r'\d.*', next(target).text).group(),
                         re.search(r'\d.*', next(target).text).group()])
    return data
def to_excel(data):
    wb=openpyxl.Workbook()
    ws=wb.active
    ws.append(['城市','平均房价','平均工资','房价工资比'])
    for each in data:
        ws.append(each)
    wb.save('fangjia.xlsx')


def main():
    url="http://news.house.qq.com/a/20170702/003985.htm"
    res=open_url(url)

    # with open("fangjia.txt","w",encoding='utf-8') as file:
    #     file.write(res.text)
    data=fine_data(res)
    to_excel(data)
if __name__ == '__main__':
    main()