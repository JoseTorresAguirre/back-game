from flask import Blueprint, request, jsonify
from ..models import Usuario, db
from werkzeug.security import generate_password_hash

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    
    new_user = Usuario(
        nombre=data['nombre'],
        email=data['email'],
        dni=data['dni'],
        password=data['password'],
        celular=data.get('celular'),
        rol=data['rol'],
        fecha_registro=data['fecha_registro'],
        fecha_nacimiento=data.get('fecha_nacimiento'),
        direccion=data.get('direccion'),
        sexo=data.get('sexo'),
        especialidad=data.get('especialidad'),
        imagen_perfil_url=data.get('imagen_perfil_url')
    )
    
    # Hash the password
    new_user.set_password(data['password'])
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Usuario registrado exitosamente."}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
