import json
from time import sleep
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, WebDriverException
from db.wireless_headphone_models import Commodity, YouPinURL
from spider.utils import (get_chrome_driver, get_response_body, get_response_body_list, window_scroll_by,
                          waiting_content_loading, open_second_window, back_to_first_window)


def get_wireless_headphone_from_youpin(browser: Chrome):
    # 打开小米有品无线耳机搜索结果
    # url_list = [
    #     'https://www.xiaomiyoupin.com/search?keyword=%E6%97%A0%E7%BA%BF%E8%80%B3%E6%9C%BA',
    #     'https://www.xiaomiyoupin.com/search?keyword=%E8%93%9D%E7%89%99%E8%80%B3%E6%9C%BA'
    # ]
    # for url in url_list:
    #     print(f'------正在打开小米有品无线耳机搜索结果页面------')
    #     browser.get(url)
    #     sleep(1)
    #     # 保存将要获取的所有商品SKU编号
    #     insert_youpin_all_url(browser)

    # 保存所有商品信息
    insert_youpin_all_commodity(browser)

    print('------小米有品无线耳机销量数据获取完成------')


# 保存将要获取的所有商品SKU编号
def insert_youpin_all_url(browser: Chrome):
    current_page = 0
    while True:
        current_page += 1
        print(f'当前页数: {current_page}')
        # 保存将要获取的当前页面的商品URL链接
        insert_youpin_url(browser)

        next_page = ''
        elements = browser.find_elements_by_class_name('m-pagination-item')
        for element in elements:
            if element.text == '下一页':
                next_page = element

        if 'disabled' in next_page.get_attribute('class'):
            break
        else:
            next_page.click()
            sleep(1)


# 保存将要获取的当前页面的商品URL链接
def insert_youpin_url(browser: Chrome):
    elements = browser.find_elements_by_css_selector('.pro-item.m-tag-a')
    print(f'当前页面共有{len(elements)}个商品')
    for element in elements:
        # 获取当前商品SKU编号
        target_url = element.get_attribute('data-src')
        YouPinURL.get_or_create(url=target_url)


def insert_youpin_all_commodity(browser: Chrome):
    for youpin_url in YouPinURL.select():
        commodity = Commodity()
        commodity.source = '小米有品'
        commodity.url = youpin_url.url

        # 打开并切换到当前商品页面
        switch_to_current_sku_page(browser, commodity.url)
        # 打开评论页面并获取总销量
        browser.execute_script('document.querySelector("li.info-nav-item:nth-child(2)").click()')
        sleep(1)
        commodity.total = -1
        total_str = browser.find_element_by_css_selector('div.tabbar-item:nth-child(1) > a:nth-child(1)').text
        total_str = total_str.lstrip('全部(').rstrip(')').strip()
        commodity.total = int(total_str)

        break
        # # 保存商品信息
        # commodity.save()
        # # 删除已经保存的商品URL链接
        # delete_saved_commodity_url(commodity.url)
        # print(f'------SKU编号为 {sku} 的商品信息保存完毕------')
        # # 回到无线耳机分类页面
        # back_to_first_window(browser)
        # sleep(2)


# 打开并切换到当前商品页面
def switch_to_current_sku_page(browser: Chrome, sku_url: str):
    open_second_window(browser)
    print(f'------打开新窗口并正在加载当前商品页面: {sku_url}------')
    browser.get(sku_url)
    print('------当前商品页面加载完成------')
    sleep(2)


# 删除已经保存的商品URL链接
def delete_saved_commodity_url(target_url):
    saved_url = YouPinURL.get_by_id(target_url)
    saved_url.delete_instance()


if __name__ == '__main__':
    # 创建一个chrome实例
    driver = get_chrome_driver()
    # 从苏宁获得数据
    get_wireless_headphone_from_youpin(driver)
    # 退出浏览器实例
    driver.quit()
