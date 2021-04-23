from db.wireless_headphone_models import Commodity


# 预处理原生数据
def preprocess_data():
    # 删除销量为0的无效数据
    Commodity.delete().where(Commodity.total == 0).execute()


if __name__ == '__main__':
    preprocess_data()
