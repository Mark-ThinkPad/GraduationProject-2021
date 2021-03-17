import re
import json
from time import time, sleep
from selenium.webdriver import Chrome, ChromeOptions


# 设置requests请求头
def set_headers(**kwargs) -> dict:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
    }
    headers.update(kwargs)

    return headers


# 设置Chrome启动参数
def set_options() -> ChromeOptions:
    options = ChromeOptions()
    # 以最大化窗口启动
    options.add_argument('--start-maximized')
    # 设置开发者模式启动，该模式下webdriver属性为正常值
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # 设置W3C模式
    options.add_experimental_option('w3c', False)

    return options


# 设置selenium webdriver配置信息, 以便获取Network信息
def set_capabilities() -> dict:
    caps = {
        'browserName': 'chrome',
        'loggingPrefs': {
            'browser': 'ALL',
            'driver': 'ALL',
            'performance': 'ALL',
        },
        'google:chromeOptions': {
            'perfLoggingPrefs': {
                'enableNetwork': True,
            },
        },
    }

    return caps


# 创建一个chrome实例
def get_chrome_driver() -> Chrome:
    options = set_options()
    caps = set_capabilities()
    # 在Windows环境下已将chromedriver添加至环境变量, 无需声明执行文件路径
    # 在Arch Linux环境下, 使用archlinux cn源安装的chromedriver位置在/usr/bin, 也无需声明执行文件路径
    driver = Chrome(options=options, desired_capabilities=caps)
    return driver


# 从Chrome中获取单个指定接口的响应数据
def get_response_body(browser: Chrome, target_url: str, target_method: str):
    request_log = browser.get_log('performance')
    for i in range(len(request_log)):
        message = json.loads(request_log[i]['message'])
        message = message['message']['params']
        try:
            request = message['request']
        except KeyError:
            continue
        # print(request, type(request))
        current_url = request['url']
        current_method = request['method']
        if target_url in current_url and target_method == current_method:
            # 得到requestId
            requestId = message['requestId']
            # print(requestId)
            # 通过requestId获取接口内容
            response = browser.execute_cdp_cmd('Network.getResponseBody', {'requestId': requestId})
            return response['body']

    return None


# 从Chrome中获取多个指定接口的响应数据
def get_response_body_list(browser: Chrome, target_list: list) -> list:
    response_body_list = []
    request_log = browser.get_log('performance')
    for i in range(len(request_log)):
        message = json.loads(request_log[i]['message'])
        message = message['message']['params']
        try:
            request = message['request']
        except KeyError:
            continue
        # print(request, type(request))
        current_url = request['url']
        current_method = request['method']
        for target in target_list:
            if target['url'] in current_url and target['method'] == current_method:
                # 得到requestId
                requestId = message['requestId']
                # print(requestId)
                # 通过requestId获取接口内容
                response = browser.execute_cdp_cmd('Network.getResponseBody', {'requestId': requestId})
                response_body_list.append({
                    'response_body': response['body'],
                    'url': target['url'],
                    'method': target['method']
                })

    return response_body_list


# 网页在垂直方向滑动, distance为正之时向下滑动, 为负值时向上滑动
def window_scroll_by(browser: Chrome, distance: int):
    js = f'window.scrollBy({{top:{distance}, left:0, behavior: "smooth"}})'
    browser.execute_script(js)
    sleep(0.1)


# 获取13位时间戳
def get_timestamp_13bit() -> str:
    return str(round(time() * 1000))


# 将京东计数字符转为数字
def parse_jd_count_str(count_str: str) -> int:
    result = count_str.rstrip('+')
    if result.isdigit() is False:
        cn_number_unit = result[-1]
        if cn_number_unit == '万':
            prefix_number = result.replace(cn_number_unit, '')
            result = int(prefix_number) * 10000
    else:
        result = int(result)

    return result


# selenium打开第二个窗口
def open_second_window(browser: Chrome):
    browser.execute_script("window.open()")
    handles = browser.window_handles
    browser.switch_to.window(handles[1])


# selenium回到第一个窗口
def back_to_first_window(browser: Chrome):
    browser.close()
    handles = browser.window_handles
    browser.switch_to.window(handles[0])


# 解析小米10产品信息
def parse_mi10_product_info(product_color: str, storage: str) -> tuple:
    if '灰' in product_color:
        product_color = '国风雅灰'
    if '黑' in product_color:
        product_color = '钛银黑'
    if '蓝' in product_color:
        product_color = '冰海蓝'
    if '金' in product_color:
        product_color = '蜜桃金'
    product_ram_and_rom = re.search(r'\d+[GB]*\+\d+[GB]*', storage).group().split('+')
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


# 计算小米10数据最终好评率
def calculate_mi10_good_rate(summary_list):
    for summary in summary_list:
        good_count = summary.star_four + summary.star_five
        sum_count = summary.star_one + summary.star_two + summary.star_three + summary.star_four + summary.star_five
        final_good_rate = (good_count / sum_count) * 100
        summary.good_rate = format(final_good_rate, '.1f')
        summary.save()
    print('------最终好评率计算完成------')

