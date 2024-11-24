from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app, origins=["http://localhost:5173"], methods=["GET", "POST", "OPTIONS"], supports_credentials=True)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/usuariosDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de la tabla usuarios
class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(50), nullable=False)
    apellidos = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    celular = db.Column(db.String(15))
    pais = db.Column(db.String(50))
    departamento = db.Column(db.String(50))
    direccion = db.Column(db.String(100))
    password = db.Column(db.String(200), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Modelo de la tabla 'nicks'
class Nick(db.Model):
    __tablename__ = 'nicks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    nick = db.Column(db.String(255), nullable=False)

    user = db.relationship('Usuario', backref=db.backref('nicks', lazy=True))


# Crear las tablas en la base de datos si no existen
with app.app_context():
    db.create_all()

# Endpoint para registrar usuarios
@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    hashed_password = generate_password_hash(data['dni'], method='pbkdf2:sha256')  # Usando DNI como contraseña inicial

    new_user = Usuario(
        nombres=data.get('nombres'),
        apellidos=data.get('apellidos'),
        email=data.get('email'),
        dni=data.get('dni'),
        celular=data.get('celular'),
        pais=data.get('pais'),
        departamento=data.get('departamento'),
        direccion=data.get('direccion'),
        password=hashed_password,
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Usuario registrado exitosamente."}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# Endpoint para login de usuarios
@app.route('/login', methods=['POST'])
def login_user():
    data = request.json
    user = Usuario.query.filter_by(email=data['email']).first()

    # Verificar existencia del usuario y contraseña
    if user:
        
        
        if check_password_hash(user.password, data['password']):  # Aquí se compara la contraseña
            session['user_id'] = user.id
            session['email'] = user.email
            
            # Enviar el userId en la respuesta
            return jsonify({
                'message': 'Login exitoso',
                'userId': user.id  # Asegúrate de incluir el userId
            }), 200
        else:
            return jsonify({'message': 'Credenciales incorrectas'}), 401
    else:
        return jsonify({'message': 'Usuario no encontrado'}), 404


# Endpoint de logout
@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return jsonify({"message": "Logout exitoso"}), 200

# Endpoint para guardar el nick
@app.route('/save-nick', methods=['POST'])
def savenick():
    data = request.get_json()  # Obtenemos los datos del cuerpo de la solicitud
    
    # Verificamos si 'user_id' y 'nick' están presentes en el cuerpo de la solicitud
    if not data.get('user_id') or not data.get('nick'):
        return jsonify({"error": "user_id y nick son requeridos"}), 400

    # Buscamos al usuario por 'user_id' (puedes usar el 'email' si es necesario)
    user = Usuario.query.filter_by(id=data['user_id']).first()

    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    # Creamos el nuevo registro de 'nick'
    new_nick = Nick(user_id=data['user_id'], nick=data['nick'])
    
    try:
        # Insertamos el nuevo 'nick' en la base de datos
        db.session.add(new_nick)
        db.session.commit()
        return jsonify({"message": "Nick guardado con éxito"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al guardar el nick: {str(e)}"}), 500

#Verificar si un usuario posee nick o no   
@app.route('/get-nick/<int:user_id>', methods=['GET'])
def get_nick(user_id):
    # Buscar el nick asociado al usuario
    user_nick = Nick.query.filter_by(user_id=user_id).first()

    if user_nick:
        return jsonify({"nick": user_nick.nick}), 200  # Nick encontrado
    else:
        return jsonify({"nick": None}), 200  # No se encuentra nick, pero se responde con 200
    



if __name__ == '__main__':
    app.run(debug=True)
