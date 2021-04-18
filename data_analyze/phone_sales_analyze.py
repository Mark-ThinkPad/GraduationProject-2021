from db.phone_sales_models import Commodity


# 预处理原生数据
def preprocess_data():
    # 删除销量为0的无效数据
    # query = Commodity.delete().where(Commodity.total == 0)
    # query.execute()
    # 找出销量被标记为-1的商品
    # for commodity in Commodity.select().where(Commodity.total == -1):
    #     print(commodity.url)
    # 找出价格被标记为-1和-2的商品
    # for commodity in Commodity.select().where(Commodity.price.in_([-1, -2])):
    #     print(commodity.url)
    # 统一品牌名
    for commodity in Commodity.select().group_by(Commodity.brand):
        print(commodity.brand)

    # query = Commodity.update(brand='21克').where(Commodity.brand.in_(['21KE', '21克(21ke)']))
    # query.execute()
    # query = Commodity.update(brand='百合').where(Commodity.brand.in_(['BIHEE']))
    # query.execute()
    # query = Commodity.update(brand='征服').where(Commodity.brand.in_(['CONQUEST']))
    # query.execute()
    # query = Commodity.update(brand='龙贝尔').where(Commodity.brand.in_(['LBER']))
    # query.execute()
    # query = Commodity.update(brand='新路虎').where(Commodity.brand.in_(['LGRAVER']))
    # query.execute()
    # query = Commodity.update(brand='硕王').where(Commodity.brand.in_(['SAILF']))
    # query.execute()
    # query = Commodity.update(brand='优畅想').where(Commodity.brand.in_(['U-Magic']))
    # query.execute()
    # query = Commodity.update(brand='纬图').where(Commodity.brand.in_(['VERTU']))
    # query.execute()
    # query = Commodity.update(brand='索野').where(Commodity.brand.in_(['soyes', '索野(SOYES)', '索野（SOYES）']))
    # query.execute()
    # query = Commodity.update(brand='京崎').where(Commodity.brand.in_(['京崎（TOOKY）']))
    # query.execute()
    # query = Commodity.update(brand='依偎').where(Commodity.brand.in_(['依偎(ivvi)']))
    # query.execute()
    # query = Commodity.update(brand='克里特').where(Commodity.brand.in_(['克里特（kreta）']))
    # query.execute()
    # query = Commodity.update(brand='北斗天地').where(Commodity.brand.in_(['北斗天地（BDTD）']))
    # query.execute()
    # query = Commodity.update(brand='守护宝(上海中兴)').where(Commodity.brand.in_(['守护宝', '守护宝(angel care)']))
    # query.execute()
    # query = Commodity.update(brand='尼凯恩').where(Commodity.brand.in_(['尼凯恩（neken）']))
    # query.execute()
    # query = Commodity.update(brand='康佳').where(Commodity.brand.in_(['康佳(KONKA)', '康佳（KONKA）']))
    # query.execute()
    # query = Commodity.update(brand='捷语').where(Commodity.brand.in_(['捷语（GoFly）']))
    # query.execute()
    # query = Commodity.update(brand='朵唯').where(Commodity.brand.in_(['朵唯(DOOV)', '朵唯（DOOV）']))
    # query.execute()
    # query = Commodity.update(brand='天语').where(Commodity.brand.in_(['天语(K-Touch)', '天语（K-TOUCH）', '天语（K-Touch）']))
    # query.execute()
    # query = Commodity.update(brand='欧奇').where(Commodity.brand.in_(['欧奇（OUKI）']))
    # query.execute()
    # query = Commodity.update(brand='波导').where(Commodity.brand.in_(['波导(BiRD)']))
    # query.execute()
    # query = Commodity.update(brand='海信').where(Commodity.brand.in_(['海信(Hisense)', '海信（Hisense）']))
    # query.execute()
    # query = Commodity.update(brand='海语').where(Commodity.brand.in_(['海语（HAIYU）']))
    # query.execute()
    # query = Commodity.update(brand='爱户外').where(Commodity.brand.in_(['爱户外（ioutdoor）']))
    # query.execute()
    # query = Commodity.update(brand='糖果').where(Commodity.brand.in_(['糖果（sugar）']))
    # query.execute()
    # query = Commodity.update(brand='索爱').where(Commodity.brand.in_(['索爱(soaiy)', '索爱（soaiy）']))
    # query.execute()
    # query = Commodity.update(brand='纽万').where(Commodity.brand.in_(['纽万(NEWONE)']))
    # query.execute()
    # query = Commodity.update(brand='纽曼').where(Commodity.brand.in_(['纽曼(Newman)', '纽曼(Newsmy)', '纽曼（Newman）']))
    # query.execute()
    # query = Commodity.update(brand='詹姆士').where(Commodity.brand.in_(['詹姆士（GEMRY）', '詹姆士（GERMY）']))
    # query.execute()
    # query = Commodity.update(brand='誉品').where(Commodity.brand.in_(['誉品(YEPEN)', '誉品（YEPEN）']))
    # query.execute()
    # query = Commodity.update(brand='诺亚信').where(Commodity.brand.in_(['诺亚信（NOAIN）']))
    # query.execute()
    # query = Commodity.update(brand='遨游').where(Commodity.brand.in_(['遨游（AORO）']))
    # query.execute()
    # query = Commodity.update(brand='酷和').where(Commodity.brand.in_(['酷和(KUH)']))
    # query.execute()
    # query = Commodity.update(brand='酷比').where(Commodity.brand.in_(['酷比(koobee)', '酷比（koobee）']))
    # query.execute()
    # query = Commodity.update(brand='酷派').where(Commodity.brand.in_(['酷派(Coolpad)', '酷派（Coolpad）']))
    # query.execute()
    # query = Commodity.update(brand='金伯利').where(Commodity.brand.in_(['金伯利(JINBOLI)']))
    # query.execute()
    # query = Commodity.update(brand='金立').where(Commodity.brand.in_(['金立(GiONEE)', '金立（GiONEE）', '金立（Gionee）']))
    # query.execute()
    # query = Commodity.update(brand='青橙').where(Commodity.brand.in_(['青橙(Green Orange)']))
    # query.execute()
    # query = Commodity.update(brand='飞利浦').where(Commodity.brand.in_(['飞利浦(Philips)', '飞利浦（PHILIPS ）']))
    # query.execute()
    #
    # query = Commodity.update(brand='苹果').where(Commodity.brand.in_(['APPLE', 'Apple', 'iPhone', '苹果（Apple）']))
    # query.execute()
    # query = Commodity.update(brand='荣耀').where(Commodity.brand.in_(['HONOR', '荣耀(honor)', '荣耀（HONOR）', '荣耀（honor）']))
    # query.execute()
    # query = Commodity.update(brand='小米').where(Commodity.brand.in_(['XIAOMI', '小米(mi)', '小米（MI）']))
    # query.execute()
    # query = Commodity.update(brand='OPPO').where(Commodity.brand.in_(['oppo']))
    # query.execute()
    # query = Commodity.update(brand='vivo').where(Commodity.brand.in_(['维沃（vivo）', 'iQOO']))
    # query.execute()
    # query = Commodity.update(brand='三星').where(Commodity.brand.in_(['三星(SAMSUNG)', '三星（SAMSUNG）']))
    # query.execute()
    # query = Commodity.update(brand='中兴').where(Commodity.brand.in_(['中兴(ZTE)', '中兴（ZTE）']))
    # query.execute()
    # query = Commodity.update(brand='努比亚').where(Commodity.brand.in_(['努比亚(nubia)', '努比亚（nubia）']))
    # query.execute()
    # query = Commodity.update(brand='华为').where(Commodity.brand.in_(['华为(HUAWEI)', '华为（HUAWEI）', '麦芒']))
    # query.execute()
    # query = Commodity.update(brand='锤子/坚果').where(Commodity.brand.in_(['坚果', '锤子（smartisan）']))
    # query.execute()
    # query = Commodity.update(brand='多亲').where(Commodity.brand.in_(['多亲(QIN)', '多亲（QIN）']))
    # query.execute()
    # query = Commodity.update(brand='摩托罗拉').where(Commodity.brand.in_(['摩托罗拉(MOTOROLA)', '摩托罗拉（Motorola）']))
    # query.execute()
    # query = Commodity.update(brand='柔宇').where(Commodity.brand.in_(['柔宇(ROYOLE)', '柔宇（ROYOLE）']))
    # query.execute()
    # query = Commodity.update(brand='realme').where(Commodity.brand.in_(['真我（realme）']))
    # query.execute()
    # query = Commodity.update(brand='索尼').where(Commodity.brand.in_(['索尼(SONY)', '索尼（SONY）', 'SONY']))
    # query.execute()
    # query = Commodity.update(brand='美图').where(Commodity.brand.in_(['美图(Meitu)']))
    # query.execute()
    # query = Commodity.update(brand='联想').where(Commodity.brand.in_(['联想(Lenovo)', '联想（LENOVO）', '联想（Lenovo）',
    #                                                                 '联想（lenovo）']))
    # query.execute()
    # query = Commodity.update(brand='诺基亚').where(Commodity.brand.in_(['诺基亚(NOKIA)', '诺基亚（NOKIA）']))
    # query.execute()
    # query = Commodity.update(brand='魅族').where(Commodity.brand.in_(['魅族(MEIZU)', '魅族（MEIZU）', '魅族（meizu）']))
    # query.execute()

    # 规范产品名
    # name_list = ['黑鲨4 Pro']
    # Commodity.update(model='黑鲨游戏手机4 Pro').where(Commodity.model.in_(name_list)).execute()

    # 规范操作系统名和SoC信息
    # target_brand = '荣耀'
    # model_list = ['荣耀畅玩9A']
    # Commodity.update({
    #     Commodity.os: 'Android',
    #     Commodity.soc_mfrs: '联发科',
    #     Commodity.soc_model: 'P35'
    # }).where((Commodity.model.in_(model_list)) & (Commodity.brand == target_brand)).execute()
    # for commodity in Commodity.select().where(Commodity.brand == target_brand).group_by(Commodity.model):
    #     print(commodity.model)
    # for commodity in Commodity.select().where(Commodity.brand == target_brand).group_by(Commodity.soc_mfrs):
    #     print(commodity.soc_mfrs)
    # for commodity in Commodity.select().where(Commodity.brand == target_brand).group_by(Commodity.soc_model):
    #     print(commodity.soc_model)

    Commodity.update({Commodity.soc_model: '未知'}).where(Commodity.soc_model.in_(['其它', '其他', '以官网信息为准', '以官方信息为准'])).execute()
    for commodity in Commodity.select().group_by(Commodity.soc_model):
        print(commodity.soc_model)


if __name__ == '__main__':
    preprocess_data()
