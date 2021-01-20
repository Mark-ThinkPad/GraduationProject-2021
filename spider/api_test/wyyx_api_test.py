import requests
from time import sleep
from spider.utils import set_headers, get_timestamp_13bit


# 日式和风声波式电动牙刷 严选电动牙刷系列
# 获取评论统计数据
def get_comment_tags():
    comment_tags_url = f'http://you.163.com/xhr/comment/tags.json?__timestamp={get_timestamp_13bit()}&itemId=1127007'
    # print(comment_tags_url)
    response = requests.get(comment_tags_url, headers=set_headers())
    content = response.json()
    # print(content)
    with open('wyyx_comment_tags.json', 'w', encoding='UTF-8') as file:
        file.write(response.text)


# 获取好评率数据
def get_comment_itemGoodRates():
    comment_itemGoodRates_url = 'http://you.163.com/xhr/comment/itemGoodRates.json'
    payload = {'itemId': '1127007'}
    response = requests.post(comment_itemGoodRates_url, payload, headers=set_headers())
    content = response.json()
    # print(content)
    with open('wyyx_comment_itemGoodRates.json', 'w', encoding='UTF-8') as file:
        file.write(response.text)


# 获取评论详情
def get_comment_list():
    commment_list_url = f'http://you.163.com/xhr/comment/listByItemByTag.json?' \
                        f'__timestamp={get_timestamp_13bit()}&itemId=1127007&tag=全部&size=20&page=1&orderBy=0' \
                        f'&oldItemTag=全部&oldItemOrderBy=0&tagChanged=0'
    # print(commment_list_url)
    response = requests.get(commment_list_url, headers=set_headers())
    content = response.json()
    # print(content)
    with open('wyyx_comment_list.json', 'w', encoding='UTF-8') as file:
        file.write(response.text)


if __name__ == '__main__':
    get_comment_tags()
    sleep(3)
    get_comment_itemGoodRates()
    sleep(3)
    get_comment_list()
