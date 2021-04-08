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
                          waiting_content_loading)


# 获取京东手机分类销量数据
def get_phone_sales_from_jd(browser: Chrome):
    # 打开京东手机分类
    print(f'------打开京东手机分类页面------')
    browser.get('https://list.jd.com/list.html?cat=9987,653,655')
    # api = 'productCommentSummaries.action'
    max_page = 141
    current_page = 0
    while current_page <= max_page:
        # 获取最大页数和当前页数
        mp_path = '/html/body/div[7]/div/div[2]/div[1]/div/div[1]/div[1]/div[3]/span/i'
        cp_path = '/html/body/div[7]/div/div[2]/div[1]/div/div[1]/div[1]/div[3]/span/b'
        max_page = int(browser.find_element_by_xpath(mp_path).text)
        current_page = int(browser.find_element_by_xpath(cp_path).text)
        print(f'总页数: {max_page}, 当前页数: {current_page}')
        # 下滑半页使页面加载后30个商品 (lazy-loading机制)
        window_scroll_by(browser, 3200)
        sleep(3)

        elements = browser.find_elements_by_class_name('gl-item')
        print(len(elements))
        # for element in elements:
        #     print(element)
        #     print(element.get_attribute('data-sku'), element.get_attribute('2333'), element.get_property('2333'))

        # 翻页
        if current_page == max_page:
            break
        else:
            turn_to_the_next_page(browser)


# 京东手机分类页面翻页
def turn_to_the_next_page(browser: Chrome):
    while True:
        try:
            WebDriverWait(browser, 0.5).until(
                ec.element_to_be_clickable((By.CLASS_NAME, 'pn-next'))
            )
            browser.execute_script('document.querySelector(".pn-next").click()')
            waiting_content_loading(browser, 'gl-item')
            break
        except TimeoutException:
            window_scroll_by(browser, 500)


if __name__ == '__main__':
    # 创建一个chrome实例
    driver = get_chrome_driver()
    # 获取京东手机分类销量数据
    get_phone_sales_from_jd(driver)
    # 退出浏览器实例
    driver.quit()
