import peewee as pw

mi10_db = pw.SqliteDatabase('mi10.db')


class BaseModel(pw.Model):
    class Meta:
        database = mi10_db


# 店铺
class Shop(BaseModel):
    url = pw.TextField(unique=True)  # 网页URL链接
    source = pw.CharField(max_length=4)  # 平台数据源
    is_official = pw.BooleanField()  # 是否为官方自营/官方旗舰店


# 评论
class Comment(BaseModel):
    comment_id = pw.CharField(max_length=20, primary_key=True)  # 评论ID, 前缀JD, SN等, 小米商城和小米有品共用MI前缀(评论互通)
    source = pw.CharField(max_length=4)  # 平台数据源
    is_official = pw.BooleanField()  # 是否为官方自营/官方旗舰店
    create_time = pw.DateTimeField()  # 评论创建时间
    content = pw.TextField()  # 评论内容
    after_time = pw.DateTimeField(null=True)  # 追评时间
    after_content = pw.TextField()  # 追评内容
    after_days = pw.SmallIntegerField(null=True)  # 追评间隔时间
    order_time = pw.DateTimeField(null=True)  # 下单时间, 限京东数据源
    order_days = pw.SmallIntegerField(null=True)  # 从下单到评论的时间(包括物流时间)
    user_device = pw.CharField(max_length=10, null=True)  # 用户设备类型, Android, iOS, other, 限京东和苏宁数据源
    product_color = pw.CharField(max_length=5)  # 产品颜色版本
    product_ram = pw.CharField(max_length=4, constraints=[pw.Check('product_ram in ("8GB","12GB")')])  # 内存大小
    product_rom = pw.CharField(max_length=5, constraints=[pw.Check('product_rom in ("128GB","256GB")')])  # 储存大小


class Summary(BaseModel):
    pass


if __name__ == '__main__':
    mi10_db.connect()
    mi10_db.create_tables([Comment])
    mi10_db.close()
