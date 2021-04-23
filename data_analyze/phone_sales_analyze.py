from peewee import fn
from data_analyze.utils import calculate_percentage, calculate_average, calculate_median
from db.phone_sales_models import Commodity
from db.phone_sales_analyze_models import (Phone, PhoneTotal, PhonePlatform, PhoneOS, PhoneBrand, BrandSalesStar,
                                           BrandPercentage, FeaturePhonePercentage, SoC, SoCMfrs, SoCStar,
                                           FeaturePhoneSoCPer, PhoneSize, PhonePriceAndSales, PhonePriceAndBrand)


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

    Commodity.update({Commodity.soc_model: '未知'}).where(
        Commodity.soc_model.in_(['其它', '其他', '以官网信息为准', '以官方信息为准'])).execute()
    for commodity in Commodity.select().group_by(Commodity.soc_model):
        print(commodity.soc_model)


# 生成型号及销量
def get_phone():
    for commodity in Commodity.select():
        try:
            phone = Phone.get(
                Phone.brand == commodity.brand,
                Phone.model == commodity.model
            )
            phone.total += commodity.total
            phone.save()
        except Phone.DoesNotExist:
            Phone.create(
                brand=commodity.brand,
                model=commodity.model,
                total=commodity.total
            )


# 生成数据总览
def get_phone_total():
    total_count = Commodity.select(fn.SUM(Commodity.total).alias('tc')).dicts()[0]['tc']
    commodity_count = Commodity.select().count()
    brand_count = Commodity.select().group_by(Commodity.brand).count()
    model_count = Commodity.select().group_by(Commodity.model).count()

    PhoneTotal.create(
        total_count=total_count,
        commodity_count=commodity_count,
        brand_count=brand_count,
        model_count=model_count
    )


# 生成平台数据源概览
def get_phone_platform():
    source_list = ['京东', '苏宁']
    for source in source_list:
        total_count = Commodity.select(fn.SUM(Commodity.total).alias('tc')) \
            .where(Commodity.source == source).dicts()[0]['tc']
        commodity_count = Commodity.select().where(Commodity.source == source).count()
        self_count = Commodity.select(fn.SUM(Commodity.total).alias('tc')) \
            .where((Commodity.source == source) & (Commodity.is_self == True)).dicts()[0]['tc']
        non_self_count = Commodity.select(fn.SUM(Commodity.total).alias('tc')) \
            .where((Commodity.source == source) & (Commodity.is_self == False)).dicts()[0]['tc']

        PhonePlatform.create(
            source=source,
            total_count=total_count,
            commodity_count=commodity_count,
            self_percentage=calculate_percentage(total_count, self_count),
            non_self_percentage=calculate_percentage(total_count, non_self_count)
        )


# 生成操作系统占比
def get_phone_os():
    # for commodity in Commodity.select():
    #     try:
    #         phone_os = PhoneOS.get(PhoneOS.os == commodity.os)
    #         phone_os.total += commodity.total
    #         phone_os.save()
    #     except PhoneOS.DoesNotExist:
    #         PhoneOS.create(
    #             os=commodity.os,
    #             total=commodity.total
    #         )
    total_count = PhoneOS.select(fn.SUM(PhoneOS.total).alias('tc')).dicts()[0]['tc']
    for phone_os in PhoneOS.select():
        phone_os.percentage = calculate_percentage(total_count, phone_os.total)
        phone_os.save()


# 生成品牌销量占比
def get_phone_brand():
    # for commodity in Commodity.select():
    #     try:
    #         phone_brand = PhoneBrand.get(PhoneBrand.brand == commodity.brand)
    #         phone_brand.total += commodity.total
    #         phone_brand.save()
    #     except PhoneBrand.DoesNotExist:
    #         PhoneBrand.create(
    #             brand=commodity.brand,
    #             total=commodity.total
    #         )
    total_count = PhoneBrand.select(fn.SUM(PhoneBrand.total).alias('tc')).dicts()[0]['tc']
    print(total_count)
    for phone_brand in PhoneBrand.select():
        phone_brand.percentage = calculate_percentage(total_count, phone_brand.total)
        phone_brand.save()
        # if float(phone_brand.percentage) < 0.8:
        #     others = PhoneBrand.get_by_id('其他品牌')
        #     others.total += phone_brand.total
        #     others.save()
        #     phone_brand.delete_instance()


# 生成品牌销量明星
def get_brand_sales_star():
    brand_list = ['苹果', '小米', '华为', '荣耀', 'OPPO', 'vivo']
    for brand in brand_list:
        for phone in Phone.select().where(Phone.brand == brand):
            BrandSalesStar.create(
                brand=brand,
                model=phone.model,
                total=phone.total
            )


# 生成主品牌与子品牌销量占比
def get_brand_percentage():
    # redmi = BrandPercentage.get(
    #     BrandPercentage.main_brand == '小米',
    #     BrandPercentage.sub_brand == '红米'
    # )
    # xiaomi = BrandPercentage.get(
    #     BrandPercentage.main_brand == '小米',
    #     BrandPercentage.sub_brand == '小米'
    # )
    # for phone in Phone.select().where(Phone.brand == '小米'):
    #     if '小米' in phone.model:
    #         xiaomi.total += phone.total
    #         xiaomi.save()
    #     if '红米' in phone.model:
    #         redmi.total += phone.total
    #         redmi.save()
    #
    # vivo = BrandPercentage.get(
    #     BrandPercentage.main_brand == 'vivo',
    #     BrandPercentage.sub_brand == 'vivo'
    # )
    # iqoo = BrandPercentage.get(
    #     BrandPercentage.main_brand == 'vivo',
    #     BrandPercentage.sub_brand == 'iQOO'
    # )
    # for phone in Phone.select().where(Phone.brand == 'vivo'):
    #     if 'iQOO' in phone.model:
    #         iqoo.total += phone.total
    #         iqoo.save()
    #     else:
    #         vivo.total += phone.total
    #         vivo.save()
    #
    # oppo = BrandPercentage.get(
    #     BrandPercentage.main_brand == 'OPPO',
    #     BrandPercentage.sub_brand == 'OPPO'
    # )
    # realme = BrandPercentage.get(
    #     BrandPercentage.main_brand == 'OPPO',
    #     BrandPercentage.sub_brand == 'realme'
    # )
    # oneplus = BrandPercentage.get(
    #     BrandPercentage.main_brand == 'OPPO',
    #     BrandPercentage.sub_brand == '一加'
    # )
    # oppo.total = Phone.select(fn.SUM(Phone.total).alias('tc')).where(Phone.brand == 'OPPO').dicts()[0]['tc']
    # oppo.save()
    # realme.total = Phone.select(fn.SUM(Phone.total).alias('tc')).where(Phone.brand == 'realme').dicts()[0]['tc']
    # realme.save()
    # oneplus.total = Phone.select(fn.SUM(Phone.total).alias('tc')).where(Phone.brand == '一加').dicts()[0]['tc']
    # oneplus.save()

    brand_list = ['小米', 'OPPO', 'vivo']
    for brand in brand_list:
        total_count = BrandPercentage.select(fn.SUM(BrandPercentage.total).alias('tc')) \
            .where(BrandPercentage.main_brand == brand).dicts()[0]['tc']
        print(total_count)
        for bp in BrandPercentage.select().where(BrandPercentage.main_brand == brand):
            bp.percentage = calculate_percentage(total_count, bp.total)
            bp.save()


# 生成功能机品牌占比
def get_feature_phone_percentage():
    # for commodity in Commodity.select().where(Commodity.os == '功能机'):
    #     try:
    #         fpp = FeaturePhonePercentage.get(FeaturePhonePercentage.brand == commodity.brand)
    #         fpp.total += commodity.total
    #         fpp.save()
    #     except FeaturePhonePercentage.DoesNotExist:
    #         FeaturePhonePercentage.create(
    #             brand=commodity.brand,
    #             total=commodity.total
    #         )
    total_count = FeaturePhonePercentage.select(fn.SUM(FeaturePhonePercentage.total).alias('tc')).dicts()[0]['tc']
    print(total_count)
    for fpp in FeaturePhonePercentage.select():
        fpp.percentage = calculate_percentage(total_count, fpp.total)
        fpp.save()
        # if float(fpp.percentage) < 0.9:
        #     others = FeaturePhonePercentage.get_by_id('其他品牌')
        #     others.total += fpp.total
        #     others.save()
        #     fpp.delete_instance()


# 生成SoC型号及销量
def get_soc():
    for commodity in Commodity.select():
        try:
            soc = SoC.get(
                SoC.soc_mfrs == commodity.soc_mfrs,
                SoC.soc_model == commodity.soc_model
            )
            soc.total += commodity.total
            soc.save()
        except SoC.DoesNotExist:
            SoC.create(
                soc_mfrs=commodity.soc_mfrs,
                soc_model=commodity.soc_model,
                total=commodity.total
            )


# 生成SoC制造商占比
def get_soc_mfrs():
    for soc in SoC.select():
        try:
            soc_mfrs = SoCMfrs.get_by_id(soc.soc_mfrs)
            soc_mfrs.total += soc.total
            soc_mfrs.save()
        except SoCMfrs.DoesNotExist:
            SoCMfrs.create(
                soc_mfrs=soc.soc_mfrs,
                total=soc.total
            )
    total_count = SoCMfrs.select(fn.SUM(SoCMfrs.total).alias('tc')).dicts()[0]['tc']
    print(total_count)
    for soc_mfrs in SoCMfrs.select():
        soc_mfrs.percentage = calculate_percentage(total_count, soc_mfrs.total)
        soc_mfrs.save()


# 生成SoC制造商内部销量明星
def get_soc_star():
    for soc in SoC.select():
        SoCStar.create(
            soc_mfrs=soc.soc_mfrs,
            soc_model=soc.soc_model,
            total=soc.total
        )


# 生成功能机SoC制造商占比
def get_feature_phone_soc_percentage():
    # for commodity in Commodity.select().where(Commodity.os == '功能机'):
    #     try:
    #         fpsp = FeaturePhoneSoCPer.get(FeaturePhoneSoCPer.soc_mfrs == commodity.soc_mfrs)
    #         fpsp.total += commodity.total
    #         fpsp.save()
    #     except FeaturePhoneSoCPer.DoesNotExist:
    #         FeaturePhoneSoCPer.create(
    #             soc_mfrs=commodity.soc_mfrs,
    #             total=commodity.total
    #         )
    total_count = FeaturePhoneSoCPer.select(fn.SUM(FeaturePhoneSoCPer.total).alias('tc')).dicts()[0]['tc']
    print(total_count)
    for fpsp in FeaturePhoneSoCPer.select():
        fpsp.percentage = calculate_percentage(total_count, fpsp.total)
        fpsp.save()


# 生成智能手机各项尺寸参数的平均数和中位数
def get_phone_size():
    screen_size_list = []
    width_list = []
    thickness_list = []
    length_list = []
    weight_list = []

    for commodity in Commodity.select().where(Commodity.os.not_in(['功能机', '页面未注明'])):
        if commodity.screen_size is not None:
            screen_size_list.append(commodity.screen_size)
        if commodity.width is not None:
            width_list.append(commodity.width)
        if commodity.thickness is not None:
            thickness_list.append(commodity.thickness)
        if commodity.length is not None:
            length_list.append(commodity.length)
        if commodity.weight is not None:
            weight_list.append(commodity.weight)

    PhoneSize.create(
        screen_size_avg=calculate_average(screen_size_list, True),
        screen_size_med=calculate_median(screen_size_list, True),
        width_avg=calculate_average(width_list, True),
        width_med=calculate_median(width_list, True),
        thickness_avg=calculate_average(thickness_list, True),
        thickness_med=calculate_median(thickness_list, True),
        length_avg=calculate_average(length_list, True),
        length_med=calculate_median(length_list, True),
        weight_avg=calculate_average(weight_list, True),
        weight_med=calculate_median(weight_list, True)
    )


# 生成智能手机与功能机价格区间与销量分布
def get_phone_price_and_sales():
    # PhonePriceAndSales.create(
    #     type='功能机',
    #     price_range='500-1000元',
    #     total=0
    # )

    # for commodity in Commodity.select().where(Commodity.os.in_(['Android', 'iOS'])):
    #     if 0 < commodity.price < 500:
    #         ppas = PhonePriceAndSales.get_by_id(1)
    #         ppas.total += commodity.total
    #         ppas.save()
    #     if 500 <= commodity.price < 1000:
    #         ppas = PhonePriceAndSales.get_by_id(2)
    #         ppas.total += commodity.total
    #         ppas.save()
    #     if 1000 <= commodity.price < 2000:
    #         ppas = PhonePriceAndSales.get_by_id(3)
    #         ppas.total += commodity.total
    #         ppas.save()
    #     if 2000 <= commodity.price < 3000:
    #         ppas = PhonePriceAndSales.get_by_id(4)
    #         ppas.total += commodity.total
    #         ppas.save()
    #     if 3000 <= commodity.price < 4000:
    #         ppas = PhonePriceAndSales.get_by_id(5)
    #         ppas.total += commodity.total
    #         ppas.save()
    #     if 4000 <= commodity.price < 5000:
    #         ppas = PhonePriceAndSales.get_by_id(6)
    #         ppas.total += commodity.total
    #         ppas.save()
    #     if 5000 <= commodity.price < 8000:
    #         ppas = PhonePriceAndSales.get_by_id(7)
    #         ppas.total += commodity.total
    #         ppas.save()
    #     if commodity.price >= 8000:
    #         ppas = PhonePriceAndSales.get_by_id(8)
    #         ppas.total += commodity.total
    #         ppas.save()

    # total_count = PhonePriceAndSales.select(fn.SUM(PhonePriceAndSales.total).alias('tc')) \
    #     .where(PhonePriceAndSales.type == '智能手机').dicts()[0]['tc']
    # print(total_count)
    # for ppas in PhonePriceAndSales.select().where(PhonePriceAndSales.type == '智能手机'):
    #     ppas.percentage = calculate_percentage(total_count, ppas.total)
    #     ppas.save()

    for commodity in Commodity.select().where(Commodity.os.in_(['功能机'])):
        if 0 < commodity.price < 100:
            ppas = PhonePriceAndSales.get_by_id(9)
            ppas.total += commodity.total
            ppas.save()
        if 100 <= commodity.price < 200:
            ppas = PhonePriceAndSales.get_by_id(10)
            ppas.total += commodity.total
            ppas.save()
        if 200 <= commodity.price < 300:
            ppas = PhonePriceAndSales.get_by_id(11)
            ppas.total += commodity.total
            ppas.save()
        if 300 <= commodity.price < 400:
            ppas = PhonePriceAndSales.get_by_id(12)
            ppas.total += commodity.total
            ppas.save()
        if 400 <= commodity.price < 500:
            ppas = PhonePriceAndSales.get_by_id(13)
            ppas.total += commodity.total
            ppas.save()
        if 500 <= commodity.price < 1000:
            ppas = PhonePriceAndSales.get_by_id(14)
            ppas.total += commodity.total
            ppas.save()

    total_count = PhonePriceAndSales.select(fn.SUM(PhonePriceAndSales.total).alias('tc')) \
        .where(PhonePriceAndSales.type == '功能机').dicts()[0]['tc']
    print(total_count)
    for ppas in PhonePriceAndSales.select().where(PhonePriceAndSales.type == '功能机'):
        ppas.percentage = calculate_percentage(total_count, ppas.total)
        ppas.save()


# 生成智能手机在不同价格区间的品牌销量占比
def get_phone_price_and_brand():
    # for commodity in Commodity.select().where(Commodity.os.in_(['Android', 'iOS'])):
    #     if 0 < commodity.price < 2000:
    #         try:
    #             ppab = PhonePriceAndBrand.get(
    #                 PhonePriceAndBrand.price_range == '2000元以下',
    #                 PhonePriceAndBrand.brand == commodity.brand
    #             )
    #             ppab.total += commodity.total
    #             ppab.save()
    #         except PhonePriceAndBrand.DoesNotExist:
    #             PhonePriceAndBrand.create(
    #                 price_range='2000元以下',
    #                 brand=commodity.brand,
    #                 total=commodity.total
    #             )
    #     if 2000 <= commodity.price < 5000:
    #         try:
    #             ppab = PhonePriceAndBrand.get(
    #                 PhonePriceAndBrand.price_range == '2000-5000元',
    #                 PhonePriceAndBrand.brand == commodity.brand
    #             )
    #             ppab.total += commodity.total
    #             ppab.save()
    #         except PhonePriceAndBrand.DoesNotExist:
    #             PhonePriceAndBrand.create(
    #                 price_range='2000-5000元',
    #                 brand=commodity.brand,
    #                 total=commodity.total
    #             )
    #     if commodity.price >= 5000:
    #         try:
    #             ppab = PhonePriceAndBrand.get(
    #                 PhonePriceAndBrand.price_range == '5000元以上',
    #                 PhonePriceAndBrand.brand == commodity.brand
    #             )
    #             ppab.total += commodity.total
    #             ppab.save()
    #         except PhonePriceAndBrand.DoesNotExist:
    #             PhonePriceAndBrand.create(
    #                 price_range='5000元以上',
    #                 brand=commodity.brand,
    #                 total=commodity.total
    #             )
    range_list = ['2000元以下', '2000-5000元', '5000元以上']
    for pr in range_list:
        total_count = PhonePriceAndBrand.select(fn.SUM(PhonePriceAndBrand.total).alias('tc')) \
            .where(PhonePriceAndBrand.price_range == pr).dicts()[0]['tc']
        print(total_count)
        for ppab in PhonePriceAndBrand.select().where(PhonePriceAndBrand.price_range == pr):
            ppab.percentage = calculate_percentage(total_count, ppab.total)
            ppab.save()
            # if float(ppab.percentage) < 1:
            #     others = PhonePriceAndBrand.get(
            #         PhonePriceAndBrand.price_range == pr,
            #         PhonePriceAndBrand.brand == '其他品牌'
            #     )
            #     others.total += ppab.total
            #     others.save()
            #     ppab.delete_instance()


if __name__ == '__main__':
    # preprocess_data()
    # get_phone()
    # get_phone_total()
    # get_phone_platform()
    # get_phone_os()
    # get_brand_sales_star()
    # get_brand_percentage()
    # get_feature_phone_percentage()
    # get_soc()
    # get_soc_mfrs()
    # get_soc_star()
    # get_feature_phone_soc_percentage()
    # get_phone_size()
    # get_phone_price_and_sales()
    get_phone_price_and_brand()
