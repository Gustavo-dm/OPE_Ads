from flask import Flask
from db import db


def create_app(): 
    app = Flask(__name__)
    app.secret_key = 'askjdnaskjdnaksjdn'
    app.config['SESSION_TYPE'] = 'memcached'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///arquesys.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app