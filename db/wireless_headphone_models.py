import peewee as pw
from conf.settings import DATABASE_DIR

wireless_headphone_db = pw.SqliteDatabase(DATABASE_DIR + '/wireless_headphone.db', pragmas=(('foreign_keys', 1),))


class BaseModel(pw.Model):
    class Meta:
        database = wireless_headphone_db


# 商品模型
class Commodity(BaseModel):
    source = pw.CharField(max_length=4)  # 数据源平台
    url = pw.TextField(unique=True)  # 商品链接
    title = pw.CharField(max_length=200)  # 商品标题
    shop_name = pw.CharField(max_length=60)  # 店铺名称
    is_self = pw.BooleanField()  # 是否为官方自营店铺
    price = pw.FloatField()  # 价格
    total = pw.IntegerField()  # 销量/评价总数
    brand = pw.CharField(max_length=40)  # 品牌
    model = pw.CharField(max_length=200)  # 产品型号


# 京东平台所有将要获取的商品SKU编号
class JDTargetSku(BaseModel):
    sku = pw.CharField(max_length=20, primary_key=True)  # 商品SKU编号


# 京东平台已存在的SKU, 避免销量重复计数
class JDExistedSku(BaseModel):
    sku = pw.CharField(max_length=20, primary_key=True)  # 商品SKU编号


# 苏宁平台所有将要获取的商品SKU编号
class SNTargetSku(BaseModel):
    shop_code = pw.CharField(max_length=10)  # 苏宁商品URL中含有店铺代码, 需保存
    sku = pw.CharField(max_length=20)  # 商品SKU编号

    class Meta:
        primary_key = pw.CompositeKey('shop_code', 'sku')


# 苏宁平台已存在的SKU, 避免销量重复计数
class SNExistedSku(BaseModel):
    shop_code = pw.CharField(max_length=10)  # 苏宁商品URL中含有店铺代码, 需保存
    sku = pw.CharField(max_length=20)  # 商品SKU编号

    class Meta:
        primary_key = pw.CompositeKey('shop_code', 'sku')


if __name__ == '__main__':
    wireless_headphone_db.create_tables([Commodity, JDTargetSku, JDExistedSku, SNTargetSku, SNExistedSku])
