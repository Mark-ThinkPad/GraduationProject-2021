import peewee as pw
from conf.settings import DATABASE_DIR

phone_sales_analyze_db = pw.SqliteDatabase(DATABASE_DIR + '/phone_sales_analyze.db', pragmas=(('foreign_keys', 1),))


class BaseModel(pw.Model):
    class Meta:
        database = phone_sales_analyze_db


# 机型销量
class Phone(BaseModel):
    brand = pw.CharField(max_length=40)  # 品牌
    model = pw.CharField(max_length=200)  # 产品型号
    total = pw.IntegerField()  # 销量/评价总数
    ref_price = pw.FloatField(null=True)  # 参考价格

    class Meta:
        primary_key = pw.CompositeKey('brand', 'model')


# 数据总览
class PhoneTotal(BaseModel):
    total_count = pw.IntegerField()  # 总销量
    commodity_count = pw.IntegerField()  # 商品数量
    brand_count = pw.IntegerField()  # 品牌数
    model_count = pw.IntegerField()  # 机型数


# 平台数据源概览
class PhonePlatform(BaseModel):
    source = pw.CharField(max_length=4, primary_key=True)  # 数据源平台
    total_count = pw.IntegerField()  # 总销量
    commodity_count = pw.IntegerField()  # 商品数量
    self_percentage = pw.CharField(max_length=4)  # 自营销量占比
    non_self_percentage = pw.CharField(max_length=4)  # 非自营销量占比


# 操作系统比例
class PhoneOS(BaseModel):
    os = pw.CharField(max_length=10, primary_key=True)
    total = pw.IntegerField()
    percentage = pw.CharField(max_length=4, null=True)


# 品牌销量占比
class PhoneBrand(BaseModel):
    brand = pw.CharField(max_length=20, primary_key=True)  # 品牌
    total = pw.IntegerField()
    percentage = pw.CharField(max_length=4, null=True)


# 品牌内部销量明星
class BrandSalesStar(BaseModel):
    brand = pw.CharField(max_length=20)
    model = pw.CharField(max_length=40)
    total = pw.IntegerField()

    class Meta:
        primary_key = pw.CompositeKey('brand', 'model')


# 主品牌与子品牌销量占比
class BrandPercentage(BaseModel):
    main_brand = pw.CharField(max_length=20)  # 主品牌
    sub_brand = pw.CharField(max_length=20)  # 子品牌
    total = pw.IntegerField()
    percentage = pw.CharField(max_length=4, null=True)

    class Meta:
        primary_key = pw.CompositeKey('main_brand', 'sub_brand')


# 功能机品牌占比
class FeaturePhonePercentage(BaseModel):
    brand = pw.CharField(max_length=20, primary_key=True)
    total = pw.IntegerField()
    percentage = pw.CharField(max_length=4, null=True)


# SoC销量
class SoC(BaseModel):
    soc_mfrs = pw.CharField(max_length=10)  # SoC制造商, mfrs为manufacturer的缩写
    soc_model = pw.CharField(max_length=20)  # SoC型号
    total = pw.IntegerField()  # 销量

    class Meta:
        primary_key = pw.CompositeKey('soc_mfrs', 'soc_model')


# SoC制造商占比
class SoCMfrs(BaseModel):
    soc_mfrs = pw.CharField(max_length=10, primary_key=True)  # SoC制造商, mfrs为manufacturer的缩写
    total = pw.IntegerField()
    percentage = pw.CharField(max_length=4, null=True)


# SoC制造商内部销量明星
class SoCStar(BaseModel):
    soc_mfrs = pw.CharField(max_length=10)  # SoC制造商, mfrs为manufacturer的缩写
    soc_model = pw.CharField(max_length=20)  # SoC型号
    total = pw.IntegerField()

    class Meta:
        primary_key = pw.CompositeKey('soc_mfrs', 'soc_model')


# 功能机SoC制造商占比
class FeaturePhoneSoCPer(BaseModel):
    soc_mfrs = pw.CharField(max_length=10, primary_key=True)
    total = pw.IntegerField()
    percentage = pw.CharField(max_length=4, null=True)


# 智能手机各项尺寸参数的平均数和中位数
class PhoneSize(BaseModel):
    screen_size_avg = pw.CharField(max_length=6)  # 屏幕尺寸平均数
    screen_size_med = pw.CharField(max_length=6)  # 屏幕尺寸中位数
    width_avg = pw.CharField(max_length=6)
    width_med = pw.CharField(max_length=6)
    thickness_avg = pw.CharField(max_length=6)
    thickness_med = pw.CharField(max_length=6)
    length_avg = pw.CharField(max_length=6)
    length_med = pw.CharField(max_length=6)
    weight_avg = pw.CharField(max_length=6)
    weight_med = pw.CharField(max_length=6)


# 智能手机与功能机价格区间与销量分布
class PhonePriceAndSales(BaseModel):
    type = pw.CharField(max_length=4)
    price_range = pw.CharField(max_length=20)
    total = pw.IntegerField()
    percentage = pw.CharField(max_length=4, null=True)


# 智能手机在不同价格区间的品牌销量占比
class PhonePriceAndBrand(BaseModel):
    price_range = pw.CharField(max_length=20)
    brand = pw.CharField(max_length=20)
    total = pw.IntegerField()
    percentage = pw.CharField(max_length=4, null=True)

    class Meta:
        primary_key = pw.CompositeKey('price_range', 'brand')


if __name__ == '__main__':
    phone_sales_analyze_db.create_tables([Phone, PhoneTotal, PhonePlatform, PhoneOS, PhoneBrand, BrandSalesStar,
                                          BrandPercentage, FeaturePhonePercentage, SoC, SoCMfrs, SoCStar,
                                          FeaturePhoneSoCPer, PhoneSize, PhonePriceAndSales, PhonePriceAndBrand])
