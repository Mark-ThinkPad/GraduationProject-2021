import re
import json
from time import sleep
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, WebDriverException
from db.mi10_models import Shop, Sku, Comment, CommentSummary, ModelSummary
from spider.utils import (get_chrome_driver, get_response_body, window_scroll_by, parse_jd_count_str,
                          open_second_window, back_to_first_window, parse_mi10_product_info, calculate_mi10_good_rate,
                          waiting_comments_loading)


# 获取京东商城的小米10销售数据
def get_mi10_data_from_jd(browser: Chrome):
    for jd_shop in Shop.select().where(Shop.source == '京东'):
        print(f'------打开当前京东商品链接: {jd_shop.url}------')
        browser.get(jd_shop.url)  # 打开商品页面
        # 获取已上架SKU
        get_jd_sku_from_api(browser, jd_shop)

        # 获取默认推荐排序评论和默认时间排序评论, 并遍历所有SKU
        print('------开始获取默认推荐排序评论------')
        switch_to_jd_default_comments_page(browser, jd_shop.url)  # 打开评论默认页面
        get_jd_comments(browser, jd_shop, get_sku=True, summary=True)  # 从全部评价标签获取评论和统计信息

        print('------开始获取默认时间排序评论------')
        switch_to_jd_default_comments_page(browser, jd_shop.url)
        switch_to_jd_time_sort(browser)  # 切换到时间排序
        get_jd_comments(browser, jd_shop, get_sku=True)  # 从全部评价标签获取评论

        # 轮询各个SKU的商品页面
        print('------SKU轮询开始------')
        for current_sku in jd_shop.sku:
            print(f'------本轮SKU: {current_sku.sku}------')
            current_sku_url = current_sku.url_prefix + current_sku.sku + '.html'
            print(f'------正在打开当前SKU链接: {current_sku_url}------')
            browser.get(current_sku_url)

            print('------开始获取当前SKU推荐排序评论------')
            switch_to_jd_sku_comments_page(browser, current_sku_url)
            get_jd_comments(browser, jd_shop, sku_mode=True, summary=True)  # 从全部评价标签获取评论和统计信息

            print('------开始获取当前SKU时间排序评论------')
            switch_to_jd_sku_comments_page(browser, current_sku_url)
            switch_to_jd_time_sort(browser)  # 切换到时间排序
            get_jd_comments(browser, jd_shop, sku_mode=True)  # 从全部评价标签获取评论

    # 数据汇总后计算最终好评率
    calculate_mi10_good_rate(CommentSummary.select().where(CommentSummary.source == '京东'))
    calculate_mi10_good_rate(ModelSummary.select().where(ModelSummary.source == '京东'))
    print('------京东平台数据获取完成------')


# 从后端API接口获取已上架的SKU
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
    print('------获取已上架SKU完成------')


# 打开新窗口并切换到默认评论页面
def switch_to_jd_default_comments_page(browser: Chrome, shop_url: str):
    open_second_window(browser)
    print('------打开新窗口并正在加载默认评论页面------')
    browser.get(shop_url + '#comment')
    print('------默认评论页面加载完成------')
    waiting_comments_loading(browser, 'comment-item')


# 打开新窗口并切换到具体SKU评论页面
def switch_to_jd_sku_comments_page(browser: Chrome, sku_url: str):
    open_second_window(browser)
    print('------打开新窗口并正在加载当前SKU默认评论页面------')
    browser.get(sku_url + '#comment')
    browser.execute_script('document.getElementById("comm-curr-sku").click()')
    print('------当前SKU默认评论页面加载完成------')
    waiting_comments_loading(browser, 'comment-item')


# 评论页面切换到时间排序
def switch_to_jd_time_sort(browser: Chrome):
    browser.execute_script('document.querySelector("li.J-sortType-item:nth-child(2)").click()')
    print('------切换到时间排序------')
    waiting_comments_loading(browser, 'comment-item')


# 从默认评论排序中获取所有SKU, 也可以顺便保存评论
def get_jd_comments(browser: Chrome, shop: Shop, get_sku: bool = False, sku_mode: bool = False, summary: bool = False):
    max_page = 141
    while max_page > 0:
        try:
            # 获取评论
            if sku_mode is True:
                jd_comments_url = 'skuProductPageComments'
            else:
                jd_comments_url = 'productPageComments'
            jd_comments = get_response_body(browser, jd_comments_url, 'GET')
            if jd_comments is None:
                print('---未找到评论接口数据---')
                raise WebDriverException(msg='jd_comments is None')
            jd_comments = jd_comments.lstrip('fetchJSON_comment98(').rstrip(');')
            jd_comments = json.loads(jd_comments)
            # 保存评论
            comment_list = jd_comments['comments']
            insert_jd_comments(comment_list, shop)
            if len(comment_list) == 0:
                print('该页评论数据0条')
            # 遍历评论中的所有SKU
            if get_sku is True:
                get_sku_from_jd_comments(comment_list, shop)
        except WebDriverException:
            print('---此页评论数据获取异常, 跳过此分类---')
            break
        # 赋值最大页数
        if max_page == 141:
            max_page = jd_comments['maxPage']
            if sku_mode and summary:
                sku_summary = jd_comments['productCommentSummary']
                first_comment = comment_list[0]
                insert_jd_model_summary(sku_summary, first_comment, shop)
            elif summary is True:
                total_summary = jd_comments['productCommentSummary']
                insert_jd_comment_summary(total_summary, shop)
        # 最后一页就不下滑了
        max_page -= 1
        print(f'剩余页数: {max_page}')
        if max_page == 0:
            break
        # 下滑点击下一页
        while True:
            try:
                WebDriverWait(browser, 0.5).until(
                    ec.element_to_be_clickable((By.CLASS_NAME, 'ui-pager-next'))
                )
                browser.execute_script('document.getElementsByClassName("ui-pager-next")[0].click()')
                waiting_comments_loading(browser, 'comment-item')
                break
            except TimeoutException:
                window_scroll_by(browser, 200)

    back_to_first_window(browser)
    print('------当前浏览器窗口已关闭, 暂停10秒------')
    sleep(10)


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


# 保存京东评论
def insert_jd_comments(comment_list: list, shop: Shop):
    for comment in comment_list:
        color, ram, rom = parse_mi10_product_info(comment['productColor'], comment['productSize'])
        new_comment, created = Comment.get_or_create(
            source=shop.source,
            is_official=shop.is_official,
            comment_id='JD' + str(comment['id']),
            create_time=comment['creationTime'],
            content=comment['content'],
            star=comment['score'],
            order_time=comment['referenceTime'],
            order_days=comment['days'],
            product_color=color,
            product_ram=ram,
            product_rom=rom
        )
        if created is True:
            if 'afterUserComment' in comment:
                after_comment = comment['afterUserComment']
                new_comment.after_time = after_comment['created']
                new_comment.after_content = after_comment['content']
                new_comment.after_days = comment['afterDays']
            if comment['userClient'] == 4:
                new_comment.user_device = 'Android'
            elif comment['userClient'] == 2:
                new_comment.user_device = 'iOS'
            else:
                new_comment.user_device = 'other'
            new_comment.save()


# 更新统计数据
def update_jd_summary_data(s, summary):
    s.total += parse_jd_count_str(summary['commentCountStr'])
    s.default_good += parse_jd_count_str(summary['defaultGoodCountStr'])
    s.star_one += summary['score1Count']
    s.star_two += summary['score2Count']
    s.star_three += summary['score3Count']
    s.star_four += summary['score4Count']
    s.star_five += summary['score5Count']
    s.save()


# 保存评论统计数据
def insert_jd_comment_summary(comment_summary: dict, shop: Shop):
    try:
        cs = CommentSummary.get(
            source=shop.source,
            is_official=shop.is_official
        )
        update_jd_summary_data(cs, comment_summary)
    except CommentSummary.DoesNotExist:
        CommentSummary.create(
            source=shop.source,
            is_official=shop.is_official,
            total=parse_jd_count_str(comment_summary['commentCountStr']),
            good_rate=str(comment_summary['goodRate'] * 100),
            default_good=parse_jd_count_str(comment_summary['defaultGoodCountStr']),
            star_one=comment_summary['score1Count'],
            star_two=comment_summary['score2Count'],
            star_three=comment_summary['score3Count'],
            star_four=comment_summary['score4Count'],
            star_five=comment_summary['score5Count']
        )


# 保存型号统计数据
def insert_jd_model_summary(model_summary: dict, comment: dict, shop: Shop):
    color, ram, rom = parse_mi10_product_info(comment['productColor'], comment['productSize'])
    try:
        ms = ModelSummary.get(
            source=shop.source,
            is_official=shop.is_official,
            product_color=color,
            product_ram=ram,
            product_rom=rom
        )
        update_jd_summary_data(ms, model_summary)
    except ModelSummary.DoesNotExist:
        ModelSummary.create(
            source=shop.source,
            is_official=shop.is_official,
            product_color=color,
            product_ram=ram,
            product_rom=rom,
            total=parse_jd_count_str(model_summary['commentCountStr']),
            good_rate=str(model_summary['goodRate'] * 100),
            default_good=parse_jd_count_str(model_summary['defaultGoodCountStr']),
            star_one=model_summary['score1Count'],
            star_two=model_summary['score2Count'],
            star_three=model_summary['score3Count'],
            star_four=model_summary['score4Count'],
            star_five=model_summary['score5Count']
        )


if __name__ == '__main__':
    # 创建一个chrome实例
    driver = get_chrome_driver()
    # 从京东获得数据
    get_mi10_data_from_jd(driver)
    # 退出浏览器实例
    driver.quit()
