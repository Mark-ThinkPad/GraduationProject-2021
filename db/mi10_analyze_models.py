import peewee as pw
from conf.settings import DATABASE_DIR

mi10_analyze_db = pw.SqliteDatabase(DATABASE_DIR + '/mi10_analyze.db', pragmas=(('foreign_keys', 1),))


class BaseModel(pw.Model):
    class Meta:
        database = mi10_analyze_db


# 统计用户发表评论时使用的设备类型, 用于计算安卓用户留存率和iOS用户转化率
class UserDeviceCount(BaseModel):
    total = pw.IntegerField()
    android = pw.IntegerField()
    ios = pw.IntegerField()
    other = pw.IntegerField()
    android_percentage = pw.CharField(max_length=4)
    ios_percentage = pw.CharField(max_length=4)
    other_percentage = pw.CharField(max_length=4)


# 评论总计数量
# 由于京东平台不再显示评论总数和默认好评数的具体数据, 改为类似于70万+的大致数值, 所以需要简单处理一下
# 苏宁平台的数据中, 总数和所有型号数据加总的数据不相等
class Total(BaseModel):
    source = pw.CharField(max_length=4, primary_key=True, constraints=[pw.Check('source in ("京东", "苏宁", "小米商城")')])
    total = pw.IntegerField()  # 基于CommentSummary的总数
    all_models_total = pw.IntegerField()  # 基于所有ModelSummary加和的数据
    good_rate = pw.CharField(max_length=4)  # 好评率
    default_good = pw.IntegerField()  # 默认好评数
    good_count = pw.IntegerField()  # 好评数
    general_count = pw.IntegerField()  # 中评数
    bad_count = pw.IntegerField()  # 差评数
    star_one = pw.IntegerField()  # 一星数量
    star_two = pw.IntegerField()  # 二星数量
    star_three = pw.IntegerField()  # 三星数量
    star_four = pw.IntegerField()  # 四星数量
    star_five = pw.IntegerField()  # 五星数量


# 各个型号的统计数据 (苏宁和京东数据合并)
class ModelCount(BaseModel):
    # 产品型号信息
    product_color = pw.CharField(max_length=4,
                                 constraints=[pw.Check('product_color in ("国风雅灰", "钛银黑", "冰海蓝", "蜜桃金")')])  # 产品颜色版本
    product_ram = pw.CharField(max_length=4, constraints=[pw.Check('product_ram in ("8GB", "12GB")')])  # 内存大小
    product_rom = pw.CharField(max_length=5, constraints=[pw.Check('product_rom in ("128GB", "256GB")')])  # 储存大小
    total = pw.IntegerField(null=True)
    percentage = pw.CharField(max_length=4, null=True)  # 该型号占总数的百分比
    cal_total = pw.IntegerField(null=True)  # 用于计算好评率的总数 (京东计算规则)
    good_rate = pw.CharField(max_length=4, null=True)  # 好评率
    default_good = pw.IntegerField(null=True)  # 默认好评数
    good_count = pw.IntegerField(null=True)  # 好评数
    general_count = pw.IntegerField(null=True)  # 中评数
    bad_count = pw.IntegerField(null=True)  # 差评数
    star_one = pw.IntegerField(null=True)  # 一星数量
    star_two = pw.IntegerField(null=True)  # 二星数量
    star_three = pw.IntegerField(null=True)  # 三星数量
    star_four = pw.IntegerField(null=True)  # 四星数量
    star_five = pw.IntegerField(null=True)  # 五星数量

    class Meta:
        primary_key = pw.CompositeKey('product_color', 'product_ram', 'product_rom')  # 复合主键


if __name__ == '__main__':
    mi10_analyze_db.create_tables([UserDeviceCount, Total, ModelCount])
