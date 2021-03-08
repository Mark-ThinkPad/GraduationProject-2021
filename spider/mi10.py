import re
import json
from time import sleep
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from spider.utils import (set_options, set_capabilities, get_response_body, window_scroll_by)
from db.mi10_models import Shop, Sku, Comment, CommentSummary, ModelSummary


# 获取京东数据
def get_data_from_jd(browser: Chrome, shop: Shop):
    browser.get(shop.url)  # 打开商品页面
    # 获取京东商品已上架SKU
    # get_jd_sku_from_api(browser, shop)
    # 获取默认总推荐排序评论和默认总时间排序, 并遍历所有SKU
    switch_to_jd_default_comments_page(browser)  # 打开评论默认页面
    # get_jd_comments(browser, shop, get_sku=True)  # 从全部评价标签获取评论
    switch_to_good_comments(browser)  # 切换到好评
    # get_jd_comments(browser, shop, get_sku=True)  # 从好评标签获取评论
    switch_to_general_comments(browser)  # 切换到中评
    # get_jd_comments(browser, shop, get_sku=True)  # 从中评标签获取评论
    switch_to_bad_comments(browser)  # 切换到差评
    # get_jd_comments(browser, shop, get_sku=True)  # 从差评标签获取评论
    switch_to_total_comments(browser)  # 切回全部评论
    switch_to_time_sort(browser)  # 切换到时间排序
    # get_jd_comments(browser, shop, get_sku=True)  # 从全部评价标签获取评论
    switch_to_video_comments(browser)  # 切换到视频晒单
    # get_jd_comments(browser, shop, get_sku=True)  # 从视频晒单标签获取评论
    switch_to_after_comments(browser)  # 切换到追评
    # get_jd_comments(browser, shop, get_sku=True)  # 从追评标签获取评论
    switch_to_good_comments(browser)  # 切换到好评
    # get_jd_comments(browser, shop, get_sku=True)  # 从好评标签获取评论
    switch_to_general_comments(browser)  # 切换到中评
    # get_jd_comments(browser, shop, get_sku=True)  # 从中评标签获取评论
    switch_to_bad_comments(browser)  # 切换到差评
    # get_jd_comments(browser, shop, get_sku=True)  # 从差评标签获取评论

    browser.close()


# 从getstocks接口获取已上架的SKU
def get_jd_sku_from_api(browser: Chrome, shop: Shop):
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


# 打开新窗口并切换到默认评论页面
def switch_to_jd_default_comments_page(browser: Chrome):
    driver.execute_script("window.open()")
    handles = driver.window_handles
    driver.switch_to.window(handles[1])
    browser.get(shop.url + '#comment')


# 等待评论加载
def waiting_comments_loading(browser: Chrome):
    while True:
        try:
            WebDriverWait(browser, 0.5).until(
                ec.presence_of_all_elements_located((By.CLASS_NAME, 'comment-item'))
            )
            break
        except TimeoutException:
            pass


# 评论页面切换到时间排序
def switch_to_time_sort(browser: Chrome):
    browser.execute_script('document.querySelector("li.J-sortType-item:nth-child(2)").click()')
    waiting_comments_loading(browser)
    sleep(2)


# 评论页面切换到全部评价
def switch_to_total_comments(browser: Chrome):
    browser.execute_script('document.querySelector(".filter-list > li:nth-child(1) > a:nth-child(1)").click()')
    waiting_comments_loading(browser)
    sleep(2)


# 评论页面切换到视频晒单
def switch_to_video_comments(browser: Chrome):
    browser.execute_script('document.querySelector(".filter-list > li:nth-child(3) > a:nth-child(1)").click()')
    waiting_comments_loading(browser)
    sleep(2)


# 评论页面切换到追评
def switch_to_after_comments(browser: Chrome):
    browser.execute_script('document.querySelector(".J-addComment > a:nth-child(1)").click()')
    waiting_comments_loading(browser)
    sleep(2)


# 评论页面切换到好评
def switch_to_good_comments(browser: Chrome):
    browser.execute_script('document.querySelector(".filter-list > li:nth-child(5) > a:nth-child(1)").click()')
    waiting_comments_loading(browser)
    sleep(2)


# 评论页面切换到中评
def switch_to_general_comments(browser: Chrome):
    browser.execute_script('document.querySelector(".filter-list > li:nth-child(6) > a:nth-child(1)").click()')
    waiting_comments_loading(browser)
    sleep(2)


# 评论页面切换到差评
def switch_to_bad_comments(browser: Chrome):
    browser.execute_script('document.querySelector(".filter-list > li:nth-child(7) > a:nth-child(1)").click()')
    waiting_comments_loading(browser)
    sleep(2)


# 从默认评论排序中获取所有SKU, 顺便保存评论
def get_jd_comments(browser: Chrome, shop: Shop, get_sku: bool = False, sku_mode: bool = False):
    max_page = 101
    while max_page > 0:
        # 获取评论
        jd_comments_url = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98'
        jd_comments = get_response_body(browser, jd_comments_url, 'GET')
        jd_comments = jd_comments.lstrip('fetchJSON_comment98(').rstrip(');')
        jd_comments = json.loads(jd_comments)
        # 赋值最大页数
        if max_page == 101:
            max_page = jd_comments['maxPage']
            if sku_mode is True:
                pass
        # 保存评论
        comment_list = jd_comments['comments']
        insert_jd_comments(comment_list, shop)
        # 遍历评论中的所有SKU
        if get_sku is True:
            get_sku_from_jd_comments(comment_list, shop)
        # 最后一页就不下滑了
        max_page -= 1
        print(max_page)
        if max_page == 0:
            break
        # 下滑点击下一页
        while True:
            try:
                WebDriverWait(browser, 0.5).until(
                    ec.element_to_be_clickable((By.CLASS_NAME, 'ui-pager-next'))
                )
                browser.execute_script('document.getElementsByClassName("ui-pager-next")[0].click()')
                waiting_comments_loading(browser)
                sleep(2)
                break
            except TimeoutException:
                window_scroll_by(browser, 200)


# 保存京东评论
def insert_jd_comments(comment_list, shop: Shop):
    for comment in comment_list:
        new_comment, created = Comment.get_or_create(
            source=shop.source,
            is_official=shop.is_official,
            comment_id='JD' + str(comment['id']),
            create_time=comment['creationTime'],
            content=comment['content'],
            star=comment['score'],
            order_time=comment['referenceTime'],
            order_days=comment['days'],
            product_color=comment['productColor'],
            product_ram=re.match(r'^\w+?\+', comment['productSize']).group().replace('+', ''),
            product_rom=re.search(r'\+\w+?$', comment['productSize']).group().replace('+', '')
        )
        if created is True:
            if 'afterUserComment' in comment:
                after_comment = comment['afterUserComment']
                new_comment.after_time = after_comment['created'][0:9]
                new_comment.after_content = after_comment['content']
                new_comment.after_days = comment['afterDays']
            if comment['userClient'] == 4:
                new_comment.user_device = 'Android'
            elif comment['userClient'] == 2:
                new_comment.user_device = 'iOS'
            else:
                new_comment.user_device = 'other'
            new_comment.save()


# 从评论中获取SKU
def get_sku_from_jd_comments(comment_list: list, shop: Shop):
    for comment in comment_list:
        try:
            Sku.get(
                source=shop.source,
                sku=comment['referenceId']
            )
        except Sku.DoesNotExist:
            Sku.create(
                source=shop.source,
                is_official=shop.is_official,
                sku=comment['referenceId'],
                url_prefix='https://item.jd.com/',
                shop=shop,
            )


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
