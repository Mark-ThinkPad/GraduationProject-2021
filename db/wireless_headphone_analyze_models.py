import peewee as pw
from conf.settings import DATABASE_DIR

wireless_headphone_analyze_db = pw.SqliteDatabase(DATABASE_DIR + '/wireless_headphone_analyze.db',
                                                  pragmas=(('foreign_keys', 1),))


class BaseModel(pw.Model):
    class Meta:
        database = wireless_headphone_analyze_db


# 数据总览
class WHTotal(BaseModel):
    total_count = pw.IntegerField()  # 总销量
    commodity_count = pw.IntegerField()  # 商品数量
    brand_count = pw.IntegerField()  # 品牌数
    model_count = pw.IntegerField()  # 机型数


# 自营与非自营销量比例
class WHSelfPer(BaseModel):
    total_count = pw.IntegerField()  # 总销量
    self_count = pw.IntegerField()  # 自营销量
    self_percentage = pw.CharField(max_length=4)  # 自营销量占比
    non_self_count = pw.IntegerField()  # 非自营销量
    non_self_percentage = pw.CharField(max_length=4)  # 非自营销量占比


# 型号和销量 (WH为 Wireless Headphone 的缩写)
class WH(BaseModel):
    brand = pw.CharField(max_length=40)  # 品牌
    model = pw.CharField(max_length=200)  # 产品型号
    total = pw.IntegerField()  # 销量/评价总数
    ref_price = pw.FloatField(null=True)  # 参考价格

    class Meta:
        primary_key = pw.CompositeKey('brand', 'model')


# 品牌销量占比
class WHBrand(BaseModel):
    brand = pw.CharField(max_length=40, primary_key=True)  # 品牌
    total = pw.IntegerField()
    percentage = pw.CharField(max_length=4, null=True)


# 无线耳机在不同价格区间与销量分布
class WHPriceAndSales(BaseModel):
    price_range = pw.CharField(max_length=20, primary_key=True)
    total = pw.IntegerField()
    percentage = pw.CharField(max_length=4, null=True)


# 无线耳机在不同价格区间的品牌销量占比
class WHPriceAndBrand(BaseModel):
    price_range = pw.CharField(max_length=20)
    brand = pw.CharField(max_length=40)
    total = pw.IntegerField()
    percentage = pw.CharField(max_length=4, null=True)

    class Meta:
        primary_key = pw.CompositeKey('price_range', 'brand')


# 品牌内部销量明星
class WHBrandSalesStar(BaseModel):
    brand = pw.CharField(max_length=40)
    model = pw.CharField(max_length=200)
    total = pw.IntegerField()

    class Meta:
        primary_key = pw.CompositeKey('brand', 'model')


if __name__ == '__main__':
    wireless_headphone_analyze_db.create_tables([WH, WHTotal, WHSelfPer, WHBrand, WHBrandSalesStar, WHPriceAndSales,
                                                 WHPriceAndBrand])
