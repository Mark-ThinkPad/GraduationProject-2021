import re
import json
from time import sleep
from random import uniform
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support import expected_conditions as ec
from db.mi10_models import Shop, Sku, Comment, CommentSummary, ModelSummary
from spider.utils import (set_options, set_capabilities, get_response_body, get_response_body_list, window_scroll_by)


# 获取苏宁易购的小米10销售数据
def get_mi10_data_from_sn(browser: Chrome):
    for sn_shop in Shop.select().where(Shop.source == '苏宁'):
        print(f'------打开当前苏宁店铺链接: {sn_shop.url}------')
        browser.get(sn_shop.url)
        # 获取所有SKU和评论统计
        get_sn_sku_and_comment_summary_from_api(browser, sn_shop)

        # 获取默认排序评论, 并遍历所有SKU
        print('------开始获取默认排序评论------')
        switch_to_sn_default_comments_page(browser, sn_shop.url)
        get_sn_comments(browser, sn_shop)

        # # 轮询各个SKU的商品页面
        # print('------SKU轮询开始------')
        # for current_sku in sn_shop.sku:
        #     print(f'------本轮SKU: {current_sku.sku}------')
        #     current_sku_url = current_sku.url_prefix + current_sku.shop_code + '/' + current_sku.sku + '.html'
        #     print(f'------正在打开当前SKU链接: {current_sku_url}------')
        #     browser.get(current_sku_url)
        #     sleep(10)


# 获取所有SKU和评论统计 (苏宁自营店页面返回了两个接口数据)
def get_sn_sku_and_comment_summary_from_api(browser: Chrome, shop: Shop):
    skus_list = []
    summary = {}
    sn_sku_target = [
        {'url': 'getClusterPrice', 'method': 'GET'},
        {'url': 'cluster_review_satisfy', 'method': 'GET'}
    ]
    all_data = get_response_body_list(browser, sn_sku_target)
    for data in all_data:
        if data['url'] == 'getClusterPrice' and data['method'] == 'GET':
            skus_list.append(data['response_body'])
        if data['url'] == 'cluster_review_satisfy' and data['method'] == 'GET':
            summary = data['response_body']

    for skus in skus_list:
        skus = skus.lstrip('getClusterPrice(').rstrip(');')
        skus = json.loads(skus)
        for sku in skus:
            Sku.create(
                source=shop.source,
                is_official=shop.is_official,
                sku=sku['cmmdtyCode'].replace(re.match(r'^[0]+', sku['cmmdtyCode']).group(), ''),
                url_prefix='https://product.suning.com/',
                shop_code=sku['vendorCode'],
                shop=shop
            )
    print('------获取所有SKU完成------')

    summary = summary.lstrip('satisfy(').rstrip(')')
    summary = json.loads(summary)
    if summary['returnMsg'] == '查询数量成功':
        review_count = summary['reviewCounts'][0]
        CommentSummary.create(
            source=shop.source,
            is_official=shop.is_official,
            total=review_count['totalCount'],
            good_rate=str(review_count['goodRate']),
            default_good=review_count['defaultCount'],
            star_one=review_count['oneStarCount'],
            star_two=review_count['twoStarCount'],
            star_three=review_count['threeStarCount'],
            star_four=review_count['fourStarCount'],
            star_five=review_count['fiveStarCount'],
        )
        print('------保存商品评论统计数量完成------')
    else:
        print('------查询商品评论统计数量失败------')


# 打开新窗口并切换到默认评论页面
def switch_to_sn_default_comments_page(browser: Chrome, shop_url: str):
    browser.execute_script("window.open()")
    handles = browser.window_handles
    browser.switch_to.window(handles[1])
    print('------打开新窗口并正在加载默认评论页面------')
    browser.get(shop_url + '#productCommTitle')
    browser.execute_script('document.querySelector("#productCommTitle > a:nth-child(1)").click()')
    print('------默认评论页面加载完成------')
    waiting_sn_comments_loading(browser)


# 打开新窗口并切换到具体SKU评论页面
def switch_to_sn_sku_comments_page(browser: Chrome, sku_url: str):
    browser.execute_script("window.open()")
    handles = browser.window_handles
    browser.switch_to.window(handles[1])
    print('------打开新窗口并正在加载当前SKU默认评论页面------')
    browser.get(sku_url + '#productCommTitle')
    browser.execute_script('document.querySelector("#productCommTitle > a:nth-child(1)").click()')
    waiting_sn_comments_loading(browser)
    browser.execute_script('document.querySelector(".uncheck").click()')
    print('------当前SKU默认评论页面加载完成------')
    waiting_sn_comments_loading(browser)


# 等待苏宁评论加载
def waiting_sn_comments_loading(browser: Chrome):
    while True:
        try:
            WebDriverWait(browser, 0.5).until(
                ec.presence_of_all_elements_located((By.CLASS_NAME, 'rv-target-item'))
            )
            interval_time = uniform(3, 6)  # 随机生成间隔秒数
            print(f'本次随机间隔时间: {interval_time} 秒')
            sleep(interval_time)  # 停顿一下, 降低访问频率
            break
        except TimeoutException:
            pass


#  回到第一个窗口
def back_to_first_window(browser: Chrome):
    browser.close()
    handles = browser.window_handles
    browser.switch_to.window(handles[0])


# 获取苏宁评论
def get_sn_comments(browser: Chrome, shop: Shop, sku_mode: bool = False):
    page = 1
    while True:
        try:
            # 获取评论
            if sku_mode is True and page == 1:
                sn_comments = {}
                sn_model_summary = {}
                target_urls = [
                    {'url': 'cluster_review_lists/general', 'method': 'GET'},
                    {'url': 'review_count/general', 'method': 'GET'}
                ]
                all_data = get_response_body_list(browser, target_urls)
                for data in all_data:
                    if data['url'] == 'cluster_review_lists/general' and data['method'] == 'GET':
                        sn_comments = data['response_body']
                        sn_comments = sn_comments.lstrip('reviewList(').rstrip(')')
                        sn_comments = json.loads(sn_comments)
                    if data['url'] == 'review_count/general' and data['method'] == 'GET':
                        sn_model_summary = data['response_body']
                        sn_model_summary = sn_model_summary.lstrip('satisfy(').rstrip(')')
                        sn_model_summary = json.loads(sn_model_summary)
                if sn_comments['returnMsg'] == '无评价数据':
                    break
                else:
                    if sn_model_summary['returnMsg'] == '查询数量成功':
                        insert_sn_model_summary(sn_model_summary['reviewCounts'][0],
                                                sn_comments['commodityReviews'][0], shop)
                    else:
                        print('---查询当前SKU评论统计数量失败---')
            else:
                if sku_mode is False:
                    sn_comments_url = 'cluster_review_lists/cluster'
                else:
                    sn_comments_url = 'cluster_review_lists/general'
                sn_comments = get_response_body(browser, sn_comments_url, 'GET')
                sn_comments = sn_comments.lstrip('reviewList(').rstrip(')')
                sn_comments = json.loads(sn_comments)

            # 保存评论
            if sn_comments['returnMsg'] == '成功取得评价列表':
                comment_list = sn_comments['commodityReviews']
                insert_sn_comments(comment_list, shop)
            else:
                break
        except WebDriverException:
            print('---此页评论数据获取异常, 跳过此轮---')
            break

        print(f'当前页数: {page}')
        # 下滑点击下一页
        while True:
            try:
                WebDriverWait(browser, 0.5).until(
                    ec.element_to_be_clickable((By.CSS_SELECTOR, '.next.rv-maidian'))
                )
                browser.execute_script('document.getElementsByClassName("next rv-maidian")[0].click()')
                waiting_sn_comments_loading(browser)
                break
            except TimeoutException:
                window_scroll_by(browser, 500)

        page += 1

    back_to_first_window(browser)


# 保存苏宁评论
def insert_sn_comments(comment_list: list, shop: Shop):
    for comment in comment_list:
        productColor, productRam, productRom = parse_sn_mi10_product_info(comment)
        new_comment, created = Comment.get_or_create(
            source=shop.source,
            is_official=shop.is_official,
            comment_id='JD' + str(comment['commodityReviewId']),
            create_time=comment['publishTime'],
            content=comment['content'],
            star=comment['qualityStar'],
            user_device=comment['sourceSystem'],
            product_color=productColor,
            product_ram=productRam,
            product_rom=productRom
        )
        if created is True:
            if comment['againFlag'] is True:
                after_comment = comment['againReview']
                new_comment.after_time = after_comment['publishTime']
                new_comment.after_content = after_comment['againContent']
                after_days_str = after_comment['publishTimeStr']
                if after_days_str == '当天追加':
                    after_days_num = 0
                else:
                    after_days_num = int(re.match(r'^\d+', after_days_str).group())
                new_comment.after_days = after_days_num
            new_comment.save()


# 解析小米10产品信息
def parse_sn_mi10_product_info(commodity_info) -> tuple:
    product_color = commodity_info['charaterDesc1']
    if '灰' in product_color:
        product_color = '国风雅灰'
    if '黑' in product_color:
        product_color = '钛银黑'
    if '蓝' in product_color:
        product_color = '冰海蓝'
    if '金' in product_color:
        product_color = '蜜桃金'
    product_ram_and_rom = re.search(r'\d+[GB]*\+\d+[GB]*', commodity_info['charaterDesc2']).group().split('+')
    product_ram = product_ram_and_rom[0]
    product_rom = product_ram_and_rom[1]
    if 'G' not in product_ram:
        product_ram += 'GB'
    elif 'B' not in product_ram:
        product_ram += 'B'
    if 'G' not in product_rom:
        product_rom += 'GB'
    elif 'B' not in product_rom:
        product_rom += 'B'
    return product_color, product_ram, product_rom


# 保存型号统计数据
def insert_sn_model_summary(model_summary: dict, comment: dict, shop: Shop):
    pass


if __name__ == '__main__':
    options = set_options()
    caps = set_capabilities()
    # 在Windows环境下已将chromedriver添加至环境变量, 无需声明执行文件路径
    # 在Arch Linux环境下, 使用archlinux cn源安装的chromedriver位置在/usr/bin, 也无需声明执行文件路径
    driver = Chrome(options=options, desired_capabilities=caps)
    # 从苏宁获得数据
    get_mi10_data_from_sn(driver)
    # 退出浏览器实例
    driver.quit()
