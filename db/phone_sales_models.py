import peewee as pw
from conf.settings import DATABASE_DIR

phone_sales_db = pw.SqliteDatabase(DATABASE_DIR + '/phone_sales.db', pragmas=(('foreign_keys', 1),))


class BaseModel(pw.Model):
    class Meta:
        database = phone_sales_db


# 商品模型
class Commodity(BaseModel):
    source = pw.CharField(max_length=4, constraints=[pw.Check('source in ("京东", "苏宁")')])  # 数据源平台
    url = pw.TextField(unique=True)  # 商品链接
    title = pw.CharField(max_length=200)  # 商品标题
    shop_name = pw.CharField(max_length=60)  # 店铺名称
    is_self = pw.BooleanField()  # 是否为官方自营店铺
    price = pw.FloatField()  # 价格
    total = pw.IntegerField()  # 销量/评价总数
    brand = pw.CharField(max_length=40)  # 品牌
    model = pw.CharField(max_length=200)  # 产品型号
    os = pw.CharField(max_length=40)  # 操作系统
    # 可选信息
    soc_mfrs = pw.CharField(max_length=40, null=True)  # SoC制造商, mfrs为manufacturer的缩写
    soc_model = pw.CharField(max_length=20, null=True)  # SoC型号
    width = pw.FloatField(null=True)  # 机身宽度
    thickness = pw.FloatField(null=True)  # 机身厚度
    length = pw.FloatField(null=True)  # 机身长度
    weight = pw.FloatField(null=True)  # 机身重量
    screen_size = pw.FloatField(null=True)  # 屏幕尺寸


# 已存在的SKU, 避免销量重复计数
class ExistedSku(BaseModel):
    source = pw.CharField(max_length=4, constraints=[pw.Check('source in ("京东", "苏宁")')])  # 数据源平台
    sku = pw.CharField(max_length=20)  # 商品SKU编号

    class Meta:
        primary_key = pw.CompositeKey('source', 'sku')


# 所有将要获取的商品SKU编号
class TargetSku(BaseModel):
    source = pw.CharField(max_length=4, constraints=[pw.Check('source in ("京东", "苏宁")')])  # 数据源平台
    sku = pw.CharField(max_length=20)  # 商品SKU编号

    class Meta:
        primary_key = pw.CompositeKey('source', 'sku')


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
    phone_sales_db.create_tables([Commodity, ExistedSku, TargetSku, SNTargetSku, SNExistedSku])
