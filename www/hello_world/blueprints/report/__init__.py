from flask import render_template
from flask import Blueprint

report_blueprint = Blueprint('report_blueprint', __name__)

@report_blueprint.route('/report')
def report():

    return render_template('report.html')