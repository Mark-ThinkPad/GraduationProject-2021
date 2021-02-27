import peewee as pw

mi10_db = pw.SqliteDatabase('mi10.db')


class BaseModel(pw.Model):
    class Meta:
        database = mi10_db


class Comment(BaseModel):
    pass


if __name__ == '__main__':
    mi10_db.connect()
    mi10_db.create_tables([Comment])
    mi10_db.close()
