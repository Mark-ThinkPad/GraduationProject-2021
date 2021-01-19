from time import sleep
from selenium.webdriver import Chrome
from spider.utils import set_options, set_capabilities, get_response_body


# 获取所有规格的商品信息
def get_detail(browser: Chrome):
    # 小米10ultra 小米自营
    browser.get('https://www.xiaomiyoupin.com/detail?gid=134230&spmref=YouPinPC.$SearchFilter$1.search_list.1.4643522')
    sleep(1)
    # 获取小米有品商品信息并保存到本地json文件
    detail_url = 'https://www.xiaomiyoupin.com/api/gateway/detail'
    detail = get_response_body(browser, detail_url)
    # print(detail)
    with open('xmyp_detail.json', 'w', encoding='UTF-8') as file:
        file.write(detail)


# 获取评论统计信息
def get_index(browser: Chrome):
    # 小米10ultra 小米自营
    browser.get('https://www.xiaomiyoupin.com/detail?gid=134230&spmref=YouPinPC.$SearchFilter$1.search_list.1.4643522')
    # 模拟滚动条的js脚本
    js = 'window.scrollBy({top:800, left:0, behavior: "smooth"})'
    # 执行js脚本
    browser.execute_script(js)
    sleep(10)


if __name__ == '__main__':
    options = set_options()
    caps = set_capabilities()
    # 在Windows环境下已将chromedriver添加至环境变量, 无需声明执行文件路径
    # 在Arch Linux环境下, 使用archlinux cn源安装的chromedriver位置在/usr/bin, 也无需声明执行文件路径
    driver = Chrome(options=options, desired_capabilities=caps)
    # get_detail(driver)
    get_index(driver)
    driver.quit()
