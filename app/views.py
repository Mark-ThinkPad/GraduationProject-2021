from flask import Blueprint, render_template, redirect, url_for
from db.mi10_analyze_models import (UserDeviceCount, Total, ModelCount, ColorCount, RamCount, RomCount,
                                    CommentDateCount, AfterDaysCount, OrderDateCount, OrderDaysCount, UserActivity)
from db.phone_sales_analyze_models import (Phone, PhoneTotal, PhonePlatform, PhoneOS, PhoneBrand, BrandSalesStar,
                                           BrandPercentage, FeaturePhonePercentage, SoC, SoCMfrs, SoCStar,
                                           FeaturePhoneSoCPer, PhoneSize, PhonePriceAndSales, PhonePriceAndBrand)

views = Blueprint('views', __name__)


@views.route('/')
def index():
    return redirect(url_for('views.phone'))


@views.route('/phone')
def phone():
    # 手机销量排行
    phone_name = []
    phone_count = []
    for item in Phone.select().order_by(Phone.total.asc()):
        phone_name.append(item.brand + '\n' + item.model)
        phone_count.append(item.total)
    # 数据总览
    total = PhoneTotal.get_by_id(1)
    # 平台数据源概览
    platform_source = []
    platform_tc = []
    platform_cc = []
    platform_sp = []
    platform_nsp = []
    for platform in PhonePlatform.select():
        platform_source.append(platform.source)
        platform_tc.append(platform.total_count)
        platform_cc.append(platform.commodity_count)
        platform_sp.append(float(platform.self_percentage))
        platform_nsp.append(float(platform.non_self_percentage))
    # 操作系统占比
    phoneos = []
    for phone_os in PhoneOS.select():
        phoneos.append({'value': float(phone_os.percentage), 'name': phone_os.os})
    # 品牌销量占比
    phonebrand = []
    for phone_brand in PhoneBrand.select():
        phonebrand.append({'value': float(phone_brand.percentage), 'name': phone_brand.brand})
    # 苹果手机销量明星
    apple_model = []
    apple_mt = []
    for bss in BrandSalesStar.select().where(BrandSalesStar.brand == '苹果') \
            .order_by(BrandSalesStar.total.desc()):
        apple_model.append(bss.model)
        apple_mt.append(bss.total)
    # 小米手机销量明星
    mi_model = []
    mi_mt = []
    for bss in BrandSalesStar.select().where(BrandSalesStar.brand == '小米') \
            .order_by(BrandSalesStar.total.desc()):
        mi_model.append(bss.model)
        mi_mt.append(bss.total)
    # 华为手机销量明星
    hw_model = []
    hw_mt = []
    for bss in BrandSalesStar.select().where(BrandSalesStar.brand == '华为') \
            .order_by(BrandSalesStar.total.desc()):
        hw_model.append(bss.model)
        hw_mt.append(bss.total)
    # 荣耀手机销量明星
    honor_model = []
    honor_mt = []
    for bss in BrandSalesStar.select().where(BrandSalesStar.brand == '荣耀') \
            .order_by(BrandSalesStar.total.desc()):
        honor_model.append(bss.model)
        honor_mt.append(bss.total)
    # OPPO手机销量明星
    oppo_model = []
    oppo_mt = []
    for bss in BrandSalesStar.select().where(BrandSalesStar.brand == 'OPPO') \
            .order_by(BrandSalesStar.total.desc()):
        oppo_model.append(bss.model)
        oppo_mt.append(bss.total)
    # vivo手机销量明星
    vivo_model = []
    vivo_mt = []
    for bss in BrandSalesStar.select().where(BrandSalesStar.brand == 'vivo') \
            .order_by(BrandSalesStar.total.desc()):
        vivo_model.append(bss.model)
        vivo_mt.append(bss.total)
    # 小米与子品牌红米销量占比
    mi_per = []
    for bp in BrandPercentage.select().where(BrandPercentage.main_brand == '小米'):
        mi_per.append({'value': float(bp.percentage), 'name': bp.sub_brand})
    # vivo与子品牌iQOO销量占比
    vivo_per = []
    for bp in BrandPercentage.select().where(BrandPercentage.main_brand == 'vivo'):
        vivo_per.append({'value': float(bp.percentage), 'name': bp.sub_brand})
    # OPPO与子品牌realme和一加的销量占比
    oppo_per = []
    for bp in BrandPercentage.select().where(BrandPercentage.main_brand == 'OPPO'):
        oppo_per.append({'value': float(bp.percentage), 'name': bp.sub_brand})
    # 功能机品牌占比
    fpp = []
    for fp in FeaturePhonePercentage.select():
        fpp.append({'value': float(fp.percentage), 'name': fp.brand})
    # SoC销量排行
    soc_name = []
    soc_count = []
    for soc in SoC.select().order_by(SoC.total.asc()):
        soc_name.append(soc.soc_mfrs + '\n' + soc.soc_model)
        soc_count.append(soc.total)
    # SoC制造商占比
    socmfrs = []
    for soc_mfrs in SoCMfrs.select():
        socmfrs.append({'value': float(soc_mfrs.percentage), 'name': soc_mfrs.soc_mfrs})
    # 苹果A系列SoC销量明星
    as_model = []
    as_mt = []
    for soc in SoCStar.select().where(SoCStar.soc_mfrs == '苹果(A系列)').order_by(SoCStar.total.desc()):
        as_model.append(soc.soc_model)
        as_mt.append(soc.total)
    # 紫光展锐SoC销量明星
    unisoc_model = []
    unisoc_mt = []
    for soc in SoCStar.select().where(SoCStar.soc_mfrs == '紫光展锐').order_by(SoCStar.total.desc()):
        unisoc_model.append(soc.soc_model)
        unisoc_mt.append(soc.total)
    # 三星猎户座SoC销量明星
    exynos_model = []
    exynos_mt = []
    for soc in SoCStar.select().where(SoCStar.soc_mfrs == '三星猎户座').order_by(SoCStar.total.desc()):
        exynos_model.append(soc.soc_model)
        exynos_mt.append(soc.total)
    # 高通骁龙SoC销量明星
    snapdragon_model = []
    snapdragon_mt = []
    for soc in SoCStar.select().where(SoCStar.soc_mfrs == '高通骁龙').order_by(SoCStar.total.desc()):
        snapdragon_model.append(soc.soc_model)
        snapdragon_mt.append(soc.total)
    # 海思麒麟SoC销量明星
    kirin_model = []
    kirin_mt = []
    for soc in SoCStar.select().where(SoCStar.soc_mfrs == '海思麒麟').order_by(SoCStar.total.desc()):
        kirin_model.append(soc.soc_model)
        kirin_mt.append(soc.total)
    # 联发科SoC销量明星
    mtk_model = []
    mtk_mt = []
    for soc in SoCStar.select().where(SoCStar.soc_mfrs == '联发科').order_by(SoCStar.total.desc()):
        mtk_model.append(soc.soc_model)
        mtk_mt.append(soc.total)
    # 功能机SoC制造商占比
    fpsp = []
    for fps in FeaturePhoneSoCPer.select():
        fpsp.append({'value': float(fps.percentage), 'name': fps.soc_mfrs})
    # 智能手机各项尺寸参数的平均数和中位数
    phone_size = PhoneSize.get_by_id(1)
    # 智能手机与功能机价格区间与销量分布
    ppas_sp = []
    for ppas in PhonePriceAndSales.select().where(PhonePriceAndSales.type == '智能手机'):
        ppas_sp.append({'value': float(ppas.percentage), 'name': ppas.price_range})
    ppas_fp = []
    for ppas in PhonePriceAndSales.select().where(PhonePriceAndSales.type == '功能机'):
        ppas_fp.append({'value': float(ppas.percentage), 'name': ppas.price_range})
    # 智能手机在不同价格区间的品牌销量占比
    ppab_b2k = []
    for ppab in PhonePriceAndBrand.select().where(PhonePriceAndBrand.price_range == '2000元以下'):
        ppab_b2k.append({'value': float(ppab.percentage), 'name': ppab.brand})
    ppab_2kto5k = []
    for ppab in PhonePriceAndBrand.select().where(PhonePriceAndBrand.price_range == '2000-5000元'):
        ppab_2kto5k.append({'value': float(ppab.percentage), 'name': ppab.brand})
    ppab_a5k = []
    for ppab in PhonePriceAndBrand.select().where(PhonePriceAndBrand.price_range == '5000元以上'):
        ppab_a5k.append({'value': float(ppab.percentage), 'name': ppab.brand})

    return render_template('phone.html', phone_name=phone_name, phone_count=phone_count, total=total,
                           platform_source=platform_source, platform_tc=platform_tc, platform_cc=platform_cc,
                           platform_sp=platform_sp, platform_nsp=platform_nsp, phone_os=phoneos, phone_brand=phonebrand,
                           apple_model=apple_model, apple_mt=apple_mt, mi_model=mi_model, mi_mt=mi_mt,
                           hw_model=hw_model, hw_mt=hw_mt, honor_model=honor_model, honor_mt=honor_mt,
                           oppo_model=oppo_model, oppo_mt=oppo_mt, vivo_model=vivo_model, vivo_mt=vivo_mt,
                           mi_per=mi_per, vivo_per=vivo_per, oppo_per=oppo_per, fpp=fpp, soc_name=soc_name,
                           soc_count=soc_count, soc_mfrs=socmfrs, as_model=as_model, as_mt=as_mt,
                           unisoc_model=unisoc_model, unisoc_mt=unisoc_mt, exynos_model=exynos_model,
                           exynos_mt=exynos_mt, snapdragon_model=snapdragon_model, snapdragon_mt=snapdragon_mt,
                           kirin_model=kirin_model, kirin_mt=kirin_mt, mtk_model=mtk_model, mtk_mt=mtk_mt, fpsp=fpsp,
                           phone_size=phone_size, ppas_sp=ppas_sp, ppas_fp=ppas_fp, ppab_b2k=ppab_b2k,
                           ppab_2kto5k=ppab_2kto5k, ppab_a5k=ppab_a5k)


@views.route('/phone/mi10')
def mi10():
    # 电商平台数据源概览
    total_source = []
    total_count = []
    total_good_rate = []
    for platform in Total.select():
        total_source.append(platform.source)
        total_count.append(platform.total)
        total_good_rate.append(float(platform.good_rate))
    # 各型号数据概览
    mc_name = []
    mc_per = []
    mc_good_rate = []
    for model in ModelCount.select():
        mc_name.append(model.product_color + '\n' + model.product_ram + '+' + model.product_rom)
        mc_per.append(model.percentage)
        mc_good_rate.append(float(model.good_rate))
    # 机身颜色百分比
    color_count = []
    for cc in ColorCount.select():
        color_count.append({'value': float(cc.percentage), 'name': cc.product_color})
    # 内存容量百分比
    ram_count = []
    for rac in RamCount.select():
        ram_count.append({'value': float(rac.percentage), 'name': rac.product_ram})
    # 储存容量百分比
    rom_count = []
    for roc in RomCount.select():
        rom_count.append({'value': float(roc.percentage), 'name': roc.product_rom})
    # 用户活跃度百分比
    ua_source = []
    ua_ap = []
    ua_iap = []
    for ua in UserActivity.select():
        ua_source.append(ua.source)
        ua_ap.append(float(ua.active_percentage))
        ua_iap.append(float(ua.inactive_percentage))
    # 用户评论时间分布
    cdc_ym = []
    cdc_per = []
    for cdc in CommentDateCount.select().order_by(CommentDateCount.year_month.asc()):
        cdc_ym.append(cdc.year_month)
        cdc_per.append(float(cdc.percentage))
    # 用户下单时间分布
    odc_ym = []
    odc_per = []
    for odc in OrderDateCount.select().order_by(OrderDateCount.year_month.asc()):
        odc_ym.append(odc.year_month)
        odc_per.append(float(odc.percentage))
    # 从下单到评论的时间间隔分布
    odsc_days = []
    odsc_per = []
    for odsc in OrderDaysCount.select():
        odsc_days.append(odsc.order_days)
        odsc_per.append(float(odsc.percentage))
    # 追评时间间隔分布
    adc_days = []
    adc_per = []
    for adc in AfterDaysCount.select():
        adc_days.append(adc.after_days)
        adc_per.append(adc.percentage)
    # 用户设备类型统计
    udc_system = []
    udc_per = []
    for udc in UserDeviceCount.select():
        udc_system += ['Android 留存用户', 'iOS 转化用户', 'other']
        udc_per += [udc.android_percentage, udc.ios_percentage, udc.other_percentage]

    return render_template('mi10.html', total_source=total_source, total_count=total_count,
                           total_good_rate=total_good_rate, mc_name=mc_name, mc_per=mc_per, mc_good_rate=mc_good_rate,
                           color_count=color_count, ram_count=ram_count, rom_count=rom_count, ua_source=ua_source,
                           ua_ap=ua_ap, ua_iap=ua_iap, cdc_ym=cdc_ym, cdc_per=cdc_per, odc_ym=odc_ym, odc_per=odc_per,
                           odsc_days=odsc_days, odsc_per=odsc_per, adc_days=adc_days, adc_per=adc_per, udc_per=udc_per,
                           udc_system=udc_system)
