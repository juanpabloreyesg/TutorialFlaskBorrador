
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow  
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import datetime

db = SQLAlchemy()


class Libro(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column( db.String(50) )
    autor = db.Column( db.String(50) )
    genero = db.Column( db.String(50) )
    prestamos = db.relationship("Prestamo", backref='libro', lazy=True)

class Prestamo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    fecha = db.Column(db.DateTime)
    dias = db.Column(db.Integer)
    libro_id = db.Column(db.Integer, db.ForeignKey('libro.id'))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    contrasena = db.Column(db.String(50), nullable=False)
    prestamos = db.relationship("Prestamo", backref='usuario', cascade='all, delete, delete-orphan', lazy=True)


class LibroSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = Libro
         include_relationships = True
         load_instance = True

class PrestamoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Prestamo
        include_fk = True
        load_instance = True

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True


