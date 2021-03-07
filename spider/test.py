from db.mi10_models import Shop

shop = Shop()
shop.source = '京东'
shop.is_official = True
shop.url = 'https://item.jd.com/100011336064.html'
shop.save()
