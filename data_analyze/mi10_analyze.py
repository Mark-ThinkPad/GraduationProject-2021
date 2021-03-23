from db.mi10_models import Comment, CommentSummary, ModelSummary
from db.mi10_analyze_models import UserDeviceCount, Total
from data_analyze.utils import calculate_percentage


# 分析安卓用户留存率和iOS用户转化率
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
                for ms in all_ms:
                    if ms.source == '京东':
                        pass
                    if ms.source == '苏宁':
                        pass


if __name__ == '__main__':
    # get_user_device_count()
    # get_total()
    get_model_count()
