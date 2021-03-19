import re
import json
from time import sleep
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, WebDriverException
from db.mi10_models import Shop, MiSku, Comment, CommentSummary, ModelSummary
from spider.utils import (get_chrome_driver, get_response_body, get_response_body_list, window_scroll_by,
                          open_second_window, back_to_first_window, waiting_comments_loading)


# 获取小米有品的小米10销售数据
def get_mi10_data_from_youpin(browser: Chrome):
    for youpin_shop in Shop.select().where(Shop.source == '小米有品'):
        print(f'------打开当前小米有品商品链接: {youpin_shop.url}------')
        browser.get(youpin_shop.url)
        # 获取所有SKU与对应的产品规格信息 (方便标识评论对应的产品信息)
        get_mi_sku_and_product_info_from_api(browser, youpin_shop)

        # 获取默认排序评论
        print('------开始获取默认排序评论------')
        switch_to_youpin_default_comments_page(browser)
        get_youpin_comments(browser, youpin_shop)


# 从后端API接口获取小米平台(商城和有品)所有SKU与对应的产品规格信息
def get_mi_sku_and_product_info_from_api(browser: Chrome, shop: Shop):
    detail_url = 'api/gateway/detail'
    detail = get_response_body(browser, detail_url, 'POST')
    detail = json.loads(detail)
    if detail['message'] == 'ok':
        for info in detail['data']['goods']['productInfo'].values():
            ram_and_rom = info['attributeValues'][0].split('+')
            ram = ram_and_rom[0]
            rom = ram_and_rom[1]
            mi_sku, created = MiSku.get_or_create(
                source=shop.source,
                is_official=shop.is_official,
                sku=str(info['mapId']),
                product_color=info['attributeValues'][1],
                product_ram=ram,
                product_rom=rom
            )
            if created is False:
                print(f'SKU: {str(info["mapId"])} 已存在')
        print('-----保存商品SKU和规格信息成功------')
    else:
        print('-----获取商品SKU和规格信息失败------')


# 打开默认评论页面
def switch_to_youpin_default_comments_page(browser: Chrome):
    window_scroll_by(browser, 800)
    browser.execute_script('document.querySelector("li.info-nav-item:nth-child(2)").click()')
    waiting_comments_loading(browser, 'commentItem')


# 获取小米有品的评论数据
def get_youpin_comments(browser: Chrome, shop: Shop):
    page = 1
    while True:
        try:
            if page == 1:
                pass
            else:
                pass
        except WebDriverException:
            print(f'---获取第{page}页评论异常---')
            break

        print(f'当前页数: {page}')
        # 下滑点击下一页
        while True:
            try:
                WebDriverWait(browser, 0.5).until(
                    ec.element_to_be_clickable((By.CSS_SELECTOR, 'li.m-pagination-item:nth-child(8) > a:nth-child(1)'))
                )
                js_script = 'document.querySelector("li.m-pagination-item:nth-child(8) > a:nth-child(1)").click()'
                browser.execute_script(js_script)
                waiting_comments_loading(browser, 'commentItem')
                break
            except TimeoutException:
                window_scroll_by(browser, 500)

        page += 1

    print('------评论获取阶段结束------')


if __name__ == '__main__':
    # 创建一个chrome实例
    driver = get_chrome_driver()
    # 从小米有品获得数据
    get_mi10_data_from_youpin(driver)
    # 退出浏览器实例
    driver.quit()