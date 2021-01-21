from time import sleep
from selenium.webdriver import Chrome
from spider.utils import set_options, set_capabilities, get_response_body


# 获取评论统计信息
def get_comment_score(browser: Chrome):
    # 华为 Mate 30 Pro 5G 华为商城
    browser.get('https://www.vmall.com/product/10086775311605.html')
    # 获取评论统计信息并保存到本地json文件
    comment_score_url = 'https://openapi.vmall.com/rms/comment/getCommentScore.json'
    comment_score = get_response_body(browser, comment_score_url)
    # print(comment_score)
    with open('hwsc_comment_score.json', 'w', encoding='UTF-8') as file:
        file.write(comment_score)


# 获取评论详情
def get_comment_list(browser: Chrome):
    # 华为 Mate 30 Pro 5G 华为商城
    browser.get('https://www.vmall.com/product/10086775311605.html')
    # 刷新页面
    # browser.refresh()
    # # 模拟页面滚动
    # js = 'window.scrollBy({top:1000, left:0, behavior: "smooth"})'
    # browser.execute_script(js)
    # sleep(1)
    # # 选择商品评论标签并点击
    # browser.find_element_by_xpath('//*[@id="pro-tab-evaluate"]').click()
    # sleep(1)
    # 获取评论详情并保存到本地json文件
    comment_list_url = 'https://openapi.vmall.com/rms/comment/getCommentList.json'
    comment_list = get_response_body(browser, comment_list_url)
    # print(comment_list)
    with open('hwsc_comment_list.json', 'w', encoding='UTF-8') as file:
        file.write(comment_list)


if __name__ == '__main__':
    options = set_options()
    caps = set_capabilities()
    # 在Windows环境下已将chromedriver添加至环境变量, 无需声明执行文件路径
    # 在Arch Linux环境下, 使用archlinux cn源安装的chromedriver位置在/usr/bin, 也无需声明执行文件路径
    driver = Chrome(options=options, desired_capabilities=caps)
    # get_comment_score(driver)
    get_comment_list(driver)
    driver.quit()
