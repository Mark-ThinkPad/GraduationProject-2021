import re
import json
from time import sleep
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, WebDriverException
from spider.utils import (get_chrome_driver, get_response_body, window_scroll_by, parse_jd_count_str,
                          open_second_window, back_to_first_window, parse_mi10_product_info, calculate_mi10_good_rate,
                          waiting_comments_loading)


# 获取京东手机分类销量数据
def get_phone_sales_from_jd(browser: Chrome):
    # 打开京东手机分类
    browser.get('https://list.jd.com/list.html?cat=9987,653,655')
    api = 'productCommentSummaries.action'
    elements = browser.find_elements_by_class_name('gl-item')
    print(type(elements), len(elements))
    for element in elements:
        print(element)
        print(element.get_attribute('data-sku'), element.get_attribute('2333'), element.get_property('2333'))


if __name__ == '__main__':
    # 创建一个chrome实例
    driver = get_chrome_driver()
    #
    get_phone_sales_from_jd(driver)
    # 退出浏览器实例
    driver.quit()

