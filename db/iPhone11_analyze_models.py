import peewee as pw
from conf.settings import DATABASE_DIR

iPhone11_analyze_db = pw.SqliteDatabase(DATABASE_DIR + '/iPhone11_analyze.db', pragmas=(('foreign_keys', 1),))


class BaseModel(pw.Model):
    class Meta:
        database = iPhone11_analyze_db


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
    source = pw.CharField(max_length=4, primary_key=True, constraints=[pw.Check('source in ("京东", "苏宁")')])
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
    color = pw.CharField(max_length=2, constraints=[pw.Check('color in ("黑色", "白色", "红色", "黄色", "紫色", "绿色")')])
    rom = pw.CharField(max_length=5, constraints=[pw.Check('rom in ("64GB", "128GB", "256GB")')])
    total = pw.IntegerField(default=0)
    percentage = pw.CharField(max_length=4, null=True)  # 该型号占总数的百分比
    cal_total = pw.IntegerField(default=0)  # 用于计算好评率的总数 (京东计算规则)
    good_rate = pw.CharField(max_length=4, null=True)  # 好评率
    default_good = pw.IntegerField(default=0)  # 默认好评数
    good_count = pw.IntegerField(default=0)  # 好评数
    general_count = pw.IntegerField(default=0)  # 中评数
    bad_count = pw.IntegerField(default=0)  # 差评数
    star_one = pw.IntegerField(default=0)  # 一星数量
    star_two = pw.IntegerField(default=0)  # 二星数量
    star_three = pw.IntegerField(default=0)  # 三星数量
    star_four = pw.IntegerField(default=0)  # 四星数量
    star_five = pw.IntegerField(default=0)  # 五星数量

    class Meta:
        primary_key = pw.CompositeKey('color', 'rom')  # 复合主键


# 不同颜色的统计数据
class ColorCount(BaseModel):
    color = pw.CharField(max_length=2, primary_key=True,
                         constraints=[pw.Check('color in ("黑色", "白色", "红色", "黄色", "紫色", "绿色")')])
    total = pw.IntegerField()
    percentage = pw.CharField(max_length=4)
    cal_total = pw.IntegerField()
    good_rate = pw.CharField(max_length=4)
    default_good = pw.IntegerField()  # 默认好评数
    good_count = pw.IntegerField()  # 好评数
    general_count = pw.IntegerField()  # 中评数
    bad_count = pw.IntegerField()  # 差评数
    star_one = pw.IntegerField()  # 一星数量
    star_two = pw.IntegerField()  # 二星数量
    star_three = pw.IntegerField()  # 三星数量
    star_four = pw.IntegerField()  # 四星数量
    star_five = pw.IntegerField()  # 五星数量


# 不同储存的统计数据
class RomCount(BaseModel):
    rom = pw.CharField(max_length=5, primary_key=True, constraints=[pw.Check('rom in ("64GB", "128GB", "256GB")')])
    total = pw.IntegerField()
    percentage = pw.CharField(max_length=4)
    cal_total = pw.IntegerField()
    good_rate = pw.CharField(max_length=4)
    default_good = pw.IntegerField()  # 默认好评数
    good_count = pw.IntegerField()  # 好评数
    general_count = pw.IntegerField()  # 中评数
    bad_count = pw.IntegerField()  # 差评数
    star_one = pw.IntegerField()  # 一星数量
    star_two = pw.IntegerField()  # 二星数量
    star_three = pw.IntegerField()  # 三星数量
    star_four = pw.IntegerField()  # 四星数量
    star_five = pw.IntegerField()  # 五星数量


# 用户评论分布时间 (月度)
class CommentDateCount(BaseModel):
    year_month = pw.CharField(max_length=7, primary_key=True)
    total = pw.IntegerField(default=0)
    percentage = pw.CharField(max_length=4, null=True)


# 追评间隔时间分布
class AfterDaysCount(BaseModel):
    after_days = pw.SmallIntegerField(primary_key=True)
    total = pw.IntegerField(default=0)
    percentage = pw.CharField(max_length=4, null=True)


# 用户下单时间分布 (月度) (仅限京东数据源)
class OrderDateCount(BaseModel):
    year_month = pw.CharField(max_length=7, primary_key=True)
    total = pw.IntegerField(default=0)
    percentage = pw.CharField(max_length=4, null=True)


# 用户下单到评论的间隔时间 (仅限京东数据源)
class OrderDaysCount(BaseModel):
    order_days = pw.SmallIntegerField(primary_key=True)
    total = pw.IntegerField(default=0)
    percentage = pw.CharField(max_length=4, null=True)


# 用户活跃度 (基于非默认好评数量)
class UserActivity(BaseModel):
    source = pw.CharField(max_length=4, primary_key=True, constraints=[pw.Check('source in ("京东", "苏宁")')])
    total = pw.IntegerField()
    active_count = pw.IntegerField()  # 活跃用户数 (非默认好评)
    active_percentage = pw.CharField(max_length=4)
    inactive_count = pw.IntegerField()  # 非活跃用户数 (默认好评数)
    inactive_percentage = pw.CharField(max_length=4)


# 所有评论中提取的高频词 (不包括追评)
class AllCommentsWords(BaseModel):
    word = pw.CharField(max_length=20, primary_key=True)


# 追评高频词
class AfterCommentsWords(BaseModel):
    word = pw.CharField(max_length=20, primary_key=True)


# iOS转化用户评论高频词
class IosCommentsWords(BaseModel):
    word = pw.CharField(max_length=20, primary_key=True)


# 评分五星以下用户评论的高频词
class NonFiveStarCommentsWords(BaseModel):
    word = pw.CharField(max_length=20, primary_key=True)


if __name__ == '__main__':
    iPhone11_analyze_db.create_tables([UserDeviceCount, Total, ModelCount, ColorCount, RomCount, CommentDateCount,
                                       AfterDaysCount, OrderDateCount, OrderDaysCount, UserActivity, AllCommentsWords,
                                       AfterCommentsWords, IosCommentsWords, NonFiveStarCommentsWords])
