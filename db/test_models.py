import peewee as pw

db = pw.SqliteDatabase('test.db')


class Test(pw.Model):
    pid = pw.IntegerField(primary_key=True)
    content = pw.TextField()
    vcontent = pw.IntegerField(default=1)

    class Meta:
        database = db


if __name__ == '__main__':
    db.connect()
    db.create_tables([Test])
    db.close()
