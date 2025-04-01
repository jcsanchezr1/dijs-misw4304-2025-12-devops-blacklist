import os

from flask import Flask
from flask_restful import Api
from config import Config
from models import db
from views import BlacklistView, BlacklistDetailView, HealthCheckView, ResetDatabaseView

app = Flask(__name__)

app.config.from_object(Config)
db.init_app(app)

if not os.getenv('TESTING'):
    with app.app_context():
        db.create_all()

api = Api(app)
api.add_resource(BlacklistView, '/blacklists')
api.add_resource(BlacklistDetailView, '/blacklists/<string:email>')
api.add_resource(HealthCheckView, '/blacklists/ping')
api.add_resource(ResetDatabaseView, '/blacklists/reset')

if __name__ == '__main__':
    app.run(debug=True)
