import peewee as pw
from conf.settings import DATABASE_DIR

wireless_headphone_analyze_db = pw.SqliteDatabase(DATABASE_DIR + '/wireless_headphone_analyze.db',
                                                  pragmas=(('foreign_keys', 1),))


class BaseModel(pw.Model):
    class Meta:
        database = wireless_headphone_analyze_db


if __name__ == '__main__':
    pass
