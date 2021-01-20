import requests
from time import sleep
from spider.utils import set_headers


# 小米10ultra 苏宁自营旗舰店
# 获取所有规格的商品信息
def get_price():
    # 商品信息(所有规格)接口
    price_url = 'https://icps.suning.com/icps-web/getVarnishAllPriceNoCache/000000011926584302,000000011926599708,' \
                '000000000945105780,000000011926556371,000000000945105779,000000000945105786,000000011926582930,' \
                '000000000945105781,000000011926599698,000000000945112082,000000000945112087,000000011926584323,' \
                '000000011926556428,000000000945105782,000000000945105778,000000011926582952_719_7190199_0000000000,' \
                '0000000000,0000000000,0000000000,0000000000,0000000000,0000000000,0000000000,0000000000,0000000000,' \
                '0000000000,0000000000,0000000000,0000000000,0000000000,0000000000' \
                '_1_getClusterPrice.jsonp?callback=getClusterPrice'
    response = requests.get(price_url, headers=set_headers())
    content = response.text.lstrip('getClusterPrice(').rstrip(');')
    # print(content)
    with open('sn_price.json', 'w', encoding='UTF-8') as file:
        file.write(content)


# 获取评论统计数据
def get_review_satisfy():
    # 评论数量统计接口
    review_satisfy_url = 'https://review.suning.com/ajax/cluster_review_satisfy/' \
                         'cluster-37257693-000000011926584302-0000000000-----satisfy.htm?callback=satisfy'
    response = requests.get(review_satisfy_url, headers=set_headers())
    content = response.text.lstrip('satisfy(').rstrip(')')
    # print(content)
    with open('sn_review_satisfy.json', 'w', encoding='UTF-8') as file:
        file.write(content)


# 获取评论热门标签
def get_review_labels():
    # 评论热门标签(大家印象)接口
    review_labels_url = 'https://review.suning.com/ajax/getClusterReview_labels/' \
                        'cluster-37257693-000000011926584302-0000000000-----' \
                        'commodityrLabels.htm?callback=commodityrLabels&_=1610783642619'
    response = requests.get(review_labels_url, headers=set_headers())
    content = response.text.lstrip('commodityrLabels(').rstrip(')')
    # print(content)
    with open('sn_review_labels.json', 'w', encoding='UTF-8') as file:
        file.write(content)


# 获取评论详情
def get_review_lists():
    # 评论详情接口
    review_lists_url = 'https://review.suning.com/ajax/cluster_review_lists/' \
                       'cluster-37257693-000000011926584302-0000000000-' \
                       'total-1-default-10-----reviewList.htm?callback=reviewList'
    response = requests.get(review_lists_url, headers=set_headers())
    content = response.text.lstrip('reviewList(').rstrip(')')
    # print(content)
    with open('sn_review_lists.json', 'w', encoding='UTF-8') as file:
        file.write(content)


if __name__ == '__main__':
    # get_price()
    # sleep(3)
    # get_review_satisfy()
    # sleep(3)
    # get_review_labels()
    # sleep(3)
    get_review_lists()
