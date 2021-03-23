import peewee as pw
from conf.settings import DATABASE_DIR

mi10_analyze_db = pw.SqliteDatabase(DATABASE_DIR + '/mi10_analyze.db', pragmas=(('foreign_keys', 1),))


class BaseModel(pw.Model):
    class Meta:
        database = mi10_analyze_db


# 用户发表评论时使用的设备类型, 用于计算安卓用户留存率和iOS用户转化率
class UserDeviceSummary(BaseModel):
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
    star_one = pw.IntegerField(null=True)  # 一星数量
    star_two = pw.IntegerField(null=True)  # 二星数量
    star_three = pw.IntegerField(null=True)  # 三星数量
    star_four = pw.IntegerField(null=True)  # 四星数量
    star_five = pw.IntegerField(null=True)  # 五星数量


if __name__ == '__main__':
    mi10_analyze_db.create_tables([Total])
