from db.mi10_models import Comment, CommentSummary, ModelSummary
from db.mi10_analyze_models import UserDeviceSummary
from data_analyze.utils import calculate_percentage


# 分析安卓用户留存率和iOS用户转化率
def get_user_device_summary():
    total = Comment.select().where(Comment.user_device.is_null(False)).count()
    android = Comment.select().where(Comment.user_device == 'Android').count()
    ios = Comment.select().where(Comment.user_device == 'iOS').count()
    other = Comment.select().where(Comment.user_device == 'other').count()
    android_percentage = calculate_percentage(total, android)
    ios_percentage = calculate_percentage(total, ios)
    other_percentage = calculate_percentage(total, other)

    UserDeviceSummary.create(
        total=total,
        android=android,
        ios=ios,
        other=other,
        android_percentage=android_percentage,
        ios_percentage=ios_percentage,
        other_percentage=other_percentage
    )


# 简单处理一下统计总数
def get_total():
    total = 0
    for ms in ModelSummary.select().where(ModelSummary.source == '京东'):
        total += ms.default_good + ms.star_one + ms.star_two + ms.star_three + ms.star_four + ms.star_five
    print(total)


if __name__ == '__main__':
    get_total()
