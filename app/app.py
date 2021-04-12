from flask import Flask, request

import datetime
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask import jsonify

from models.models import db
from resources.resources import *


# initialize instance of WSGI application
# act as a central registry for the view functions, URL rules, template configs
app = Flask(__name__)

## include db name in URI; _HOST entry overwrites all others
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'

db.init_app(app)
api = Api(app)
jwt = JWTManager(app)

api.add_resource(RecursoListarlibros, '/libros')
api.add_resource(RecursoListarLibro, '/libro/<int:id_libro>')
api.add_resource(RegistroUsuario, '/registro')
api.add_resource(InicioSesionUsuario, '/login')
api.add_resource(PerfilUsuario, '/usuario')
api.add_resource(PrestamosUsuario, '/usuario/<int:id_usuario>/prestamos')

if __name__ == '__main__':
    app.run(debug=True)
