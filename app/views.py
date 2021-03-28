from flask import Blueprint, render_template

views = Blueprint('views', __name__)


@views.route('/mi10')
def mi10():
    return render_template('mi10.html')
