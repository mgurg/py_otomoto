from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import yaml

with open('./hello_world/config.yml', 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)

app = Flask(__name__)
#app.config['DEBUG'] = True
app.config['DEBUG'] = False
app.config['SECRET_KEY'] = cfg['flask']['wtf_password']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+cfg['db']['settings']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from hello_world import views