from peewee import fn
from data_analyze.utils import calculate_percentage
from db.wireless_headphone_models import Commodity
from db.wireless_headphone_analyze_models import (WH, WHTotal, WHSelfPer, WHBrand, WHBrandSalesStar, WHPriceAndSales,
                                                  WHPriceAndBrand)


# 预处理原生数据
def preprocess_data():
    # 删除销量为0的无效数据
    # Commodity.delete().where(Commodity.total == 0).execute()

    # 统一品牌名
    # brand_list = ['HYUNDAI']
    # Commodity.update(brand='现代').where(Commodity.brand.in_(brand_list)).execute()
    # for commodity in Commodity.select().group_by(Commodity.brand):
    #     print(commodity.brand)

    # 规范产品名
    target_brand = 'B&O'
    name_list = ['']
    Commodity.update(model='').where((Commodity.model.in_(name_list)) & (Commodity.brand == target_brand)) \
        .execute()
    for commodity in Commodity.select().where(Commodity.brand == target_brand).group_by(Commodity.model):
        print(commodity.model)


# 生成数据总览
def get_wh_total():
    total_count = Commodity.select(fn.SUM(Commodity.total).alias('tc')).dicts()[0]['tc']
    commodity_count = Commodity.select().count()
    brand_count = Commodity.select().group_by(Commodity.brand).count()
    model_count = Commodity.select().group_by(Commodity.model).count()

    WHTotal.create(
        total_count=total_count,
        commodity_count=commodity_count,
        brand_count=brand_count,
        model_count=model_count
    )
    # for com in Commodity.select().group_by(Commodity.source):
    #     print(com.source)


# 生成自营与非自营销量比例
def get_wh_self_per():
    total_count = Commodity.select(fn.SUM(Commodity.total).alias('tc')).dicts()[0]['tc']
    self_count = Commodity.select(fn.SUM(Commodity.total).alias('tc')).where(Commodity.is_self == True).dicts()[0]['tc']
    non_self_count = Commodity.select(fn.SUM(Commodity.total).alias('tc')).where(Commodity.is_self == False).dicts()[0][
        'tc']

    WHSelfPer.create(
        total_count=total_count,
        self_count=self_count,
        self_percentage=calculate_percentage(total_count, self_count),
        non_self_count=non_self_count,
        non_self_percentage=calculate_percentage(total_count, non_self_count)
    )


# 生成型号与销量
def get_wh():
    for commodity in Commodity.select():
        try:
            wh = WH.get(
                WH.brand == commodity.brand,
                WH.model == commodity.model
            )
            wh.total += commodity.total
            wh.save()
        except WH.DoesNotExist:
            WH.create(
                brand=commodity.brand,
                model=commodity.model,
                total=commodity.total
            )


# 生成品牌销量占比
def get_wh_brand():
    # for commodity in Commodity.select():
    #     try:
    #         wh_brand = WHBrand.get(WHBrand.brand == commodity.brand)
    #         wh_brand.total += commodity.total
    #         wh_brand.save()
    #     except WHBrand.DoesNotExist:
    #         WHBrand.create(
    #             brand=commodity.brand,
    #             total=commodity.total
    #         )
    total_count = WHBrand.select(fn.SUM(WHBrand.total).alias('tc')).dicts()[0]['tc']
    print(total_count)
    for wh_brand in WHBrand.select():
        wh_brand.percentage = calculate_percentage(total_count, wh_brand.total)
        wh_brand.save()
        # if float(wh_brand.percentage) < 0.9:
        #     others = WHBrand.get_by_id('其他品牌')
        #     others.total += wh_brand.total
        #     others.save()
        #     wh_brand.delete_instance()


# 生成无线耳机在不同价格区间与销量分布
def get_wh_price_and_sales():
    for commodity in Commodity.select():
        if 0 < commodity.price < 100:
            whpas = WHPriceAndSales.get_by_id('0-100元')
            whpas.total += commodity.total
            whpas.save()
        if 100 <= commodity.price < 200:
            whpas = WHPriceAndSales.get_by_id('100-200元')
            whpas.total += commodity.total
            whpas.save()
        if 200 <= commodity.price < 500:
            whpas = WHPriceAndSales.get_by_id('200-500元')
            whpas.total += commodity.total
            whpas.save()
        if 500 <= commodity.price < 900:
            whpas = WHPriceAndSales.get_by_id('500-900元')
            whpas.total += commodity.total
            whpas.save()
        if 900 <= commodity.price < 2000:
            whpas = WHPriceAndSales.get_by_id('900-2000元')
            whpas.total += commodity.total
            whpas.save()
        if commodity.price >= 2000:
            whpas = WHPriceAndSales.get_by_id('2000元以上')
            whpas.total += commodity.total
            whpas.save()

    total_count = WHPriceAndSales.select(fn.SUM(WHPriceAndSales.total).alias('tc')).dicts()[0]['tc']
    print(total_count)
    for whpas in WHPriceAndSales.select():
        whpas.percentage = calculate_percentage(total_count, whpas.total)
        whpas.save()


# 生成无线耳机在不同价格区间的品牌销量占比
def get_wh_price_and_brand():
    # for commodity in Commodity.select():
    #     if 0 < commodity.price < 200:
    #         try:
    #             wh_pab = WHPriceAndBrand.get(
    #                 WHPriceAndBrand.price_range == '200元以下',
    #                 WHPriceAndBrand.brand == commodity.brand
    #             )
    #             wh_pab.total += commodity.total
    #             wh_pab.save()
    #         except WHPriceAndBrand.DoesNotExist:
    #             WHPriceAndBrand.create(
    #                 price_range='200元以下',
    #                 brand=commodity.brand,
    #                 total=commodity.total
    #             )
    #     if 200 <= commodity.price < 900:
    #         try:
    #             wh_pab = WHPriceAndBrand.get(
    #                 WHPriceAndBrand.price_range == '200-900元',
    #                 WHPriceAndBrand.brand == commodity.brand
    #             )
    #             wh_pab.total += commodity.total
    #             wh_pab.save()
    #         except WHPriceAndBrand.DoesNotExist:
    #             WHPriceAndBrand.create(
    #                 price_range='200-900元',
    #                 brand=commodity.brand,
    #                 total=commodity.total
    #             )
    #     if commodity.price >= 900:
    #         try:
    #             wh_pab = WHPriceAndBrand.get(
    #                 WHPriceAndBrand.price_range == '900元以上',
    #                 WHPriceAndBrand.brand == commodity.brand
    #             )
    #             wh_pab.total += commodity.total
    #             wh_pab.save()
    #         except WHPriceAndBrand.DoesNotExist:
    #             WHPriceAndBrand.create(
    #                 price_range='900元以上',
    #                 brand=commodity.brand,
    #                 total=commodity.total
    #             )

    range_list = ['200元以下', '200-900元', '900元以上']
    for pr in range_list:
        total_count = WHPriceAndBrand.select(fn.SUM(WHPriceAndBrand.total).alias('tc')) \
            .where(WHPriceAndBrand.price_range == pr).dicts()[0]['tc']
        print(total_count)
        for wh_pab in WHPriceAndBrand.select().where(WHPriceAndBrand.price_range == pr):
            wh_pab.percentage = calculate_percentage(total_count, wh_pab.total)
            wh_pab.save()
            # if float(wh_pab.percentage) < 1:
            #     others = WHPriceAndBrand.get(
            #         WHPriceAndBrand.price_range == pr,
            #         WHPriceAndBrand.brand == '其他品牌'
            #     )
            #     others.total += wh_pab.total
            #     others.save()
            #     wh_pab.delete_instance()


# 生成品牌内部销量明星
def get_wh_brand_sales_star():
    brand_list = ['苹果', '漫步者', 'ENKOR', '小米', '华为', '索尼', 'Bose']
    for brand in brand_list:
        for wh in WH.select().where(WH.brand == brand):
            WHBrandSalesStar.create(
                brand=brand,
                model=wh.model,
                total=wh.total
            )


if __name__ == '__main__':
    # preprocess_data()
    # get_wh_total()
    # get_wh_self_per()
    # get_wh()
    # get_wh_brand()
    # get_wh_price_and_sales()
    # get_wh_price_and_brand()
    get_wh_brand_sales_star()
