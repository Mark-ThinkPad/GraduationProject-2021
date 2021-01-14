import json
import requests

url = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98' \
      '&productId=100009958343&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/87.0.4280.141 Safari/537.36',
    'Accept': '*/*',
    'Referer': 'https://item.jd.com/100009958343.html'
}

res = requests.get(url, headers)
data = res.text
# jd = json.loads(data.lstrip('fetchJSON_comment98vv12345(').rstrip(');'))
print(data)
