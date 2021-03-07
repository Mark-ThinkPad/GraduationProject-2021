from time import sleep
from selenium.webdriver import Chrome
from selenium.webdriver.common.action_chains import ActionChains
from spider.utils import set_options, set_capabilities, get_response_body


# 获取京东评论api数据
def get_jd_comments(browser: Chrome):
    # 小米10ultra 京东自营旗舰店
    browser.get('https://item.jd.com/100014565800.html')
    # 模拟滚动条的js脚本
    js = 'window.scrollBy({top:1000, left:0, behavior: "smooth"})'
    # 执行js脚本
    browser.execute_script(js)
    sleep(1)
    # 选择商品评论标签并点击
    browser.find_element_by_xpath('/html/body/div[10]/div[2]/div[1]/div[1]/ul/li[5]').click()
    sleep(1)
    # 获取京东评论接口数据并保存到本地json文件
    page_comment_url = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98' \
                       '&productId=100014565800&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'
    comments = get_response_body(browser, page_comment_url, 'GET')
    comments = comments.lstrip('fetchJSON_comment98(').rstrip(');')
    # print(comments)
    with open('jd_comments.json', 'w', encoding='UTF-8') as file:
        file.write(comments)


# 评论切换到时间排序
def get_jd_comments_switch(browser: Chrome):
    # 小米10ultra 京东自营旗舰店
    browser.get('https://item.jd.com/100014565800.html')
    # 打开评论
    js = 'window.scrollBy({top:1000, left:0, behavior: "smooth"})'
    browser.execute_script(js)
    sleep(1)
    browser.find_element_by_xpath('/html/body/div[10]/div[2]/div[1]/div[1]/ul/li[5]').click()
    sleep(1)
    # 切换到时间排序
    current_sort = browser.find_element_by_xpath('/html/body/div[10]/div[2]/div[3]/div[2]/div[2]/div[1]/div/div/div[1]')
    time_sort = browser.find_element_by_xpath('/html/body/div[10]/div[2]/div[3]/div[2]/div[2]/div[1]/div/div/div[2]/ul/li[2]')
    ActionChains(browser).move_to_element(current_sort).click(time_sort).perform()
    sleep(10)


if __name__ == '__main__':
    options = set_options()
    caps = set_capabilities()
    # 在Windows环境下已将chromedriver添加至环境变量, 无需声明执行文件路径
    # 在Arch Linux环境下, 使用archlinux cn源安装的chromedriver位置在/usr/bin, 也无需声明执行文件路径
    driver = Chrome(options=options, desired_capabilities=caps)
    # get_jd_comments(driver)
    get_jd_comments_switch(driver)
    driver.quit()
