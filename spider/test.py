import re
from db.mi10_models import Shop

shop = Shop()
shop.source = '京东'
shop.is_official = True
shop.url = 'https://item.jd.com/100011336064.html'
shop.save()

# str_one = '8GB+256GB'
# str_two = '12GB+256GB'
#
# result = re.search(r'\+\w+?$', str_two)
# print(result.group().replace('+', ''))

# distance = 100
# s = f'window.scrollBy({{top:{distance}, left:0, behavior: "smooth"}})'
# print(s)

# str1 = '70万+'
# result = str1.rstrip('+')
# if result.isdigit() is False:
#     cn_number_unit = result[-1]
#     if cn_number_unit == '万':
#         prefix_number = result.replace(cn_number_unit, '')
#         result = int(prefix_number) * 10000
# else:
#     result = int(result)
#
# print(result, type(result))

# star1 = 8101
# star2 = 2088
# star3 = 4434
# star4 = 5558
# star5 = 179218
# good_count = star4 + star5
# sum_count = sum([star1, star2, star3, star4, star5])
# final_good_rate = (good_count / sum_count) * 100
# result = format(final_good_rate, '.1f')
# print(result, type(result))
