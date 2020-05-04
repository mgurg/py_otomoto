from . import db

class posty(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Nazwa = db.Column(db.String(30))
    Tresc = db.Column(db.String(64))
    Autor = db.Column(db.String(64))
