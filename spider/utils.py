from selenium.webdriver import ChromeOptions


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
