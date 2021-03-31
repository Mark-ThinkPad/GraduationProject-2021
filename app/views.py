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
    # 数据源总览
    total_source = []
    total_count = []
    for platform in Total.select():
        total_source.append(platform.source)
        total_count.append(platform.total)
    return render_template('mi10.html', total_source=total_source, total_count=total_count)
