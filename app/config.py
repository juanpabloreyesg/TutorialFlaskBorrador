from app import app, db, Usuario

with app.app_context():
    #print(Usuario.query.all())
    db.create_all()