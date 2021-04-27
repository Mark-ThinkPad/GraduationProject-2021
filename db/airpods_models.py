import peewee as pw
from conf.settings import DATABASE_DIR

airpods_db = pw.SqliteDatabase(DATABASE_DIR + '/airpods.db', pragmas=(('foreign_keys', 1),))


class BaseModel(pw.Model):
    class Meta:
        database = airpods_db


# 店铺
class Shop(BaseModel):
    source = pw.CharField(max_length=4)
    is_official = pw.BooleanField()
    url = pw.TextField(unique=True)  # 网页URL链接


# 评论
class Comment(BaseModel):
    # 评论ID, 前缀JD, SN, YP, YX
    comment_id = pw.CharField(max_length=20, primary_key=True)
    source = pw.CharField(max_length=4)
    is_official = pw.BooleanField()
    create_time = pw.DateTimeField()  # 评论创建时间
    content = pw.TextField()  # 评论内容
    star = pw.SmallIntegerField(constraints=[pw.Check('star between 0 and 5')])  # 评分星级
    spec = pw.CharField(max_length=120)  # 产品型号信息
    after_time = pw.DateTimeField(null=True)  # 追评时间
    after_content = pw.TextField(null=True)  # 追评内容
    after_days = pw.SmallIntegerField(null=True)  # 追评间隔时间
    order_time = pw.DateTimeField(null=True)  # 下单时间, 限京东数据源
    order_days = pw.SmallIntegerField(null=True)  # 从下单到评论的时间(包括物流时间)
    user_device = pw.CharField(max_length=10, null=True)  # 用户设备类型, Android, iOS, other, 限京东和苏宁数据源


# 评论统计
class CommentSummary(BaseModel):
    source = pw.CharField(max_length=4)
    is_official = pw.BooleanField()
    total = pw.IntegerField()  # 评论总数
    good_rate = pw.CharField(max_length=4, null=True)  # 好评率
    default_good = pw.IntegerField(null=True)  # 默认好评数
    star_one = pw.IntegerField(null=True)  # 一星数量
    star_two = pw.IntegerField(null=True)  # 二星数量
    star_three = pw.IntegerField(null=True)  # 三星数量
    star_four = pw.IntegerField(null=True)  # 四星数量
    star_five = pw.IntegerField(null=True)  # 五星数量

    class Meta:
        primary_key = pw.CompositeKey('source', 'is_official')  # 复合主键


# 型号统计
class ModelSummary(BaseModel):
    source = pw.CharField(max_length=4)
    is_official = pw.BooleanField()
    spec = pw.CharField(max_length=120)  # 产品型号信息
    total = pw.IntegerField()
    good_rate = pw.CharField(max_length=4, null=True)  # 好评率
    default_good = pw.IntegerField(null=True)  # 默认好评数
    star_one = pw.IntegerField(null=True)  # 一星数量
    star_two = pw.IntegerField(null=True)  # 二星数量
    star_three = pw.IntegerField(null=True)  # 三星数量
    star_four = pw.IntegerField(null=True)  # 四星数量
    star_five = pw.IntegerField(null=True)  # 五星数量

    class Meta:
        primary_key = pw.CompositeKey('source', 'is_official', 'spec')  # 复合主键


# 京东SKU
class JDSku(BaseModel):
    sku = pw.CharField(max_length=20, primary_key=True)  # 商品SKU编号


# 苏宁SKU
class SNSku(BaseModel):
    shop_code = pw.CharField(max_length=10)  # 苏宁店铺代码
    sku = pw.CharField(max_length=20)

    class Meta:
        primary_key = pw.CompositeKey('shop_code', 'sku')


if __name__ == '__main__':
    airpods_db.create_tables([Shop, Comment, CommentSummary, ModelSummary, JDSku, SNSku])
