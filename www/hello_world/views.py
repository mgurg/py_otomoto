from hello_world import app
from hello_world import db
from flask import render_template, flash

from .blueprints.report import report_blueprint
app.register_blueprint(report_blueprint)

from .models import posty
from .forms import CarForm

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/report')
# def report():
#     return render_template('report.html')

@app.route('/pricing', methods=['GET', 'POST'])
def form():
    form = CarForm()
    if form.validate_on_submit():
        year = int(form.year.data)
        mileage = int(form.mileage.data)

        feat_dict =	{
            "air_conditioning": form.air_conditioning.data,
            "front_electric_windows": form.front_electric_windows.data,
            }

        features = [form.air_conditioning.data, form.front_electric_windows.data]
        price = year + mileage

        flash('Wartość samochodu: {}, AC: {}'.format(price, form.air_conditioning.data))
    return render_template('price_predict.html', form=form)

@app.route('/posts')
def posts():
    return render_template('posts.html')

@app.route('/post/<int:post_id>')
def post(post_id):
    return render_template('post.html', post_id = post_id)

@app.route("/all-posts")
def database_posts():
    data = posty.query.all()
    for user in data:
        print(user.ID, user.Nazwa)
    data = [('1','N1','TXT1','A1'),
            ('2','N2','TXT2','A2'),
            ('3','N3','TXT3','A3')]
    return render_template('database_posts.html', data = data)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html')

@app.context_processor
def inject_variables():
    return dict(
        user = {'name': 'Alicja'},
        posts = [
        {
            'post_id': 0,
            'title': 'Post numer 0'
        },
        {
            'post_id': 1,
            'title': 'Post numer 1'
        },
        {
            'post_id': 2,
            'title': 'Post numer 2'
        }],
        # navigation = [
        #     {
        #         'href': '/',
        #         'caption': 'Home'
        #     },
        #     {
        #         'href': 'report',
        #         'caption': 'Analiza ogłoszeń'
        #     },
        #     {
        #         'href': 'price_predict',
        #         'caption': 'Predykcja ceny'
        #     # },
        #     # {
        #     #     'href': 'post',
        #     #     'caption': 'Posty'
        #     # },
        #     # {
        #     #     'href': 'all-posts',
        #     #     'caption': 'Posty z DB'
        #     }
        # ]
        )

