import re
import json
from time import sleep
from random import uniform
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, WebDriverException
from db.mi10_models import Shop, Sku, Comment, CommentSummary, ModelSummary
from spider.utils import (get_chrome_driver, get_response_body, get_response_body_list, window_scroll_by,
                          open_second_window, back_to_first_window, parse_mi10_product_info, calculate_mi10_good_rate)


# 获取小米商城的小米10销售数据
def get_mi10_data_from_mishop(browser: Chrome):
    pass


if __name__ == '__main__':
    # 创建一个chrome实例
    driver = get_chrome_driver()
    # 从小米商城获得数据
    get_mi10_data_from_mishop(driver)
    # 退出浏览器实例
    driver.quit()
