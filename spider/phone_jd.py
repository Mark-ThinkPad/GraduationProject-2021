import re
import json
from time import sleep
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from db.phone_sales_models import Commodity, ExistedSku, TargetSku
from spider.utils import (get_chrome_driver, get_response_body, window_scroll_by, parse_jd_count_str,
                          open_second_window, back_to_first_window, waiting_content_loading)


# 获取京东手机分类销量数据
def get_phone_sales_from_jd(browser: Chrome):
    # 打开京东手机分类
    print(f'------打开京东手机分类页面------')
    browser.get('https://list.jd.com/list.html?cat=9987,653,655')
    # 保存将要获取的所有商品SKU编号
    insert_jd_all_target_sku(browser)
    # 保存所有商品信息
    # insert_jd_all_commodity(browser)
    
    print('------京东手机分类销量数据获取完成------')


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


# 打开并切换到当前商品页面
def switch_to_current_sku_page(browser: Chrome, sku_url: str):
    open_second_window(browser)
    print(f'------打开新窗口并正在加载当前商品页面: {sku_url}------')
    browser.get(sku_url)
    print('------当前商品页面加载完成------')
    sleep(2)


# 从后端API接口获取并保存已上架的SKU
def get_jd_sku_from_api(browser: Chrome, sku: str):
    jd_sku_url = 'type=getstocks'
    skus = get_response_body(browser, jd_sku_url, 'GET')
    if skus is None:
        ExistedSku.create(
            source='京东',
            sku=sku
        )
        print('---当前商品所有SKU编号获取失败, 可能是单SKU商品---')
        return
    skus = skus.rstrip(')')
    skus = re.sub(r'^\w+?\(', '', skus)
    skus = json.loads(skus)
    for key in skus.keys():
        ExistedSku.create(
            source='京东',
            sku=key
        )
    print('------保存已上架SKU完成------')


# 保存将要获取的商品SKU编号
def insert_jd_target_sku(browser: Chrome):
    elements = browser.find_elements_by_class_name('gl-item')
    print(f'当前页面共有{len(elements)}个商品')
    for element in elements:
        # 获取当前商品SKU编号
        current_sku: str = element.get_attribute('data-sku')
        TargetSku.create(
            source='京东',
            sku=current_sku
        )


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
    for target_sku in TargetSku.select().where(TargetSku.source == '京东'):
        # 获取当前商品SKU编号
        sku: str = target_sku.sku
        # 检查当前SKU是否在数据库中保存的SKU中, 避免销量重复计数
        result = ExistedSku.get_or_none(
            ExistedSku.source == '京东',
            ExistedSku.sku == sku
        )
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

        commodity.price = float(browser.find_element_by_css_selector('span.price:nth-child(2)').text)
        commodity.title = browser.find_element_by_class_name('sku-name').text.strip()
        total_str = browser.find_element_by_css_selector('#comment-count > a').text
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

        # 从商品介绍中获取商品信息
        try:
            commodity.shop_name = browser.find_element_by_css_selector(
                '#crumb-wrap > div > div.contact.fr.clearfix > div.J-hove-wrap.EDropdown.fr > div:nth-child(1) > div '
                '> a').text
        except NoSuchElementException:
            commodity.shop_name = '店铺名称为空'
        commodity.brand = browser.find_element_by_css_selector('#parameter-brand > li > a').text
        intro = browser.find_elements_by_css_selector('.parameter2 > li')
        intro_list = []
        for i in intro:
            intro_list.append(i.text)
        for intro_item in intro_list:
            if '操作系统' in intro_item:
                commodity.os = intro_item.replace('操作系统：', '')
            if 'CPU型号' in intro_item:
                commodity.soc_model = intro_item.replace('CPU型号：', '')

        # 下滑点击 规格与包装 选项
        window_scroll_by(browser, 1200)
        js_script = 'document.querySelector("#detail > div.tab-main.large > ul > li:nth-child(2)").click()'
        browser.execute_script(js_script)
        sleep(1)

        # 从 规格与包装 中获取商品信息
        spec_list = browser.find_elements_by_class_name('Ptable-item')
        for spec_item in spec_list:
            spec_item_title = spec_item.find_element_by_tag_name('h3').text
            item_list = spec_item.find_elements_by_class_name('clearfix')
            if '主体' == spec_item_title:
                for item in item_list:
                    item_name = item.find_element_by_tag_name('dt').text
                    item_value = item.find_element_by_tag_name('dd').text
                    if '产品名称' == item_name:
                        commodity.model = item_value
            if '基本信息' == spec_item_title:
                for item in item_list:
                    item_name = item.find_element_by_tag_name('dt').text
                    item_value = item.find_element_by_tag_name('dd').text.replace('mm', '').replace('MM', '')\
                        .replace('mM', '').replace('Mm', '').replace('g', '').replace('G', '').replace('约', '')\
                        .replace('大约', '').replace('左右', '').replace('大概', '').strip()
                    try:
                        if '机身宽度' in item_name:
                            commodity.width = float(item_value)
                        if '机身厚度' in item_name:
                            commodity.thickness = float(item_value)
                        if '机身长度' in item_name:
                            commodity.length = float(item_value)
                        if '机身重量' in item_name:
                            commodity.weight = float(item_value)
                    except ValueError:
                        pass
            if '主芯片' == spec_item_title:
                for item in item_list:
                    item_name = item.find_element_by_tag_name('dt').text
                    item_value = item.find_element_by_tag_name('dd').text
                    if 'CPU品牌' == item_name:
                        commodity.soc_mfrs = item_value
            if '屏幕' == spec_item_title:
                for item in item_list:
                    item_name = item.find_element_by_tag_name('dt').text
                    item_value_str = item.find_element_by_tag_name('dd').text
                    if '主屏幕尺寸' in item_name:
                        try:
                            item_value = float(item_value_str.replace('英寸', '').strip())
                            commodity.screen_size = item_value
                        except ValueError:
                            pass
        # 保存商品信息
        commodity.save()
        # 删除已经保存的商品target_sku
        delete_saved_commodity_sku(sku)
        print(f'------SKU编号为 {sku} 的商品信息保存完毕------')
        # 回到手机分类页面
        back_to_first_window(browser)


# 删除已经保存的商品target_sku
def delete_saved_commodity_sku(target_sku: str):
    saved_sku = TargetSku.get(
        TargetSku.source == '京东',
        TargetSku.sku == target_sku
    )
    saved_sku.delete_instance()


if __name__ == '__main__':
    # 创建一个chrome实例
    driver = get_chrome_driver()
    # 获取京东手机分类销量数据
    get_phone_sales_from_jd(driver)
    # 退出浏览器实例
    driver.quit()
