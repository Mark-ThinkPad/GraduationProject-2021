import re
import json
from time import sleep
from random import uniform
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support import expected_conditions as ec
from db.mi10_models import Shop, Sku, Comment, CommentSummary, ModelSummary
from spider.utils import (set_options, set_capabilities, get_response_body, get_response_body_list, window_scroll_by)


# 获取苏宁易购的小米10销售数据
def get_mi10_data_from_sn(browser: Chrome):
    for sn_shop in Shop.select().where(Shop.source == '苏宁'):
        print(f'------打开当前苏宁店铺链接: {sn_shop.url}------')
        browser.get(sn_shop.url)
        # 获取所有SKU
        get_sn_sku_from_api(browser, sn_shop)

        for current_sku in sn_shop.sku:
            current_sku_url = current_sku.url_prefix + current_sku.shop_code + '/' + current_sku.sku + '.html'
            browser.get(current_sku_url)
            sleep(10)


# 获取所有SKU (苏宁自营店页面返回了两个接口数据)
def get_sn_sku_from_api(browser: Chrome, shop: Shop):
    sn_sku_target = [{'url': 'getClusterPrice', 'method': 'GET'}]
    skus_list = get_response_body_list(browser, sn_sku_target)
    for skus in skus_list:
        skus = skus['response_body'].lstrip('getClusterPrice(').rstrip(');')
        skus = json.loads(skus)
        for sku in skus:
            Sku.create(
                source=shop.source,
                is_official=shop.is_official,
                sku=sku['cmmdtyCode'].replace(re.match(r'^[0]+', sku['cmmdtyCode']).group(), ''),
                url_prefix='https://product.suning.com/',
                shop_code=sku['vendorCode'],
                shop=shop
            )


if __name__ == '__main__':
    options = set_options()
    caps = set_capabilities()
    # 在Windows环境下已将chromedriver添加至环境变量, 无需声明执行文件路径
    # 在Arch Linux环境下, 使用archlinux cn源安装的chromedriver位置在/usr/bin, 也无需声明执行文件路径
    driver = Chrome(options=options, desired_capabilities=caps)
    # 从苏宁获得数据
    get_mi10_data_from_sn(driver)
    # 退出浏览器实例
    driver.quit()
