from flask import Blueprint, render_template, redirect, url_for
from db.mi10_analyze_models import (UserDeviceCount, Total, ModelCount, ColorCount, RamCount, RomCount,
                                    CommentDateCount, AfterDaysCount, OrderDateCount, OrderDaysCount, UserActivity,
                                    AllCommentsWords, AfterCommentsWords, IosCommentsWords, NonFiveStarCommentsWords)

views = Blueprint('views', __name__)


@views.route('/')
def index():
    return redirect(url_for('views.mi10'))


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
