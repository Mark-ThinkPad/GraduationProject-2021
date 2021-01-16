import json
from time import sleep
from selenium.webdriver import Chrome
from spider.utils import set_options, set_capabilities


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
    request_log = browser.get_log('performance')
    for i in range(len(request_log)):
        message = json.loads(request_log[i]['message'])
        message = message['message']['params']
        # .get() 方式获取是了避免字段不存在时报错
        request = message.get('request')
        if request is None:
            continue

        url = request.get('url')
        page_comment_url = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98' \
                           '&productId=100014565800&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'
        if url == page_comment_url:
            # 得到requestId
            requestId = message['requestId']
            # print(requestId)
            # 通过requestId获取接口内容
            content = browser.execute_cdp_cmd('Network.getResponseBody', {'requestId': requestId})
            comments = content['body'].lstrip('fetchJSON_comment98(').rstrip(');)')
            # print(comments)
            with open('jd_comments.json', 'w', encoding='UTF-8') as file:
                file.write(comments)
            break


if __name__ == '__main__':
    options = set_options()
    caps = set_capabilities()
    # 在Windows环境下已将chromedriver添加至环境变量
    driver = Chrome(options=options, desired_capabilities=caps)
    get_jd_comments(driver)
    driver.quit()
