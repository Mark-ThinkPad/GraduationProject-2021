import re
import json
from time import sleep
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from db.phone_sales_models import Commodity, SNTargetSku, SNExistedSku
from spider.utils import (get_chrome_driver, get_response_body, get_response_body_list, window_scroll_by,
                          open_second_window, back_to_first_window, parse_mi10_product_info, calculate_mi10_good_rate,
                          waiting_content_loading)


def get_phone_sales_from_sn(browser: Chrome):
    # 打开京东手机分类
    print(f'------打开苏宁手机分类页面------')
    browser.get('https://list.suning.com/0-20006-0.html?safp=d488778a.phone2018.103327226422.2&safc=cate.0.0&safpn'
                '=10003.00006')
    # 保存将要获取的所有商品SKU编号
    # insert_sn_all_target_sku(browser)
    # 保存所有商品信息
    insert_sn_all_commodity(browser)

    print('------苏宁手机分类销量数据获取完成------')


def insert_sn_all_target_sku(browser: Chrome):
    max_page = 141
    current_page = 0
    while current_page <= max_page:
        # 获取最大页数和当前页数
        mp_path = '#second-filter > div > div.second-page.clearfix > span'
        cp_path = '#second-filter > div > div.second-page.clearfix > span > em'
        max_page = int(re.sub(r'^\d+?/', '', browser.find_element_by_css_selector(mp_path).text))
        current_page = int(browser.find_element_by_css_selector(cp_path).text)
        print(f'总页数: {max_page}, 当前页数: {current_page}')

        # 下滑半页使页面加载后30个商品 (lazy-loading机制)
        window_scroll_by(browser, 3600)
        sleep(3)
        # 保存将要获取的当前页面的商品SKU编号
        insert_sn_target_sku(browser)

        # 翻页
        if current_page == max_page:
            break
        else:
            turn_to_the_next_page(browser)


# 保存将要获取的商品SKU编号
def insert_sn_target_sku(browser: Chrome):
    elements = browser.find_elements_by_class_name('item-wrap')
    print(f'当前页面共有{len(elements)}个商品')
    for element in elements:
        # 获取当前商品SKU编号
        content = element.get_attribute('id').split('-')
        shop_code = content[0]
        sku = content[1]
        SNTargetSku.get_or_create(
            shop_code=shop_code,
            sku=sku
        )


# 京东手机分类页面翻页
def turn_to_the_next_page(browser: Chrome):
    while True:
        try:
            WebDriverWait(browser, 0.5).until(
                ec.element_to_be_clickable((By.ID, 'nextPage'))
            )
            browser.execute_script('document.querySelector("#nextPage").click()')
            waiting_content_loading(browser, 'item-wrap')
            break
        except TimeoutException:
            window_scroll_by(browser, 500)


# 保存商品信息
def insert_sn_all_commodity(browser: Chrome):
    for target_sku in SNTargetSku.select():
        # 获取当前商品店铺代码和SKU编号
        shop_code: str = target_sku.shop_code
        sku: str = target_sku.sku
        # 检查当前SKU是否在数据库中保存的SKU中, 避免销量重复计数
        result = SNExistedSku.get_or_none(
            SNExistedSku.shop_code == shop_code,
            SNExistedSku.sku == sku
        )
        if result is not None:
            # 删除已经保存的商品target_sku
            delete_saved_commodity_sku(shop_code, sku)
            print(f'---SKU编号为 {sku} 的商品信息已保存过---')
            continue

        # 开始抓取商品信息
        commodity = Commodity()
        commodity.source = '苏宁'
        commodity.url = 'https://product.suning.com/' + shop_code + '/' + sku + '.html'

        # 打开并切换到当前商品页面
        switch_to_current_sku_page(browser, commodity.url)
        # 从后端API接口获取所有SKU和销量
        commodity.total = get_sn_sku_and_total_from_api(browser, shop_code, sku)

        # 判断是否为苏宁自营, 苏宁自营的店铺码为 0000000000
        if int(shop_code) == 0:
            commodity.is_self = True
        else:
            commodity.is_self = False

        try:
            commodity.title = browser.find_element_by_id('itemDisplayName').text
        except NoSuchElementException:
            commodity.title = '无商品标题'

        try:
            commodity.price = float(browser.find_element_by_class_name('mainprice').text.replace('¥', ''))
        except (ValueError, NoSuchElementException):
            commodity.price = -2

        try:
            commodity.shop_name = browser.find_element_by_class_name('header-shop-name').text
        except NoSuchElementException:
            commodity.shop_name = '店铺名称为空'

        # 从商品介绍中获取商品信息
        # 预赋值, 防止注入空置报错
        commodity.brand = '页面未注明'
        commodity.model = '页面未注明'
        commodity.os = '页面未注明'

        # # 保存商品信息
        # commodity.save()
        # # 删除已经保存的商品target_sku
        # delete_saved_commodity_sku(sku)
        # print(f'------SKU编号为 {sku} 的商品信息保存完毕------')
        # 回到手机分类页面
        back_to_first_window(browser)
        break


# 删除已经保存的商品 sn_target_sku
def delete_saved_commodity_sku(shop_code: str, sku: str):
    saved_sku = SNTargetSku.get(
        SNTargetSku.shop_code == shop_code,
        SNTargetSku.sku == sku
    )
    saved_sku.delete_instance()


# 打开并切换到当前商品页面
def switch_to_current_sku_page(browser: Chrome, sku_url: str):
    open_second_window(browser)
    print(f'------打开新窗口并正在加载当前商品页面: {sku_url}------')
    browser.get(sku_url)
    print('------当前商品页面加载完成------')
    sleep(2)


# 从后端API接口获取所有SKU和销量 (部分SKU较多的商品可能会返回了多个同名接口数据)
def get_sn_sku_and_total_from_api(browser: Chrome, shop_code: str, sku: str):
    skus_list = []
    summary = {}
    sn_sku_target = [
        {'url': 'getClusterPrice', 'method': 'GET'},
        {'url': 'cluster_review_satisfy', 'method': 'GET'}
    ]
    all_data = get_response_body_list(browser, sn_sku_target)
    for data in all_data:
        if data['url'] == 'getClusterPrice' and data['method'] == 'GET':
            skus_list.append(data['response_body'])
        if data['url'] == 'cluster_review_satisfy' and data['method'] == 'GET':
            summary = data['response_body']

    if len(skus_list) == 0:
        SNExistedSku.get_or_create(
            shop_code=shop_code,
            sku=sku
        )
        print('-----当前商品为单SKU商品------')

    for skus in skus_list:
        skus = skus.lstrip('getClusterPrice(').rstrip(');')
        skus = json.loads(skus)
        for sku in skus:
            SNExistedSku.get_or_create(
                shop_code=sku['vendorCode'],
                sku=sku['cmmdtyCode'].replace(re.match(r'^[0]+', sku['cmmdtyCode']).group(), ''),
            )
    print('------获取当前商品所有SKU完成------')

    summary = summary.lstrip('satisfy(').rstrip(')')
    summary = json.loads(summary)
    if summary['returnMsg'] == '查询数量成功':
        return summary['reviewCounts'][0]['totalCount']
    else:
        return -1


if __name__ == '__main__':
    # 创建一个chrome实例
    driver = get_chrome_driver()
    # 从苏宁获得数据
    get_phone_sales_from_sn(driver)
    # 退出浏览器实例
    driver.quit()
