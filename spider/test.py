import re
from db.mi10_models import Shop

# shop = Shop()
# shop.source = '京东'
# shop.is_official = True
# shop.url = 'https://item.jd.com/100011336064.html'
# shop.save()

# str_one = '8GB+256GB'
# str_two = '12GB+256GB'
#
# result = re.search(r'\+\w+?$', str_two)
# print(result.group().replace('+', ''))

distance = 100
s = f'window.scrollBy({{top:{distance}, left:0, behavior: "smooth"}})'
print(s)
