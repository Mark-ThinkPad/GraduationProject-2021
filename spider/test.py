import re
import json
from random import uniform
# from db.mi10_models import Shop
from spider.utils import parse_timestamp_13bit
from db.wireless_headphone_models import Commodity
# from db.airpods_models import Shop
from db.iPhone11_models import Shop

# shop = Shop()
# shop.source = '京东'
# shop.is_official = True
# shop.url = 'https://item.jd.com/100011336064.html'
# shop.save()

# shop = Shop()
# shop.source = '苏宁'
# shop.is_official = True
# shop.url = 'https://product.suning.com/0000000000/11926557079.html'
# shop.save()

# shop = Shop()
# shop.source = '小米有品'
# shop.is_official = True
# shop.url = 'https://www.xiaomiyoupin.com/detail?gid=118630&spmref=YouPinPC'
# shop.save()

# shop = Shop()
# shop.source = '小米商城'
# shop.is_official = True
# shop.url = 'https://www.mi.com/comment/10000214.html'
# shop.save()

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

# print(uniform(3, 6))

# str1 = '全网通 8G+128G 【官方标配】'
# str2 = '12G+256G 【官方标配】'
# str3 = '全网通 8GB+128GB'
# str4 = '全网通8GB+128GB（12期免息）'
# str5 = '12+256【6期免息】'
# str6 = '8G+256G 【扫地机器人+耳机蓝牙】套装'
# str7 = '12GB+256GB'
# result = re.search(r'\d+[GB]*\+\d+[GB]*', str7).group()
# print(result)
# ram_and_rom = result.split('+')
# print(ram_and_rom)
# ram = ram_and_rom[0]
# rom = ram_and_rom[1]
# if 'G' not in ram:
#     ram += 'GB'
# elif 'B' not in ram:
#     ram += 'B'
# if 'G' not in rom:
#     rom += 'GB'
# elif 'B' not in rom:
#     rom += 'B'
# print(ram, rom)

# sku1 = '000000000945112108'
# sku2 = '000000011592114089'
# result1 = re.match(r'^[0]+', sku1).group()
# result2 = re.match(r'^[0]+', sku2).group()
# sku1 = sku1.replace(result1, '')
# sku2 = sku2.replace(result2, '')
# print(sku1, sku2)

# str1 = '30天后追加'
# result = int(re.match(r'^\d+', str1).group())
# print(result, type(result))

# str1 = '12+256（G）'
# str2 = '(5G版本）8GB+128GB'
# result = re.search(r'\d+[GB]*\+\d+[GB]*', str1).group()
# print(result)

# print(parse_timestamp_13bit(1616141975952))

# str1 = '18.7'
# str2 = '22'
# str3 = '其他英寸'
# print(float(str2))

# print(int('0070067921'))

# Commodity.create(
#     source='荣耀商城',
#     url='https://www.hihonor.com/cn/shop/product/10086341564703.html',
#     title='荣耀 FlyPods 3真无线耳机（铃兰白）',
#     shop_name='荣耀商城',
#     is_self=True,
#     price=499,
#     total=70,
#     brand='荣耀',
#     model='荣耀 FlyPods 3'
# )

# Shop.create(
#     source='京东',
#     is_official=True,
#     url='https://item.jd.com/100004325476.html'
# )
#
# self = 'https://item.jd.com/100004325476.html'
# one = 'https://item.jd.com/24497394828.html'
# two = 'https://item.jd.com/69094314974.html'
# three = 'https://item.jd.com/43835722030.html'

# Shop.create(
#     source='苏宁',
#     is_self=False,
#     url='https://product.suning.com/0070517287/12183012070.html'
# )

str1 = '全网通128GB（新包装）'
str2 = '全网通64GB（新包装）'
str3 = '（24期分期0首付新包装）全网通128G'
str4 = '品胜PD20W 128GB+快充Type-c快充充电器套装'
result = re.search(r'\d+[GB]+', str4).group()
print(result)
