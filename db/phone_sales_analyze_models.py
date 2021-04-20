import peewee as pw
from conf.settings import DATABASE_DIR

phone_sales_analyze_db = pw.SqliteDatabase(DATABASE_DIR + '/phone_analyze_sales.db', pragmas=(('foreign_keys', 1),))


class BaseModel(pw.Model):
    class Meta:
        database = phone_sales_analyze_db


class Phone(BaseModel):
    brand = pw.CharField(max_length=40)  # 品牌
    model = pw.CharField(max_length=200)  # 产品型号
    total = pw.IntegerField()  # 销量/评价总数
    ref_price = pw.FloatField(null=True)  # 参考价格

    class Meta:
        primary_key = pw.CompositeKey('brand', 'model')


if __name__ == '__main__':
    pass
