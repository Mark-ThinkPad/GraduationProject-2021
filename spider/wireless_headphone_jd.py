import re
import json
from time import sleep
from json.decoder import JSONDecodeError
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from db.wireless_headphone_models import Commodity, JDExistedSku, JDTargetSku
from spider.utils import (get_chrome_driver, get_response_body, window_scroll_by, parse_jd_count_str,
                          open_second_window, back_to_first_window, waiting_content_loading)


# 获取京东无线耳机分类销量数据
def get_wireless_headphone_from_jd(browser: Chrome):
    # 打开京东无线耳机分类
    # url_list = [
    #     'https://list.jd.com/list.html?cat=652%2C828%2C842&ev=235_58350%5E&cid3=842',
    #     'https://list.jd.com/list.html?cat=652%2C828%2C842&ev=235_66906%5E&cid3=842'
    # ]
    # for url in url_list:
    #     print(f'------正在打开京东无线耳机分类页面------')
    #     browser.get(url)
    #     # 保存将要获取的所有商品SKU编号
    #     insert_jd_all_target_sku(browser)

    # 保存所有商品信息
    insert_jd_all_commodity(browser)

    print('------京东无线耳机分类销量数据获取完成------')


# 京东无线耳机分类页面翻页
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


# 打开并切换到当前商品页面
def switch_to_current_sku_page(browser: Chrome, sku_url: str):
    open_second_window(browser)
    print(f'------打开新窗口并正在加载当前商品页面: {sku_url}------')
    browser.get(sku_url)
    print('------当前商品页面加载完成------')
    sleep(2)


# 从后端API接口获取并保存已上架的SKU
def get_jd_sku_from_api(browser: Chrome, sku: str):
    try:
        jd_sku_url = 'type=getstocks'
        skus = get_response_body(browser, jd_sku_url, 'GET')
        if skus is None:
            raise WebDriverException()

        skus = skus.rstrip(')')
        skus = re.sub(r'^\w+?\(', '', skus)
        skus = json.loads(skus)
        for key in skus.keys():
            JDExistedSku.get_or_create(sku=key)
        print('------保存已上架SKU完成------')

    except (WebDriverException, JSONDecodeError):
        JDExistedSku.get_or_create(sku=sku)
        print('------当前商品是单SKU商品------')


# 保存将要获取的商品SKU编号
def insert_jd_target_sku(browser: Chrome):
    elements = browser.find_elements_by_class_name('gl-item')
    print(f'当前页面共有{len(elements)}个商品')
    for element in elements:
        # 获取当前商品SKU编号
        current_sku: str = element.get_attribute('data-sku')
        JDTargetSku.get_or_create(sku=current_sku)


# 保存将要获取的所有商品SKU编号
def insert_jd_all_target_sku(browser: Chrome):
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
        # 保存将要获取的当前页面的商品SKU编号
        insert_jd_target_sku(browser)

        # 翻页
        if current_page == max_page:
            break
        else:
            turn_to_the_next_page(browser)


# 保存商品信息
def insert_jd_all_commodity(browser: Chrome):
    for target_sku in JDTargetSku.select():
        # 获取当前商品SKU编号
        sku: str = target_sku.sku
        # 检查当前SKU是否在数据库中保存的SKU中, 避免销量重复计数
        result = JDExistedSku.get_or_none(JDExistedSku.sku == sku)
        if result is not None:
            # 删除已经保存的商品target_sku
            delete_saved_commodity_sku(sku)
            print(f'---SKU编号为 {sku} 的商品信息已保存过---')
            continue

        # 开始抓取商品信息
        commodity = Commodity()
        commodity.source = '京东'
        commodity.url = 'https://item.jd.com/' + sku + '.html'

        # 打开并切换到当前商品页面
        switch_to_current_sku_page(browser, commodity.url)
        # 从后端API接口获取并保存已上架的SKU
        get_jd_sku_from_api(browser, sku)

        try:
            commodity.price = float(browser.find_element_by_css_selector('span.price:nth-child(2)').text)
        except (ValueError, NoSuchElementException):
            # 价格显示为待发布时或商品以下柜时, 抛出异常
            commodity.price = -2

        try:
            commodity.title = browser.find_element_by_class_name('sku-name').text.strip()
        except NoSuchElementException:
            commodity.title = '无商品标题'

        commodity.total = -1  # 商品销量预赋值
        for item in browser.find_elements_by_css_selector('#detail > div.tab-main.large > ul > li'):
            if '商品评价' in item.text:
                total_str = item.find_element_by_tag_name('s').text.lstrip('(').rstrip(')')
                commodity.total = parse_jd_count_str(total_str)

        # 判断是否为京东自营
        try:
            self_str = browser.find_element_by_class_name('u-jd').text
            if self_str == '自营':
                self = True
            else:
                self = False
        except NoSuchElementException:
            self = False
        commodity.is_self = self

        try:
            commodity.shop_name = browser.find_element_by_css_selector(
                '#crumb-wrap > div > div.contact.fr.clearfix > div.J-hove-wrap.EDropdown.fr > div:nth-child(1) > div '
                '> a').text
        except NoSuchElementException:
            commodity.shop_name = '店铺名称为空'

        # 从商品介绍中获取商品信息
        try:
            commodity.brand = browser.find_element_by_css_selector('#parameter-brand > li > a').text
        except NoSuchElementException:
            commodity.brand = '未知'

        intro = browser.find_elements_by_css_selector('.parameter2 > li')
        intro_list = []
        for i in intro:
            intro_list.append(i.text)
        # 预赋值, 防止注入空置报错
        commodity.model = '未知'
        for intro_item in intro_list:
            if '商品名称' in intro_item:
                commodity.model = intro_item.replace('商品名称：', '')

        # 保存商品信息
        commodity.save()
        # 删除已经保存的商品target_sku
        delete_saved_commodity_sku(sku)
        print(f'------SKU编号为 {sku} 的商品信息保存完毕------')
        # 回到无线耳机分类页面
        back_to_first_window(browser)


# 删除已经保存的商品 target_sku
def delete_saved_commodity_sku(target_sku: str):
    saved_sku = JDTargetSku.get(JDTargetSku.sku == target_sku)
    saved_sku.delete_instance()


if __name__ == '__main__':
    # 创建一个chrome实例
    driver = get_chrome_driver()
    # 获取京东无线耳机分类销量数据
    get_wireless_headphone_from_jd(driver)
    # 退出浏览器实例
    driver.quit()
