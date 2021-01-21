import json
from time import time
from selenium.webdriver import Chrome, ChromeOptions
from selenium.common.exceptions import WebDriverException


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


# 从Chrome中获取指定接口的响应数据
def get_response_body(browser: Chrome, target_url: str):
    request_log = browser.get_log('performance')
    response_body = 'Not Found'
    for i in range(len(request_log)):
        message = json.loads(request_log[i]['message'])
        message = message['message']['params']
        # .get() 方式获取是了避免字段不存在时报错
        request = message.get('request')
        if request is None:
            continue

        url = request.get('url')
        if target_url in url:
            # 得到requestId
            requestId = message['requestId']
            # print(requestId)
            # 通过requestId获取接口内容
            try:
                response = browser.execute_cdp_cmd('Network.getResponseBody', {'requestId': requestId})
                response_body = response['body']
            except WebDriverException:
                continue

    return response_body


# 获取13位时间戳
def get_timestamp_13bit() -> str:
    return str(round(time() * 1000))
