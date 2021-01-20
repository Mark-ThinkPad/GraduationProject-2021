import requests
from time import sleep
from spider.utils import set_headers


# 小米10ultra 小米商城
# 获取商品信息
def get_commodity():
    commodity_url = 'https://api2.service.order.mi.com/mall/commodity_page?product_id=12609&callback=__jp0'
    headers = set_headers(Referer='https://www.mi.com/comment/12609.html')
    response = requests.get(commodity_url, headers=headers)
    content = response.text.lstrip('__jp0(').rstrip(');')
    # print(content)
    with open('xmsc_commodity.json', 'w', encoding='UTF-8') as file:
        file.write(content)


# 获取评论统计数据
def get_comment_summary():
    comment_summary_url = 'https://api2.service.order.mi.com/user_comment/get_summary?' \
                          'goods_id=12609&v_pid=12609&support_start=0&support_len=10&' \
                          'add_start=0&add_len=10&profile_id=0&show_img=0&callback=__jp6'
    headers = set_headers(Referer='https://www.mi.com/comment/12609.html')
    response = requests.get(comment_summary_url, headers=headers)
    content = response.text.lstrip('__jp6(').rstrip(');')
    # print(content)
    with open('xmsc_comment_summary.json', 'w', encoding='UTF-8') as file:
        file.write(content)


# 获取评论详情
def get_comment_list():
    comment_list_url = 'https://api2.service.order.mi.com/user_comment/get_list?' \
                       'goods_id=12609&v_pid=12609&order_by=22&page_index=1&' \
                       'page_size=10&profile_id=0&show_img=0&callback=__jp5'
    headers = set_headers(Referer='https://www.mi.com/comment/12609.html')
    response = requests.get(comment_list_url, headers=headers)
    content = response.text.lstrip('__jp5(').rstrip(');')
    # print(content)
    with open('xmsc_comment_list.json', 'w', encoding='UTF-8') as file:
        file.write(content)


if __name__ == '__main__':
    get_commodity()
    sleep(3)
    get_comment_summary()
    sleep(3)
    get_comment_list()
