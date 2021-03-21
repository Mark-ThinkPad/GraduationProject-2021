from db.mi10_models import Shop

shops = [
    {'source': '京东', 'is_official': True, 'url': 'https://item.jd.com/100011336064.html'},
    {'source': '苏宁', 'is_official': True, 'url': 'https://product.suning.com/0000000000/11926557079.html'},
    {'source': '小米有品', 'is_official': True, 'url': 'https://www.xiaomiyoupin.com/detail?gid=118630&spmref=YouPinPC'},
    {'source': '小米商城', 'is_official': True, 'url': 'https://www.mi.com/comment/10000214.html'}
]

Shop.insert_many(shops).execute()
