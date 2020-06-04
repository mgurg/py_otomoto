"""Logged-in page routes."""
from flask import Blueprint, render_template, make_response, redirect, url_for
from flask_login import current_user, login_required, logout_user


# Blueprint Configuration
main_bp = Blueprint('main_bp', __name__,
                    template_folder='templates',
                    static_folder='static')

@main_bp.route("/")
def hello():
    return render_template('index.html')


@main_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """Logged-in User Dashboard."""
    return render_template('dashboard.html',
                           title='Flask-Login Tutorial.',
                           template='dashboard-template',
                           current_user=current_user,
                           body="You are now logged in!")


@main_bp.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth_bp.login'))

@main_bp.app_errorhandler(404)
def not_found(error):
    return make_response(render_template('404.html'), 404)

@main_bp.app_errorhandler(500)
def internal_error(error):
    return render_template('500.html')
