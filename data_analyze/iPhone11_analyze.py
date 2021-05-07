import jieba.analyse
from conf.settings import DATA_ANALYZE_DIR
from data_analyze.utils import calculate_percentage
from db.iPhone11_models import Comment, CommentSummary, ModelSummary
from db.iPhone11_analyze_models import (UserDeviceCount, Total, ModelCount, ColorCount, RomCount, CommentDateCount,
                                        AfterDaysCount, OrderDateCount, OrderDaysCount, UserActivity, AllCommentsWords,
                                        AfterCommentsWords, IosCommentsWords, NonFiveStarCommentsWords)


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


# 计算京东平台的评论统计总数
def get_jd_total():
    jd_total = 0
    jd_good_count = 0
    jd_general_count = 0
    jd_bad_count = 0
    jd_cal_total = 0
    jd_default_good = 0
    jd_star_one = 0
    jd_star_two = 0
    jd_star_three = 0
    jd_star_four = 0
    jd_star_five = 0
    for jd_comments_summary in CommentSummary.select().where(CommentSummary.source == '京东'):
        jd_total += jd_comments_summary.default_good + jd_comments_summary.star_one + jd_comments_summary.star_two + \
                    jd_comments_summary.star_three + jd_comments_summary.star_four + jd_comments_summary.star_five
        jd_good_count += jd_comments_summary.star_four + jd_comments_summary.star_five
        jd_general_count += jd_comments_summary.star_two + jd_comments_summary.star_three
        jd_bad_count += jd_comments_summary.star_one
        jd_cal_total += jd_comments_summary.star_one + jd_comments_summary.star_two + jd_comments_summary.star_three + \
                        jd_comments_summary.star_four + jd_comments_summary.star_five
        jd_default_good += jd_comments_summary.default_good
        jd_star_one += jd_comments_summary.star_one
        jd_star_two += jd_comments_summary.star_two
        jd_star_three += jd_comments_summary.star_three
        jd_star_four += jd_comments_summary.star_four
        jd_star_five += jd_comments_summary.star_five

    jd_good_rate = calculate_percentage(jd_cal_total, jd_good_count)

    jd_models_total = 0
    for ms in ModelSummary.select().where(ModelSummary.source == '京东'):
        jd_models_total += ms.default_good + ms.star_one + ms.star_two + ms.star_three + ms.star_four + ms.star_five

    Total.create(
        source='京东',
        total=jd_total,
        all_models_total=jd_models_total,
        good_rate=jd_good_rate,
        default_good=jd_default_good,
        good_count=jd_good_count,
        general_count=jd_general_count,
        bad_count=jd_bad_count,
        star_one=jd_star_one,
        star_two=jd_star_two,
        star_three=jd_star_three,
        star_four=jd_star_four,
        star_five=jd_star_five
    )


# 计算苏宁平台的评论统计总数
def get_sn_total():
    sn_good_count = 0
    sn_general_count = 0
    sn_bad_count = 0
    sn_total = 0
    sn_default_good = 0
    sn_star_one = 0
    sn_star_two = 0
    sn_star_three = 0
    sn_star_four = 0
    sn_star_five = 0
    for sn_comments_summary in CommentSummary.select().where(CommentSummary.source == '苏宁'):
        sn_good_count += sn_comments_summary.star_four + sn_comments_summary.star_five
        sn_general_count += sn_comments_summary.star_two + sn_comments_summary.star_three
        sn_bad_count += sn_comments_summary.star_one
        sn_total += sn_comments_summary.total
        sn_default_good += sn_comments_summary.default_good
        sn_star_one += sn_comments_summary.star_one
        sn_star_two += sn_comments_summary.star_two
        sn_star_three += sn_comments_summary.star_three
        sn_star_four += sn_comments_summary.star_four
        sn_star_five += sn_comments_summary.star_five

    sn_cal_total = sn_good_count + sn_general_count + sn_bad_count
    sn_good_rate = calculate_percentage(sn_cal_total, sn_good_count)

    sn_models_total = 0
    for ms in ModelSummary.select().where(ModelSummary.source == '苏宁'):
        sn_models_total += ms.total

    Total.create(
        source='苏宁',
        total=sn_total,
        all_models_total=sn_models_total,
        good_rate=sn_good_rate,
        default_good=sn_default_good,
        good_count=sn_good_count,
        general_count=sn_general_count,
        bad_count=sn_bad_count,
        star_one=sn_star_one,
        star_two=sn_star_two,
        star_three=sn_star_three,
        star_four=sn_star_four,
        star_five=sn_star_five
    )


# 计算各个型号的统计数据
def get_model_count():
    # 苏宁和京东数据合并
    all_color = ['黑色', '白色', '红色', '黄色', '紫色', '绿色']
    all_rom = ['64GB', '128GB', '256GB']
    for color in all_color:
        for rom in all_rom:
            all_ms = ModelSummary.select().where(
                (ModelSummary.color == color) &
                (ModelSummary.rom == rom)
            )
            mc = ModelCount.create(
                color=color,
                rom=rom
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

    all_color = ['黑色', '白色', '红色', '黄色', '紫色', '绿色']
    for color in all_color:
        color_total = 0
        color_cal_total = 0
        color_default_good = 0
        color_good_count = 0
        color_general_count = 0
        color_bad_count = 0
        color_star_one = 0
        color_star_two = 0
        color_star_three = 0
        color_star_four = 0
        color_star_five = 0

        all_mc = ModelCount.select().where(ModelCount.color == color)
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
            color=color,
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


# 计算不同储存的统计数据
def get_rom_count():
    jd_total = Total.get(Total.source == '京东')
    sn_total = Total.get(Total.source == '苏宁')
    models_total = jd_total.all_models_total + sn_total.all_models_total

    all_rom = ['64GB', '128GB', '256GB']
    for rom in all_rom:
        rom_total = 0
        rom_cal_total = 0
        rom_default_good = 0
        rom_good_count = 0
        rom_general_count = 0
        rom_bad_count = 0
        rom_star_one = 0
        rom_star_two = 0
        rom_star_three = 0
        rom_star_four = 0
        rom_star_five = 0

        all_mc = ModelCount.select().where(ModelCount.rom == rom)
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
            rom=rom,
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
    for comment in Comment.select():
        year_month = str(comment.create_time)[0:7]
        try:
            cdc = CommentDateCount.get_by_id(year_month)
            cdc.total += 1
            cdc.save()
        except CommentDateCount.DoesNotExist:
            CommentDateCount.create(
                year_month=year_month,
                total=1
            )

    comments_total = Comment.select().count()
    for cdc in CommentDateCount.select():
        cdc.percentage = calculate_percentage(comments_total, cdc.total)
        cdc.save()


# 统计追评间隔时间分布
def get_after_days_count():
    for comment in Comment.select().where(Comment.after_days.is_null(False)):
        after_days = comment.after_days
        try:
            adc = AfterDaysCount.get_by_id(after_days)
            adc.total += 1
            adc.save()
        except AfterDaysCount.DoesNotExist:
            AfterDaysCount.create(
                after_days=after_days,
                total=1
            )

    after_total = Comment.select().where(Comment.after_days.is_null(False)).count()
    for adc in AfterDaysCount.select():
        adc.percentage = calculate_percentage(after_total, adc.total)
        adc.save()


# 统计用户下单时间分布 (月度) (仅限京东数据源)
def get_order_date_count():
    for comment in Comment.select().where(Comment.order_time.is_null(False)):
        year_month = str(comment.order_time)[0:7]
        try:
            odc = OrderDateCount.get_by_id(year_month)
            odc.total += 1
            odc.save()
        except OrderDateCount.DoesNotExist:
            OrderDateCount.create(
                year_month=year_month,
                total=1
            )

    order_total = Comment.select().where(Comment.order_time.is_null(False)).count()
    for odc in OrderDateCount.select():
        odc.percentage = calculate_percentage(order_total, odc.total)
        odc.save()


# 统计用户下单到评论的间隔时间 (仅限京东数据源)
def get_order_days_count():
    for comment in Comment.select().where(Comment.order_days.is_null(False)):
        order_days = comment.order_days
        try:
            odc = OrderDaysCount.get_by_id(order_days)
            odc.total += 1
            odc.save()
        except OrderDaysCount.DoesNotExist:
            OrderDaysCount.create(
                order_days=order_days,
                total=1
            )

    order_total = Comment.select().where(Comment.order_days.is_null(False)).count()
    for odc in OrderDaysCount.select():
        odc.percentage = calculate_percentage(order_total, odc.total)
        odc.save()


# 计算用户活跃度 (基于非默认好评数量)
def get_user_activity():
    for platform in Total.select():
        UserActivity.create(
            source=platform.source,
            total=platform.total,
            active_count=platform.total - platform.default_good,
            active_percentage=calculate_percentage(platform.total, platform.total - platform.default_good),
            inactive_count=platform.default_good,
            inactive_percentage=calculate_percentage(platform.total, platform.default_good)
        )


# 提取所有评论中提取的高频词 (不包括追评)
def get_all_comments_words():
    content = ''
    for comment in Comment.select():
        content += comment.content + '\n'
    # 基于TF-IDF算法的关键词抽取
    jieba.analyse.set_stop_words(DATA_ANALYZE_DIR + '/custom_cn_stopwords.txt')
    tags = jieba.analyse.extract_tags(content, topK=200)
    for tag in tags:
        AllCommentsWords.create(word=tag)


# 提取追评中的高频词
def get_after_comments_words():
    content = ''
    for comment in Comment.select().where(Comment.after_content.is_null(False)):
        content += comment.after_content + '\n'
    # 基于TF-IDF算法的关键词抽取
    jieba.analyse.set_stop_words(DATA_ANALYZE_DIR + '/custom_cn_stopwords.txt')
    tags = jieba.analyse.extract_tags(content, topK=200)
    for tag in tags:
        AfterCommentsWords.create(word=tag)


# 提取iOS转化用户评论高频词
def get_ios_comments_words():
    content = ''
    for comment in Comment.select().where(Comment.user_device == 'iOS'):
        content += comment.content + '\n'
        if comment.after_content is not None:
            content += comment.after_content + '\n'
    # 基于TF-IDF算法的关键词抽取
    jieba.analyse.set_stop_words(DATA_ANALYZE_DIR + '/custom_cn_stopwords.txt')
    tags = jieba.analyse.extract_tags(content, topK=200)
    for tag in tags:
        IosCommentsWords.create(word=tag)


# 提取评分五星以下评论的高频词
def get_non_five_star_comments_words():
    content = ''
    for comment in Comment.select().where((Comment.star.in_([1, 2, 3, 4]))):
        content += comment.content + '\n'
        if comment.after_content is not None:
            content += comment.after_content + '\n'
    # 基于TF-IDF算法的关键词抽取
    jieba.analyse.set_stop_words(DATA_ANALYZE_DIR + '/custom_cn_stopwords.txt')
    tags = jieba.analyse.extract_tags(content, topK=200)
    for tag in tags:
        NonFiveStarCommentsWords.create(word=tag)


if __name__ == '__main__':
    # get_user_device_count()
    # get_total()
    # get_model_count()
    get_color_count()
    get_rom_count()
    # get_comment_date_count()
    # get_after_days_count()
    # get_order_date_count()
    # get_order_days_count()
    # get_user_activity()
    # get_all_comments_words()
    # get_after_comments_words()
    # get_ios_comments_words()
    # get_non_five_star_comments_words()
