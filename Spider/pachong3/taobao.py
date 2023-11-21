
import requests
import re
import json


def open_url(keyword, page=1):
    # &s=0 表示从第1个商品开始显示，由于1页是44个商品，所以 &s=44 表示第二页
    # &sort=sale-desc 表示按销量排序
    payload = {'q': keyword, 's': str((page - 1) * 44), "sort": "sale-desc"}
    url = "https://s.taobao.com/search"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36',
        'referer': 'https://ai.taobao.com/',
        'cookie': 'ctoken=DAK3YdYgjahL76lYJFoj5UWR; lego2_cna=DEW12W0HP0212RE4TXXYRWP1; __wpkreporterwid_=4f28ba59-4eb7-40ca-214c-d9e34e4a92ba; _m_h5_tk=512dfc8ab996aa690d9549a27005e4e1_1650650807890; _m_h5_tk_enc=f773e23c73a5c5ae219917000c38a8ea; cna=czE2GcGWtTwCAW8oOpg37AzA; xlly_s=1; tfstk=cIqGBAOjnPu1jU03PGi1crL0rNbRZnAZ6VuYYOqsHpnEmmrFigTezaMkZX55_E1..; l=eBEnq0IRLJpC8HysKOfZFurza7yFSIRAguPzaNbMiOCPOq1p54CGW6qVy0L9C3NVh686R35sMeeMBeYBqI2jPGK3X2uPIODmn; isg=BNDQjRdJhjFQxFo1qAlNmymmoR4imbTjIvTT38qhnCv-BXCvcqmEcyY32Y1A1Wy7'
    }

    res = requests.get(url, params=payload, headers=headers)
    print(res.text)
    return res


# 获取列表页的所有商品
def get_items(res):
    g_page_config = re.search(r'g_page_config = (.*?);\n', res.text)
    page_config_json = json.loads(g_page_config.group(1))
    page_items = page_config_json['mods']['itemlist']['data']['auctions']

    results = []  # 整理出我们关注的信息（ID、标题、链接、售价、销量和商家）
    for each_item in page_items:
        dict1 = dict.fromkeys(('nid', 'title', 'detail_url', 'view_price', 'view_sales', 'nick'))
        dict1['nid'] = each_item['nid']
        dict1['title'] = each_item['title']
        dict1['detail_url'] = each_item['detail_url']
        dict1['view_price'] = each_item['view_price']
        dict1['view_sales'] = each_item['view_sales']
        dict1['nick'] = each_item['nick']
        results.append(dict1)

    return results


# 统计该页面所有商品的销量
def count_sales(items):
    count = 0
    for each in items:
        if '小甲鱼' in each['title']:
            count += int(re.search(r'\d+', each['view_sales']).group())

    return count


def main():
    keyword = input("请输入搜索关键词：")

    length = 3
    total = 0
    open_url(keyword,1)
    # for each in range(length):
    #     res = open_url(keyword, each + 1)
    #     items = get_items(res)
    #     total += count_sales(items)
    #
    # print("总销量是：", total)


if __name__ == "__main__":
    main()