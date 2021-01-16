import requests
from time import sleep
from spider.utils import set_headers

headers = set_headers()

# 小米10ultra 小米自营
# 商品信息(所有规格)接口
detail_url = 'https://www.xiaomiyoupin.com/api/gateway/detail'


# 获取所有规格的商品信息
def get_detail():
    # 设置post请求数据
    data = {'groupName': 'details',
            'groupParams': [['134230']],
            'methods': [],
            'version': '1.0.0',
            'debug': False,
            'channel': ''}
    cookies = {
        'Hm_lpvt_025702dcecee57b18ed6fb366754c1b8': '1610795299',
        'Hm_lvt_025702dcecee57b18ed6fb366754c1b8': '1610792355',
        'mjclient': 'PC',
        'youpin_sessionid': '1770ae1af52-05f0c0ebca4c478-15b9',
        'youpindistinct_id': '1756a31a6ab29c-01af0b6b818cda-4c3f2779'
    }
    response = requests.post(detail_url, json=data, headers=headers, cookies=cookies)
    # print(response)
    content = response.json()
    print(content)


if __name__ == '__main__':
    pass
