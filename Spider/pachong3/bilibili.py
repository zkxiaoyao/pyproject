import requests
import bs4
import time


def get_input():
    keyword = input("请输入关键词：")
    pages = int(input("请输入要爬取得页数（1~50）："))

    while pages not in range(1, 51):
        pages = int(input("请输入正确的页数："))

    return keyword, pages


def get_html(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'}
    res = requests.get(url, headers=headers)

    return res.text


def get_datas(text):
    soup = bs4.BeautifulSoup(text, "html.parser")

    datas = []
    videos = soup.find_all("li", class_="video matrix")
    for video in videos:
        # 获取标题
        datas.append(video.a['title'])
        # 获取URL
        datas.append(video.a['href'])
        # 获取观看数/弹幕数/上传时间/阿婆主
        tags = video.select("div[class='tags'] > span")
        for tag in tags:
            datas.append(''.join(tag.text.split()))

    return datas


def grouped(iterable, n):
    "将列表切成n片一组"
    "s -> (s0,s1,s2,...sn-1), (sn,sn+1,sn+2,...s2n-1), (s2n,s2n+1,s2n+2,...s3n-1), ..."
    return zip(*[iter(iterable)] * n)


def main():
    keyword, pages = get_input()
    order = ['totalrank', 'click', 'dm', 'stow']
    order_name = ['综合排序', '最多点击', '最多弹幕', '最多收藏']

    # 迭代每种排序
    for i in range(4):
        index = 1
        # 迭代每一页
        for page in range(1, pages + 1):
            url = "https://search.bilibili.com/all?keyword={}&order={}&duration=4&tids_1=36&page={}".format(keyword,
                                                                                                            order[i],
                                                                                                            page)
            text = get_html(url)
            datas = get_datas(text)
            # 为每种排序创建一个文本文件单独存放
            with open(order_name[i] + '.txt', 'a', encoding="utf-8") as file:
                for video_title, video_URL, video_watch, video_dm, video_time, video_up in grouped(datas, 6):
                    file.write(' + '.join(
                        [str(index), video_title, video_URL, video_watch, video_dm, video_time, video_up, '\n']))
                    index += 1
            # 做一只善意的爬虫，不要给服务器带来负担
            time.sleep(1)


if __name__ == "__main__":
    main()