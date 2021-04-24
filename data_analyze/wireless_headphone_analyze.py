from db.wireless_headphone_models import Commodity


# 预处理原生数据
def preprocess_data():
    # 删除销量为0的无效数据
    # Commodity.delete().where(Commodity.total == 0).execute()

    # 统一品牌名
    # brand_list = ['HYUNDAI']
    # Commodity.update(brand='现代').where(Commodity.brand.in_(brand_list)).execute()
    # for commodity in Commodity.select().group_by(Commodity.brand):
    #     print(commodity.brand)

    # 规范产品名
    target_brand = 'AKG'
    name_list = ['']
    Commodity.update(model='').where((Commodity.model.in_(name_list)) & (Commodity.brand == target_brand))\
        .execute()
    for commodity in Commodity.select().where(Commodity.brand == target_brand).group_by(Commodity.model):
        print(commodity.model)


if __name__ == '__main__':
    preprocess_data()
