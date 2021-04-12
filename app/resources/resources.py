import datetime
from flask import request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from models.models import db, Libro, LibroSchema, Prestamo, PrestamoSchema, Usuario, UsuarioSchema
from flask_restful import Resource
from tasks import celery
from time import sleep

libro_schema = LibroSchema()
prestamo_schema = PrestamoSchema()
usuario_schema = UsuarioSchema()

class RecursoListarlibros(Resource):
    def get(self):
        libros = [libro_schema.dump(l) for l in Libro.query.all()]
        return libros
    
    def post(self):
        nuevo_libro = Libro(titulo=request.json["titulo"], autor=request.json["autor"], genero=request.json["genero"])
        db.session.add(nuevo_libro)
        db.session.commit()
        return libro_schema.dump(nuevo_libro)

class RecursoListarLibro(Resource):
    def get(self, id_libro):
        libro = Libro.query.get_or_404(id_libro)
        return libro_schema.dump(libro)

    def put(self, id_libro):
        libro = Libro.query.get_or_404(id_libro)
        libro.titulo = request.json.get("titulo",libro.titulo)
        libro.autor = request.json.get("autor", libro.autor)
        libro.genero = request.json.get("genero", libro.genero)
        db.session.commit()
        return libro_schema.dump(libro)
 
    def delete(self, id_libro):
        libro = Libro.query.get_or_404(id_libro)
        db.session.delete(libro)
        db.session.commit()
        return '',204

class RegistroUsuario(Resource):
    def post(self):
        nuevo_usuario = Usuario(username=request.json.get("username"), contrasena=request.json.get("contrasena"))
        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
            return {'mensaje':"Inscripción exitosa"}
        except Exception as e:
            return {'mensaje':"Error al inscribir el usuario ({})".format(e)}

class InicioSesionUsuario(Resource):

    def post(self):
        username = request.json.get("username")
        contrasena = request.json.get("contrasena")
        usuario = Usuario.query.filter_by(username = username).first()
        if not usuario:
            return {"mensaje":"El usuario no está registrado"}
        else:
            if contrasena != usuario.contrasena:
                return {"mensaje":"contraseña incorrecta"}
            else:
                access_token = create_access_token(identity = username)
                return {"mensaje":"login exitoso", "token de acceso":access_token}

class PrestamosUsuario(Resource):

    def get(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        return [prestamo_schema.dump(prestamo) for prestamo in usuario.prestamos]

    def post(self, id_usuario):
        dias = request.json.get("dias",1)
        libro_id = request.json.get("libro_id")
        task = self.gestionar_reserva.delay(id_usuario,dias, libro_id)
        return {'task_id': task.id}, 204

    @staticmethod
    @celery.task()
    def gestionar_reserva(id_usuario, dias, libro_id):
        sleep(10)
        #prestamo = Prestamo(fecha = datetime.datetime.utcnow(), dias=dias, libro_id =libro_id )
        #usuario = Usuario.query.get_or_404(id_usuario)
        #usuario.prestamos.append(prestamo)
        #db.session.commit()
        #return prestamo_schema.dump(prestamo)
        return 10

class PerfilUsuario(Resource):

    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        return [usuario_schema.dump(l) for l in Usuario.query.all()]
     