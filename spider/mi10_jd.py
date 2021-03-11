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
from spider.utils import (set_options, set_capabilities, get_response_body, window_scroll_by, parse_jd_count_str)


# 获取京东商城的小米10销售数据
def get_mi10_data_from_jd(browser: Chrome):
    for jd_shop in Shop.select().where(Shop.source == '京东'):
        print(f'------打开当前京东店铺链接: {jd_shop.url}------')
        browser.get(jd_shop.url)  # 打开商品页面
        # 获取已上架SKU
        get_jd_sku_from_api(browser, jd_shop)

        # 获取默认总推荐排序评论和默认总时间排序评论, 并遍历所有SKU
        print('------获取默认总推荐排序评论和默认总时间排序评论, 并遍历所有SKU------')
        switch_to_jd_default_comments_page(browser, jd_shop)  # 打开评论默认页面
        get_jd_comments(browser, jd_shop, get_sku=True, summary=True)  # 从全部评价标签获取评论和统计信息

        # # switch_to_jd_default_comments_page(browser, jd_shop)
        # switch_to_jd_good_comments(browser)  # 切换到好评
        # get_jd_comments(browser, jd_shop, get_sku=True)  # 从好评标签获取评论
        #
        # # switch_to_jd_default_comments_page(browser, jd_shop)
        # switch_to_jd_general_comments(browser)  # 切换到中评
        # get_jd_comments(browser, jd_shop, get_sku=True)  # 从中评标签获取评论
        #
        # # switch_to_jd_default_comments_page(browser, jd_shop)
        # switch_to_jd_bad_comments(browser)  # 切换到差评
        # get_jd_comments(browser, jd_shop, get_sku=True)  # 从差评标签获取评论

        # switch_to_jd_total_comments(browser)  # 切回全部评论
        switch_to_jd_default_comments_page(browser, jd_shop)
        switch_to_jd_time_sort(browser)  # 切换到时间排序
        get_jd_comments(browser, jd_shop, get_sku=True)  # 从全部评价标签获取评论

        # # switch_to_jd_default_comments_page(browser, jd_shop)
        # # switch_to_jd_time_sort(browser)
        # switch_to_jd_video_comments(browser)  # 切换到视频晒单
        # get_jd_comments(browser, jd_shop, get_sku=True)  # 从视频晒单标签获取评论
        #
        # # switch_to_jd_default_comments_page(browser, jd_shop)
        # # switch_to_jd_time_sort(browser)
        # switch_to_jd_after_comments(browser)  # 切换到追评
        # get_jd_comments(browser, jd_shop, get_sku=True)  # 从追评标签获取评论
        #
        # # switch_to_jd_default_comments_page(browser, jd_shop)
        # # switch_to_jd_time_sort(browser)
        # switch_to_jd_good_comments(browser)  # 切换到好评
        # get_jd_comments(browser, jd_shop, get_sku=True)  # 从好评标签获取评论
        #
        # # switch_to_jd_default_comments_page(browser, jd_shop)
        # # switch_to_jd_time_sort(browser)
        # switch_to_jd_general_comments(browser)  # 切换到中评
        # get_jd_comments(browser, jd_shop, get_sku=True)  # 从中评标签获取评论
        #
        # # switch_to_jd_default_comments_page(browser, jd_shop)
        # # switch_to_jd_time_sort(browser)
        # switch_to_jd_bad_comments(browser)  # 切换到差评
        # get_jd_comments(browser, jd_shop, get_sku=True)  # 从差评标签获取评论
        # back_to_first_window(browser)

        # 轮询各个SKU的商品页面
        skus = jd_shop.sku  # 通过shop模型反向查询所有sku
        print('------SKU轮询开始------')
        for current_sku in skus:
            print(f'------本轮SKU: {current_sku.sku}------')
            current_sku_url = current_sku.url_prefix + current_sku.sku + '.html'
            print(f'------正在打开当前SKU链接: {current_sku_url}------')
            browser.get(current_sku_url)
            switch_to_jd_sku_comments_page(browser, current_sku)
            get_jd_comments(browser, jd_shop, sku_mode=True, summary=True)  # 从全部评价标签获取评论和统计信息

            # # switch_to_jd_sku_comments_page(browser, current_sku)
            # switch_to_jd_good_comments(browser)  # 切换到好评
            # get_jd_comments(browser, jd_shop, sku_mode=True)  # 从好评标签获取评论
            #
            # # switch_to_jd_sku_comments_page(browser, current_sku)
            # switch_to_jd_general_comments(browser)  # 切换到中评
            # get_jd_comments(browser, jd_shop, sku_mode=True)  # 从中评标签获取评论
            #
            # # switch_to_jd_sku_comments_page(browser, current_sku)
            # switch_to_jd_bad_comments(browser)  # 切换到差评
            # get_jd_comments(browser, jd_shop, sku_mode=True)  # 从差评标签获取评论

            # switch_to_jd_total_comments(browser)  # 切回全部评论
            switch_to_jd_sku_comments_page(browser, current_sku)
            switch_to_jd_time_sort(browser)  # 切换到时间排序
            get_jd_comments(browser, jd_shop, sku_mode=True)  # 从全部评价标签获取评论

            # # switch_to_jd_sku_comments_page(browser, current_sku)
            # # switch_to_jd_time_sort(browser)  # 切换到时间排序
            # switch_to_jd_video_comments(browser)  # 切换到视频晒单
            # get_jd_comments(browser, jd_shop, sku_mode=True)  # 从视频晒单标签获取评论
            #
            # # switch_to_jd_sku_comments_page(browser, current_sku)
            # # switch_to_jd_time_sort(browser)  # 切换到时间排序
            # switch_to_jd_after_comments(browser)  # 切换到追评
            # get_jd_comments(browser, jd_shop, sku_mode=True)  # 从追评标签获取评论
            #
            # # switch_to_jd_sku_comments_page(browser, current_sku)
            # # switch_to_jd_time_sort(browser)  # 切换到时间排序
            # switch_to_jd_good_comments(browser)  # 切换到好评
            # get_jd_comments(browser, jd_shop, sku_mode=True)  # 从好评标签获取评论
            #
            # # switch_to_jd_sku_comments_page(browser, current_sku)
            # # switch_to_jd_time_sort(browser)  # 切换到时间排序
            # switch_to_jd_general_comments(browser)  # 切换到中评
            # get_jd_comments(browser, jd_shop, sku_mode=True)  # 从中评标签获取评论
            #
            # # switch_to_jd_sku_comments_page(browser, current_sku)
            # # switch_to_jd_time_sort(browser)  # 切换到时间排序
            # switch_to_jd_bad_comments(browser)  # 切换到差评
            # get_jd_comments(browser, jd_shop, sku_mode=True)  # 从差评标签获取评论
            # back_to_first_window(browser)

    # 数据汇总后计算总好评率
    calculate_jd_good_rate(CommentSummary.select())
    calculate_jd_good_rate(ModelSummary.select())
    print('------京东平台数据获取完成------')


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
    print('------获取已上架SKU完成------')


# 打开新窗口并切换到默认评论页面
def switch_to_jd_default_comments_page(browser: Chrome, shop: Shop):
    browser.execute_script("window.open()")
    handles = browser.window_handles
    browser.switch_to.window(handles[1])
    print('------打开新窗口并正在加载默认评论页面------')
    browser.get(shop.url + '#comment')
    print('------默认评论页面加载完成------')
    waiting_jd_comments_loading(browser)


# 打开新窗口并切换到具体SKU评论页面
def switch_to_jd_sku_comments_page(browser: Chrome, sku: Sku):
    browser.execute_script("window.open()")
    handles = browser.window_handles
    driver.switch_to.window(handles[1])
    print('------打开新窗口并正在加载当前SKU默认评论页面------')
    browser.get(sku.url_prefix + sku.sku + '.html#comment')
    browser.execute_script('document.getElementById("comm-curr-sku").click()')
    # browser.find_element_by_id('comm-curr-sku').click()
    print('------当前SKU默认评论页面加载完成------')
    waiting_jd_comments_loading(browser)


# 等待京东评论加载
def waiting_jd_comments_loading(browser: Chrome):
    while True:
        try:
            WebDriverWait(browser, 0.5).until(
                ec.presence_of_all_elements_located((By.CLASS_NAME, 'comment-item'))
            )
            interval_time = uniform(3, 6)  # 随机生成间隔秒数
            print(f'本次随机间隔时间: {interval_time} 秒')
            sleep(interval_time)  # 停顿一下, 降低访问频率
            break
        except TimeoutException:
            pass


# 评论页面切换到时间排序
def switch_to_jd_time_sort(browser: Chrome):
    browser.execute_script('document.querySelector("li.J-sortType-item:nth-child(2)").click()')
    print('------切换到时间排序------')
    waiting_jd_comments_loading(browser)


# 评论页面切换到全部评价
def switch_to_jd_total_comments(browser: Chrome):
    # browser.find_element_by_css_selector('.filter-list > li:nth-child(1) > a:nth-child(1)').click()
    browser.execute_script('document.querySelector(".filter-list > li:nth-child(1) > a:nth-child(1)").click()')
    print('------切换到全部评价------')
    waiting_jd_comments_loading(browser)


# 评论页面切换到视频晒单
def switch_to_jd_video_comments(browser: Chrome):
    # browser.find_element_by_css_selector('.filter-list > li:nth-child(3) > a:nth-child(1)').click()
    browser.execute_script('document.querySelector(".filter-list > li:nth-child(3) > a:nth-child(1)").click()')
    print('------切换到视频晒单------')
    waiting_jd_comments_loading(browser)


# 评论页面切换到追评
def switch_to_jd_after_comments(browser: Chrome):
    # browser.find_element_by_css_selector('.J-addComment > a:nth-child(1)').click()
    browser.execute_script('document.querySelector(".J-addComment > a:nth-child(1)").click()')
    print('------切换到追评------')
    waiting_jd_comments_loading(browser)


# 评论页面切换到好评
def switch_to_jd_good_comments(browser: Chrome):
    # browser.find_element_by_css_selector('.filter-list > li:nth-child(5) > a:nth-child(1)').click()
    browser.execute_script('document.querySelector(".filter-list > li:nth-child(5) > a:nth-child(1)").click()')
    print('------切换到好评------')
    waiting_jd_comments_loading(browser)


# 评论页面切换到中评
def switch_to_jd_general_comments(browser: Chrome):
    # browser.find_element_by_css_selector('.filter-list > li:nth-child(6) > a:nth-child(1)').click()
    browser.execute_script('document.querySelector(".filter-list > li:nth-child(6) > a:nth-child(1)").click()')
    print('------切换到中评------')
    waiting_jd_comments_loading(browser)


# 评论页面切换到差评
def switch_to_jd_bad_comments(browser: Chrome):
    # browser.find_element_by_css_selector('.filter-list > li:nth-child(7) > a:nth-child(1)').click()
    browser.execute_script('document.querySelector(".filter-list > li:nth-child(7) > a:nth-child(1)").click()')
    print('------切换到差评------')
    waiting_jd_comments_loading(browser)


#  回到第一个窗口
def back_to_first_window(browser: Chrome):
    browser.close()
    handles = browser.window_handles
    browser.switch_to.window(handles[0])


# 从默认评论排序中获取所有SKU, 顺便保存评论
def get_jd_comments(browser: Chrome, shop: Shop, get_sku: bool = False, sku_mode: bool = False, summary: bool = False):
    max_page = 141
    # jd_comments = {}
    # comment_list = []
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
                waiting_jd_comments_loading(browser)
                break
            except TimeoutException:
                window_scroll_by(browser, 200)

    back_to_first_window(browser)
    print('------当前浏览器窗口已关闭, 暂停10秒------')
    # print('------暂停10秒------')
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
        productColor, productRam, productRom = parse_jd_mi10_product_info(comment)
        new_comment, created = Comment.get_or_create(
            source=shop.source,
            is_official=shop.is_official,
            comment_id='JD' + str(comment['id']),
            create_time=comment['creationTime'],
            content=comment['content'],
            star=comment['score'],
            order_time=comment['referenceTime'],
            order_days=comment['days'],
            product_color=productColor,
            product_ram=productRam,
            product_rom=productRom
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


# 解析小米10产品信息
def parse_jd_mi10_product_info(comment) -> tuple:
    product_color = comment['productColor']
    if '国风雅灰' in product_color:
        product_color = '国风雅灰'
    if '钛银黑' in product_color:
        product_color = '钛银黑'
    if '冰海蓝' in product_color:
        product_color = '冰海蓝'
    if '蜜桃金' in product_color:
        product_color = '蜜桃金'
    product_ram_and_rom = re.search(r'\d+[GB]*\+\d+[GB]*', comment['productSize']).group().split('+')
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
            good_rate=comment_summary['goodRate'] * 100,
            default_good=parse_jd_count_str(comment_summary['defaultGoodCountStr']),
            star_one=comment_summary['score1Count'],
            star_two=comment_summary['score2Count'],
            star_three=comment_summary['score3Count'],
            star_four=comment_summary['score4Count'],
            star_five=comment_summary['score5Count']
        )


# 保存型号统计数据
def insert_jd_model_summary(model_summary: dict, comment: dict, shop: Shop):
    productColor, productRam, productRom = parse_jd_mi10_product_info(comment)
    try:
        ms = ModelSummary.get(
            source=shop.source,
            is_official=shop.is_official,
            product_color=productColor,
            product_ram=productRam,
            product_rom=productRom,
        )
        update_jd_summary_data(ms, model_summary)
    except ModelSummary.DoesNotExist:
        ModelSummary.create(
            source=shop.source,
            is_official=shop.is_official,
            product_color=productColor,
            product_ram=productRam,
            product_rom=productRom,
            total=parse_jd_count_str(model_summary['commentCountStr']),
            good_rate=model_summary['goodRate'] * 100,
            default_good=parse_jd_count_str(model_summary['defaultGoodCountStr']),
            star_one=model_summary['score1Count'],
            star_two=model_summary['score2Count'],
            star_three=model_summary['score3Count'],
            star_four=model_summary['score4Count'],
            star_five=model_summary['score5Count']
        )


# 计算最终好评率
def calculate_jd_good_rate(summary_list):
    for summary in summary_list:
        good_count = summary.star_four + summary.star_five
        sum_count = summary.star_one + summary.star_two + summary.star_three + summary.star_four + summary.star_five
        final_good_rate = (good_count / sum_count) * 100
        summary.good_rate = format(final_good_rate, '.1f')
        summary.save()
        print('------最终好评率计算完成------')


if __name__ == '__main__':
    options = set_options()
    caps = set_capabilities()
    # 在Windows环境下已将chromedriver添加至环境变量, 无需声明执行文件路径
    # 在Arch Linux环境下, 使用archlinux cn源安装的chromedriver位置在/usr/bin, 也无需声明执行文件路径
    driver = Chrome(options=options, desired_capabilities=caps)
    # 从京东获得数据
    get_mi10_data_from_jd(driver)
    # 退出浏览器实例
    driver.quit()
