import json
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, WebDriverException
from db.mi10_models import Shop, MiSku, Comment, CommentSummary
from spider.utils import (get_chrome_driver, get_response_body, get_response_body_list, window_scroll_by,
                          waiting_comments_loading, parse_timestamp_13bit)


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
    print('------小米有品数据获取完成------')


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
        print('---获取商品SKU和规格信息失败---')


# 打开默认评论页面
def switch_to_youpin_default_comments_page(browser: Chrome):
    window_scroll_by(browser, 800)
    browser.execute_script('document.querySelector("li.info-nav-item:nth-child(2)").click()')
    waiting_comments_loading(browser, 'commentItem')


# 获取小米有品的评论数据
def get_youpin_comments(browser: Chrome, shop: Shop):
    page = 1
    max_page = 141
    while page <= max_page:
        try:
            # 获取当前页面的评论
            if page == 1:
                # 获取第一页评论和评论统计数据
                comment_index = {}
                comment_content = {}
                target_urls = [
                    {'url': 'comment/product/index', 'method': 'POST'},
                    {'url': 'comment/product/content', 'method': 'POST'}
                ]
                all_data = get_response_body_list(browser, target_urls)
                for data in all_data:
                    if data['url'] == 'comment/product/index' and data['method'] == 'POST':
                        comment_index = data['response_body']
                        comment_index = json.loads(comment_index)
                    if data['url'] == 'comment/product/content' and data['method'] == 'POST':
                        comment_content = data['response_body']
                        comment_content = json.loads(comment_content)
                        max_page = (comment_content['data']['page']['total'] + 9) // 10
                        print(f'---评论总页数: {max_page} 页')
                # 保存评论统计数量
                if comment_index['message'] == 'ok':
                    summary = comment_index['data']
                    CommentSummary.create(
                        source=shop.source,
                        is_official=shop.is_official,
                        total=summary['total_count'],
                        good_rate=summary['positive_rate']
                    )
                    print('------保存评论统计数量成功------')
                else:
                    print('---查询评论统计数量失败---')
            else:
                content_url = 'comment/product/content'
                comment_content = get_response_body(browser, content_url, 'POST')
                if comment_content is None:
                    print('---未找到评论接口数据---')
                    break
                comment_content = json.loads(comment_content)

            # 保存评论
            if comment_content['message'] == 'ok':
                comment_list = comment_content['data']['list']
                insert_youpin_comments(comment_list, shop)
            else:
                print(f'---获取第{page}页评论数据异常---')
                break
        except WebDriverException:
            print(f'---获取第{page}页评论数据异常(WebDriverException), 尝试翻到下一页---')

        print(f'当前页数: {page}')
        # 下滑点击下一页
        turn_to_the_next_page(browser)
        page += 1

    print('------评论获取阶段结束------')


# 评论页面翻页
def turn_to_the_next_page(browser: Chrome):
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


# 保存小米有品评论
def insert_youpin_comments(comment_list: list, shop: Shop):
    for comment in comment_list:
        if comment['comment_source'] == 'mishop':
            proper_source = '小米商城'
        else:
            proper_source = '小米有品'
        try:
            mi_sku = MiSku.get_by_id(str(comment['pid']))
        except MiSku.DoesNotExist:
            print('---此条评论对应的SKU不存在---')
            continue
        Comment.get_or_create(
            source=proper_source,
            is_official=shop.is_official,
            comment_id='MI' + str(comment['comment_id']),
            create_time=parse_timestamp_13bit(comment['ctime']),
            content=comment['text'],
            star=0,  # comment['score']
            product_color=mi_sku.product_color,
            product_ram=mi_sku.product_ram,
            product_rom=mi_sku.product_rom
        )


if __name__ == '__main__':
    # 创建一个chrome实例
    driver = get_chrome_driver()
    # 从小米有品获得数据
    get_mi10_data_from_youpin(driver)
    # 退出浏览器实例
    driver.quit()
