import re
import json
from time import sleep
from random import uniform
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, WebDriverException
from db.mi10_models import Shop, MiSku, Comment, CommentSummary
from spider.utils import (get_chrome_driver, get_response_body, get_response_body_list, window_scroll_by,
                          waiting_comments_loading)


# 获取小米商城的小米10销售数据
def get_mi10_data_from_mishop(browser: Chrome):
    for mishop in Shop.select().where(Shop.source == '小米商城'):
        print(f'------打开当前小米商城商品评论链接: {mishop.url}------')
        browser.get(mishop.url)
        current_page = 0
        max_page = 141
        while current_page <= max_page:
            try:
                if current_page == 0:
                    max_page = get_sku_info_and_summary_and_first_page_comments(browser)
                    current_page += 1
                else:
                    # 获取本页评论数据
                    mishop_comments = get_response_body(browser, 'user_comment/get_list', 'GET')
                    mishop_comments = mishop_comments.rstrip(');')
                    mishop_comments = re.sub(r'^\w+\(', '', mishop_comments)
                    mishop_comments = json.loads(mishop_comments)
                    # 保存本页评论数据
                    if mishop_comments['msg'] == 'success':
                        current_page = mishop_comments['data']['page_current']
                        insert_mishop_comments(mishop_comments['data']['comments'])
                    else:
                        print(f'---获取第{current_page + 1}页评论数据异常---')
                        break
            except WebDriverException:
                print(f'---获取第{current_page}页评论异常(WebDriverException), 尝试翻到下一页---')

            print(f'当前页数: {current_page}')
            turn_to_the_next_page(browser)

        print('------评论获取阶段结束------')
    print('------小米商城数据获取完成------')


# 同时获取SKU与对应的产品规格信息, 评论统计和第一页评论, 并返回总页数
def get_sku_info_and_summary_and_first_page_comments(browser: Chrome) -> int:
    # 捕获三个接口的数据
    sku_info = summary = comments = {}
    target_urls = [
        {'url': 'commodity_page', 'method': 'GET'},
        {'url': 'user_comment/get_summary', 'method': 'GET'},
        {'url': 'user_comment/get_list', 'method': 'GET'}
    ]
    all_data = get_response_body_list(browser, target_urls)
    for data in all_data:
        if data['url'] == 'commodity_page' and data['method'] == 'GET':
            sku_info = data['response_body']
            sku_info = sku_info.lstrip('__jp0(').rstrip(');')
            sku_info = json.loads(sku_info)
        if data['url'] == 'user_comment/get_summary' and data['method'] == 'GET':
            summary = data['response_body']
            summary = summary.lstrip('__jp6(').rstrip(');')
            summary = json.loads(summary)
        if data['url'] == 'user_comment/get_list' and data['method'] == 'GET':
            comments = data['response_body']
            comments = comments.lstrip('__jp5(').rstrip(');')
            comments = json.loads(comments)

    # 保存SKU与对应的产品规格信息
    if sku_info['msg'] == 'success':
        insert_mishop_sku_info(sku_info)
        print('------保存SKU信息成功------')
    else:
        print('---查询SKU信息失败---')

    # 保存评论统计数据
    if summary['msg'] == 'success':
        insert_mishop_comment_summary(summary)
        print('------保存评论统计数据成功------')
    else:
        print('---查询评论统计数据失败---')

    # 保存第一页评论数据
    if comments['msg'] == 'success':
        total_page = comments['data']['page_total']
        print(f'有 {total_page} 页评论, 共 {comments["data"]["total_count"]} 条')
        insert_mishop_comments(comments['data']['comments'])
        return total_page
    else:
        print('---获取第1页评论数据异常---')
        return 0


# 查找商品规格
def get_product_info(product_info_list: list, prop_value_id: int) -> str:
    for product_info in product_info_list:
        if product_info['prop_value_id'] == prop_value_id:
            return product_info['name']
    return 'Not Found'


# 保存SKU与对应的产品规格信息
def insert_mishop_sku_info(sku_info: dict):
    info_list = []
    sku_list = sku_info['data']['goods_info']
    for option in sku_info['data']['buy_option']:
        info_list.extend(option['list'])
    for sku in sku_list:
        color = get_product_info(info_list, sku['prop_list'][1]['prop_value_id'])
        ram_and_rom = get_product_info(info_list, sku['prop_list'][0]['prop_value_id']).split('+')
        ram = ram_and_rom[0]
        rom = ram_and_rom[1]
        try:
            MiSku.get(
                MiSku.sku == sku['goods_id'],
                MiSku.product_color == color,
                MiSku.product_ram == ram,
                MiSku.product_rom == rom
            )
            print(f'SKU: {sku["goods_id"]} 已存在')
        except MiSku.DoesNotExist:
            MiSku.create(
                source='小米商城',
                is_official=True,
                sku=sku['goods_id'],
                product_color=color,
                product_ram=ram,
                product_rom=rom
            )


# 保存评论统计数据
def insert_mishop_comment_summary(summary: dict):
    summary_detail = summary['data']['detail']
    CommentSummary.create(
        source='小米商城',
        is_official=True,
        total=summary_detail['comments_total'],
        good_rate=summary_detail['satisfy_per'],
        default_good=summary_detail['default_good'],
        star_one=summary_detail['one_star'],
        star_two=summary_detail['two_star'],
        star_three=summary_detail['three_star'],
        star_four=summary_detail['four_star'],
        star_five=summary_detail['five_star']
    )


# 保存评论
def insert_mishop_comments(comment_list: list):
    for comment in comment_list:
        try:
            existed_comment = Comment.get_by_id('MI' + comment['comment_id'])
            existed_comment.star = int(comment['total_grade'])
            existed_comment.save()
            print(f'评论ID为{comment["comment_id"]}的评论已存在, 已更新用户评分星级')
        except Comment.DoesNotExist:
            if comment['is_youpin'] == 0:
                proper_source = '小米商城'
            else:
                proper_source = '小米有品'
            try:
                mi_sku = MiSku.get_by_id(str(comment['goods_id']))
            except MiSku.DoesNotExist:
                print('---此条评论对应的SKU不存在---')
                continue
            Comment.create(
                source=proper_source,
                is_official=True,
                comment_id='MI' + comment['comment_id'],
                create_time=comment['add_time'],
                content=comment['comment_content'],
                star=int(comment['total_grade']),
                product_color=mi_sku.product_color,
                product_ram=mi_sku.product_ram,
                product_rom=mi_sku.product_rom
            )


# 评论页面翻页
def turn_to_the_next_page(browser: Chrome):
    while True:
        try:
            WebDriverWait(browser, 0.5).until(
                ec.element_to_be_clickable((By.CLASS_NAME, 'more'))
            )
            browser.execute_script('document.querySelector(".more").click()')
            waiting_comments_loading(browser, 'common')
            break
        except TimeoutException:
            window_scroll_by(browser, 500)


if __name__ == '__main__':
    # 创建一个chrome实例
    driver = get_chrome_driver()
    # 从小米商城获得数据
    get_mi10_data_from_mishop(driver)
    # 退出浏览器实例
    driver.quit()
