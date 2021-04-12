import re
import json
from time import sleep
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, WebDriverException
from db.phone_sales_models import Commodity, SNExistedSku, SNTargetSku
from spider.utils import (get_chrome_driver, get_response_body, get_response_body_list, window_scroll_by,
                          open_second_window, back_to_first_window, parse_mi10_product_info, calculate_mi10_good_rate,
                          waiting_content_loading)


def get_phone_sales_from_sn(browser: Chrome):
    # 打开京东手机分类
    print(f'------打开苏宁手机分类页面------')
    browser.get('https://list.suning.com/0-20006-0.html?safp=d488778a.phone2018.103327226422.2&safc=cate.0.0&safpn'
                '=10003.00006')
    # 保存将要获取的所有商品SKU编号
    insert_sn_all_target_sku(browser)
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


def insert_sn_all_commodity(browser: Chrome):
    pass


if __name__ == '__main__':
    # 创建一个chrome实例
    driver = get_chrome_driver()
    # 从苏宁获得数据
    get_phone_sales_from_sn(driver)
    # 退出浏览器实例
    driver.quit()
