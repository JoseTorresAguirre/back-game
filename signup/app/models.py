from . import db
from werkzeug.security import generate_password_hash

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    dni = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    celular = db.Column(db.String(15))
    rol = db.Column(db.Enum('paciente', 'especialista', 'admin'), nullable=False)
    fecha_registro = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    fecha_nacimiento = db.Column(db.Date)
    direccion = db.Column(db.String(255))
    sexo = db.Column(db.Enum('M', 'F', 'Otro'))
    especialidad = db.Column(db.String(100))
    imagen_perfil_url = db.Column(db.String(255))
    
    def set_password(self, password):
        self.password = generate_password_hash(password)