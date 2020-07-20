from flask import Flask, url_for, redirect
from flask_migrate import Migrate

from webapp.db import db

# imports from resource
from webapp.auth.views import blueprint as auth_blueprint
from webapp.auth.models import Guest
from webapp.reservation.models import Table, Reservation


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    # db starting
    db.init_app(app)
    migrate = Migrate(app, db)

    # Blueprint register
    app.register_blueprint(auth_blueprint)

    @app.route('/')
    def main():
        return redirect(url_for('auth.user_auth'))

    return app
