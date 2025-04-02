import os
import sys

# Depuración: Imprimir el directorio actual y las rutas de búsqueda de Python
print(f"Current working directory: {os.getcwd()}")
print(f"Python paths: {sys.path}")

# Asegurarte de que el directorio actual esté en sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

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
    app.run(host='0.0.0.0', port=8080, debug=True)
