from time import strftime
from db.mi10_models import Comment, CommentSummary, ModelSummary
from db.mi10_analyze_models import (UserDeviceCount, Total, ModelCount, ColorCount, RamCount, RomCount)
from data_analyze.utils import calculate_percentage


# 计算安卓用户留存率和iOS用户转化率
def get_user_device_count():
    total = Comment.select().where(Comment.user_device.is_null(False)).count()
    android = Comment.select().where(Comment.user_device == 'Android').count()
    ios = Comment.select().where(Comment.user_device == 'iOS').count()
    other = Comment.select().where(Comment.user_device == 'other').count()
    android_percentage = calculate_percentage(total, android)
    ios_percentage = calculate_percentage(total, ios)
    other_percentage = calculate_percentage(total, other)

    UserDeviceCount.create(
        total=total,
        android=android,
        ios=ios,
        other=other,
        android_percentage=android_percentage,
        ios_percentage=ios_percentage,
        other_percentage=other_percentage
    )


# 简单处理一下评论统计总数
def get_total():
    get_jd_total()
    get_sn_total()
    get_mishop_total()


# 计算京东平台的评论统计总数
def get_jd_total():
    jd_comments_summary = CommentSummary.get(CommentSummary.source == '京东')
    jd_total = jd_comments_summary.default_good + jd_comments_summary.star_one + jd_comments_summary.star_two + \
               jd_comments_summary.star_three + jd_comments_summary.star_four + jd_comments_summary.star_five
    jd_good_count = jd_comments_summary.star_four + jd_comments_summary.star_five
    jd_general_cont = jd_comments_summary.star_two + jd_comments_summary.star_three
    jd_bad_count = jd_comments_summary.star_one
    jd_cal_total = jd_comments_summary.star_one + jd_comments_summary.star_two + jd_comments_summary.star_three + \
                   jd_comments_summary.star_four + jd_comments_summary.star_five
    jd_good_rate = calculate_percentage(jd_cal_total, jd_good_count)
    jd_models_total = 0
    for ms in ModelSummary.select().where(ModelSummary.source == '京东'):
        jd_models_total += ms.default_good + ms.star_one + ms.star_two + ms.star_three + ms.star_four + ms.star_five

    Total.create(
        source='京东',
        total=jd_total,
        all_models_total=jd_models_total,
        good_rate=jd_good_rate,
        default_good=jd_comments_summary.default_good,
        good_count=jd_good_count,
        general_count=jd_general_cont,
        bad_count=jd_bad_count,
        star_one=jd_comments_summary.star_one,
        star_two=jd_comments_summary.star_two,
        star_three=jd_comments_summary.star_three,
        star_four=jd_comments_summary.star_four,
        star_five=jd_comments_summary.star_five
    )


# 计算苏宁平台的评论统计总数
def get_sn_total():
    sn_comments_summary = CommentSummary.get(CommentSummary.source == '苏宁')
    sn_good_count = sn_comments_summary.star_four + sn_comments_summary.star_five
    sn_general_cont = sn_comments_summary.star_two + sn_comments_summary.star_three
    sn_bad_count = sn_comments_summary.star_one
    sn_models_total = 0
    for ms in ModelSummary.select().where(ModelSummary.source == '苏宁'):
        sn_models_total += ms.total

    Total.create(
        source='苏宁',
        total=sn_comments_summary.total,
        all_models_total=sn_models_total,
        good_rate=sn_comments_summary.good_rate,
        default_good=sn_comments_summary.default_good,
        good_count=sn_good_count,
        general_count=sn_general_cont,
        bad_count=sn_bad_count,
        star_one=sn_comments_summary.star_one,
        star_two=sn_comments_summary.star_two,
        star_three=sn_comments_summary.star_three,
        star_four=sn_comments_summary.star_four,
        star_five=sn_comments_summary.star_five
    )


# 计算小米商城的评论统计总数
def get_mishop_total():
    mishop_comments_summary = CommentSummary.get(CommentSummary.source == '小米商城')
    mishop_good_count = mishop_comments_summary.star_three + mishop_comments_summary.star_four + \
                        mishop_comments_summary.star_five
    mishop_general_cont = mishop_comments_summary.star_two
    mishop_bad_count = mishop_comments_summary.star_one

    Total.create(
        source='小米商城',
        total=mishop_comments_summary.total,
        all_models_total=mishop_comments_summary.total,
        good_rate=mishop_comments_summary.good_rate,
        default_good=mishop_comments_summary.default_good,
        good_count=mishop_good_count,
        general_count=mishop_general_cont,
        bad_count=mishop_bad_count,
        star_one=mishop_comments_summary.star_one,
        star_two=mishop_comments_summary.star_two,
        star_three=mishop_comments_summary.star_three,
        star_four=mishop_comments_summary.star_four,
        star_five=mishop_comments_summary.star_five
    )


# 计算各个型号的统计数据
def get_model_count():
    # 苏宁和京东数据合并
    all_color = ['国风雅灰', '钛银黑', '冰海蓝', '蜜桃金']
    all_ram = ['8GB', '12GB']
    all_rom = ['128GB', '256GB']
    for color in all_color:
        for ram in all_ram:
            for rom in all_rom:
                all_ms = ModelSummary.select().where(
                    (ModelSummary.product_color == color) &
                    (ModelSummary.product_ram == ram) &
                    (ModelSummary.product_rom == rom)
                )
                # 没有12GB+128GB的奇葩内存组合
                if len(all_ms) == 0:
                    continue
                mc = ModelCount.create(
                    product_color=color,
                    product_ram=ram,
                    product_rom=rom
                )
                for ms in all_ms:
                    if ms.source == '京东':
                        mc.total += ms.default_good + ms.star_one + ms.star_two + \
                                    ms.star_three + ms.star_four + ms.star_five
                        mc.cal_total += ms.star_one + ms.star_two + ms.star_three + ms.star_four + ms.star_five
                        mc.save()
                    if ms.source == '苏宁':
                        mc.total += ms.total
                        mc.cal_total += ms.total
                        mc.save()

                    mc.default_good += ms.default_good
                    mc.good_count += ms.star_four + ms.star_five
                    mc.general_count += ms.star_two + ms.star_three
                    mc.bad_count += ms.star_one
                    mc.star_one += ms.star_one
                    mc.star_two += ms.star_two
                    mc.star_three += ms.star_three
                    mc.star_four += ms.star_four
                    mc.star_five += ms.star_five
                    mc.save()

    # 计算占比和好评率 (京东计算规则)
    jd_total = Total.get(Total.source == '京东')
    sn_total = Total.get(Total.source == '苏宁')
    models_total = jd_total.all_models_total + sn_total.all_models_total
    for mc in ModelCount.select():
        mc.percentage = calculate_percentage(models_total, mc.total)
        mc.good_rate = calculate_percentage(mc.cal_total, mc.good_count)
        mc.save()


# 计算不同颜色的统计数据
def get_color_count():
    jd_total = Total.get(Total.source == '京东')
    sn_total = Total.get(Total.source == '苏宁')
    models_total = jd_total.all_models_total + sn_total.all_models_total

    all_color = ['国风雅灰', '钛银黑', '冰海蓝', '蜜桃金']
    for color in all_color:
        color_total = color_cal_total = color_default_good = 0
        color_good_count = color_general_count = color_bad_count = 0
        color_star_one = color_star_two = color_star_three = 0
        color_star_four = color_star_five = 0

        all_mc = ModelCount.select().where(ModelCount.product_color == color)
        for mc in all_mc:
            color_total += mc.total
            color_cal_total += mc.cal_total
            color_default_good += mc.default_good
            color_good_count += mc.good_count
            color_general_count += mc.general_count
            color_bad_count += mc.bad_count
            color_star_one += mc.star_one
            color_star_two += mc.star_two
            color_star_three += mc.star_three
            color_star_four += mc.star_four
            color_star_five += mc.star_five

        ColorCount.create(
            product_color=color,
            total=color_total,
            percentage=calculate_percentage(models_total, color_total),
            cal_total=color_cal_total,
            good_rate=calculate_percentage(color_cal_total, color_good_count),
            default_good=color_default_good,
            good_count=color_good_count,
            general_count=color_general_count,
            bad_count=color_bad_count,
            star_one=color_star_one,
            star_two=color_star_two,
            star_three=color_star_three,
            star_four=color_star_four,
            star_five=color_star_five
        )


# 计算不同内存的统计数据
def get_ram_count():
    jd_total = Total.get(Total.source == '京东')
    sn_total = Total.get(Total.source == '苏宁')
    models_total = jd_total.all_models_total + sn_total.all_models_total

    all_ram = ['8GB', '12GB']
    for ram in all_ram:
        ram_total = ram_cal_total = ram_default_good = 0
        ram_good_count = ram_general_count = ram_bad_count = 0
        ram_star_one = ram_star_two = ram_star_three = 0
        ram_star_four = ram_star_five = 0

        all_mc = ModelCount.select().where(ModelCount.product_ram == ram)
        for mc in all_mc:
            ram_total += mc.total
            ram_cal_total += mc.cal_total
            ram_default_good += mc.default_good
            ram_good_count += mc.good_count
            ram_general_count += mc.general_count
            ram_bad_count += mc.bad_count
            ram_star_one += mc.star_one
            ram_star_two += mc.star_two
            ram_star_three += mc.star_three
            ram_star_four += mc.star_four
            ram_star_five += mc.star_five

        RamCount.create(
            product_ram=ram,
            total=ram_total,
            percentage=calculate_percentage(models_total, ram_total),
            cal_total=ram_cal_total,
            good_rate=calculate_percentage(ram_cal_total, ram_good_count),
            default_good=ram_default_good,
            good_count=ram_good_count,
            general_count=ram_general_count,
            bad_count=ram_bad_count,
            star_one=ram_star_one,
            star_two=ram_star_two,
            star_three=ram_star_three,
            star_four=ram_star_four,
            star_five=ram_star_five
        )


# 计算不同储存的统计数据
def get_rom_count():
    jd_total = Total.get(Total.source == '京东')
    sn_total = Total.get(Total.source == '苏宁')
    models_total = jd_total.all_models_total + sn_total.all_models_total

    all_rom = ['128GB', '256GB']
    for rom in all_rom:
        rom_total = rom_cal_total = rom_default_good = 0
        rom_good_count = rom_general_count = rom_bad_count = 0
        rom_star_one = rom_star_two = rom_star_three = 0
        rom_star_four = rom_star_five = 0

        all_mc = ModelCount.select().where(ModelCount.product_rom == rom)
        for mc in all_mc:
            rom_total += mc.total
            rom_cal_total += mc.cal_total
            rom_default_good += mc.default_good
            rom_good_count += mc.good_count
            rom_general_count += mc.general_count
            rom_bad_count += mc.bad_count
            rom_star_one += mc.star_one
            rom_star_two += mc.star_two
            rom_star_three += mc.star_three
            rom_star_four += mc.star_four
            rom_star_five += mc.star_five

        RomCount.create(
            product_rom=rom,
            total=rom_total,
            percentage=calculate_percentage(models_total, rom_total),
            cal_total=rom_cal_total,
            good_rate=calculate_percentage(rom_cal_total, rom_good_count),
            default_good=rom_default_good,
            good_count=rom_good_count,
            general_count=rom_general_count,
            bad_count=rom_bad_count,
            star_one=rom_star_one,
            star_two=rom_star_two,
            star_three=rom_star_three,
            star_four=rom_star_four,
            star_five=rom_star_five
        )


# 统计用户评论时间分布 (月度)
def get_comment_date_count():
    comment = Comment.get_by_id('SN810521815')
    year_month = str(comment.create_time)[0:7]
    print(year_month, type(year_month))


if __name__ == '__main__':
    # get_user_device_count()
    # get_total()
    # get_model_count()
    # get_color_count()
    # get_ram_count()
    # get_rom_count()
    get_comment_date_count()
