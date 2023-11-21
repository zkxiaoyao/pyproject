import requests

import pandas as pd

import re

import time

import random

from concurrent.futures import ThreadPoolExecutor

import datetime

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



start_time = datetime.datetime.now()

def Grab_barrage(date):
    params = {

        'type': 1,

        'oid': '128777652',

        'date': date
    }
    headers = {

                        "sec-fetch-dest":"empty",

                        "sec-fetch-mode":"cors",

                        "sec-fetch-site":"same-site",

                        "origin":"https://www.bilibili.com",

                        "referer":"https://www.bilibili.com/video/BV1Z5411Y7or?from=search&seid=8575656932289970537",

                        "cookie":"_uuid=0EBFC9C8-19C3-66CC-4C2B-6A5D8003261093748infoc;buvid3=4169BA78-DEBD-44E2-9780-B790212CCE76155837infoc;sid=ae7q4ujj;DedeUserID=501048197;DedeUserID__ckMd5=1d04317f8f8f1021;SESSDATA=e05321c1%2C1607514515%2C52633*61;bili_jct=98edef7bf9e5f2af6fb39b7f5140474a;CURRENT_FNVAL=16;rpdid=|(JJmlY|YukR0J'ulmumY~u~m;LIVE_BUVID=AUTO4315952457375679;CURRENT_QUALITY=80;bp_video_offset_501048197=417696779406748720;bp_t_offset_501048197=417696779406748720;PVID=2",

                        "user-agent":random.choice(user_agent),}


#发送请求获取响应

    response=requests.get(url,params=params,headers=headers)

#print(response.encoding)重新设置编码

    response.encoding='utf-8'

#print(response.text)

#正则匹配提取数据

    comment=re.findall('<dp=".*?">(.*?)</d>',response.text)

#将每条弹幕数据写入txt

    with open('weibo.txt','a+') as f:

        for con in comment:

            f.write(con+'\n')

    time.sleep(random.randint(1,3))#休眠

def main():

#开多线程爬取提高爬取效率

    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(Grab_barrage,date_list)

#计算所用时间

    delta=(datetime.datetime.now()-start_time).total_seconds()

    print(f'用时：{delta}s')


if __name__=='__main__':
    url="https://api.bilibili.com/x/v2/dm/history"

    start='20200101'

    end='20200106'

    #生成时间序列

    date_list=[x for x in pd.date_range(start,end).strftime('%Y-%m-%d')]

    count=0

    #调用主函数

    main()