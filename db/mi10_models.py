import peewee as pw

mi10_db = pw.SqliteDatabase('mi10.db')


class BaseModel(pw.Model):
    class Meta:
        database = mi10_db


# 店铺
class Shop(BaseModel):
    url = pw.TextField(unique=True)  # 网页URL链接
    # 平台数据源
    source = pw.CharField(max_length=4, constraints=[pw.Check('source in ("京东", "苏宁", "小米有品", "小米商城")')])
    is_official = pw.BooleanField()  # 是否为官方自营/官方旗舰店


# 评论
class Comment(BaseModel):
    # 评论ID, 前缀JD, SN等, 小米商城和小米有品共用MI前缀(评论互通)
    comment_id = pw.CharField(max_length=20, primary_key=True)
    # 平台数据源
    source = pw.CharField(max_length=4, constraints=[pw.Check('source in ("京东", "苏宁", "小米有品", "小米商城")')])
    is_official = pw.BooleanField()  # 是否为官方自营/官方旗舰店
    create_time = pw.DateTimeField()  # 评论创建时间
    content = pw.TextField()  # 评论内容
    star = pw.SmallIntegerField(constraints=[pw.Check('star between 1 and 5')])  # 评分星级
    after_time = pw.DateTimeField(null=True)  # 追评时间
    after_content = pw.TextField()  # 追评内容
    after_days = pw.SmallIntegerField(null=True)  # 追评间隔时间
    order_time = pw.DateTimeField(null=True)  # 下单时间, 限京东数据源
    order_days = pw.SmallIntegerField(null=True)  # 从下单到评论的时间(包括物流时间)
    user_device = pw.CharField(max_length=10, null=True)  # 用户设备类型, Android, iOS, other, 限京东和苏宁数据源
    # 产品型号信息
    product_color = pw.CharField(max_length=4,
                                 constraints=[pw.Check('product_color in ("国风雅灰", "钛银黑", "冰海蓝", "蜜桃金")')])  # 产品颜色版本
    product_ram = pw.CharField(max_length=4, constraints=[pw.Check('product_ram in ("8GB", "12GB")')])  # 内存大小
    product_rom = pw.CharField(max_length=5, constraints=[pw.Check('product_rom in ("128GB", "256GB")')])  # 储存大小


# 评论统计
class CommentSummary(BaseModel):
    # 平台数据源
    source = pw.CharField(max_length=4, constraints=[pw.Check('source in ("京东", "苏宁", "小米有品", "小米商城")')])
    is_official = pw.BooleanField()  # 是否为官方自营/官方旗舰店
    total = pw.IntegerField()  # 评论总数
    good_rate = pw.CharField(max_length=4)  # 好评率
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
    # 平台数据源
    source = pw.CharField(max_length=4, constraints=[pw.Check('source in ("京东", "苏宁", "小米有品", "小米商城")')])
    is_official = pw.BooleanField()  # 是否为官方自营/官方旗舰店
    # 产品型号信息
    product_color = pw.CharField(max_length=4,
                                 constraints=[pw.Check('product_color in ("国风雅灰", "钛银黑", "冰海蓝", "蜜桃金")')])  # 产品颜色版本
    product_ram = pw.CharField(max_length=4, constraints=[pw.Check('product_ram in ("8GB", "12GB")')])  # 内存大小
    product_rom = pw.CharField(max_length=5, constraints=[pw.Check('product_rom in ("128GB", "256GB")')])  # 储存大小
    total = pw.IntegerField()

    class Meta:
        primary_key = pw.CompositeKey('source', 'is_official', 'product_color', 'product_ram', 'product_rom')  # 复合主键


if __name__ == '__main__':
    mi10_db.connect()
    mi10_db.create_tables([Shop, Comment, CommentSummary, ModelSummary])
    mi10_db.close()
