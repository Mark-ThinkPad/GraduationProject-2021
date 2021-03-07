import re
import json
from time import sleep
from selenium.webdriver import Chrome
from selenium.webdriver.common.action_chains import ActionChains
from spider.utils import set_options, set_capabilities, get_response_body
from db.mi10_models import Shop, Sku, Comment, CommentSummary, ModelSummary


# 获取京东数据
def get_data_from_jd(browser: Chrome, shop: Shop):
    get_jd_all_sku(browser, shop)


# 获取京东商品所有SKU
def get_jd_all_sku(browser: Chrome, shop: Shop):
    # get_jd_sku_from_api(browser, shop)
    get_jd_sku_from_comments(browser, shop)


# 从getstocks接口获取已上架的SKU
def get_jd_sku_from_api(browser: Chrome, shop: Shop):
    browser.get(shop.url)
    jd_sku_url = 'type=getstocks'
    skus = get_response_body(browser, jd_sku_url, 'GET')
    skus = skus.rstrip(')')
    skus = re.sub(r'^\w+?\(', '', skus)
    skus = json.loads(skus)
    for key in skus.keys():
        Sku.create(
            source=shop.source,
            is_official=shop.is_official,
            sku=key,
            url_prefix='https://item.jd.com/',
            shop=shop
        )


# 从默认评论排序中获取所有SKU, 顺便保存评论
def get_jd_sku_from_comments(browser: Chrome, shop: Shop):
    # 完成后删除
    browser.get(shop.url)
    # 页面向下滑动
    js = 'window.scrollBy({top:1000, left:0, behavior: "smooth"})'
    browser.execute_script(js)
    sleep(1)
    # 选择商品评论标签并点击
    product_comments = '/html/body/div[10]/div[2]/div[1]/div[1]/ul/li[5]'
    browser.find_element_by_xpath(product_comments).click()
    sleep(1)



if __name__ == '__main__':
    options = set_options()
    caps = set_capabilities()
    # 在Windows环境下已将chromedriver添加至环境变量, 无需声明执行文件路径
    # 在Arch Linux环境下, 使用archlinux cn源安装的chromedriver位置在/usr/bin, 也无需声明执行文件路径
    driver = Chrome(options=options, desired_capabilities=caps)
    # 京东部分正在开发
    shop = Shop.get_by_id(1)
    get_data_from_jd(driver, shop)
    # 退出浏览器实例
    driver.quit()
