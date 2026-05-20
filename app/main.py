from flask import Flask, jsonify, request, has_request_context, g
from flask_sqlalchemy import SQLAlchemy
import logging
import os

# ==========================================
# 1. CONFIGURACIÓN DEL FILTRO DE LOGS
# ==========================================
class RequestIDFilter(logging.Filter):
    def filter(self, record):
        # Si estamos dentro de una petición web y existe un request_id, úsalo
        if has_request_context() and hasattr(g, 'request_id'):
            record.request_id = g.request_id
        else:
            # Fallback para logs internos de Flask/Kubernetes/Werkzeug
            record.request_id = 'SYSTEM'
        return True

# Configurar el logger raíz
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Crear el manejador de salida a consola
handler = logging.StreamHandler()
handler.addFilter(RequestIDFilter())

# Formato que busca el campo 'request_id' sin tronar
formatter = logging.Formatter('[%(asctime)s] [%(request_id)s] %(levelname)s en %(module)s: %(message)s')
handler.setFormatter(formatter)

# Limpiar manejadores viejos y agregar el nuevo
logger.handlers = [handler]

# ==========================================
# 2. INICIALIZACIÓN DE LA APP Y BASE DE DATOS
# ==========================================
app = Flask(__name__)

DATABASE_URL = os.environ.get(
    'DATABASE_URL', 
    'postgresql://user:password@db-service:5432/mi_base_datos'
)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==========================================
# 3. MODELO DE LA BASE DE DATOS (TABLA SQL)
# ==========================================
class Tarea(db.Model):
    __tablename__ = 'tarea'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descripcion": self.descripcion
        }

# ==========================================
# 4. ENDPOINT DE SALUD (KUBERNETES PROBES)
# ==========================================
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "database": "connected"}), 200

# ==========================================
# 5. OPERACIONES CRUD
# ==========================================
@app.route('/tareas', methods=['POST'])
def crear_tarea():
    datos = request.get_json()
    if not datos or 'titulo' not in datos:
        return jsonify({"error": "El campo 'titulo' es obligatorio"}), 400
        
    nueva_tarea = Tarea(
        titulo=datos['titulo'],
        descripcion=datos.get('descripcion', '')
    )
    db.session.add(nueva_tarea)
    db.session.commit()
    return jsonify({"message": "Tarea creada con éxito", "tarea": nueva_tarea.to_dict()}), 201

@app.route('/tareas', methods=['GET'])
def obtener_tareas():
    tareas = Tarea.query.all()
    return jsonify([t.to_dict() for t in tareas]), 200

# ==========================================
# 6. CREACIÓN AUTOMÁTICA DE TABLAS
# ==========================================
with app.app_context():
    logging.info("Verificando y creando tablas en la base de datos...")
    db.create_all()
    logging.info("¡Base de datos sincronizada exitosamente!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
