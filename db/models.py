import peewee as pw

db = pw.SqliteDatabase('test.db')


class Test(pw.Model):
    pid = pw.IntegerField(primary_key=True)
    content = pw.TextField()
    vcontent = pw.CharField(max_length=200, default='test')

    class Meta:
        database = db


if __name__ == '__main__':
    db.connect()
    db.create_tables([Test])
    db.close()
