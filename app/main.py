from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Práctica DevOps: Intentamos leer la URL de la BD desde las variables de entorno.
# Si no existe, usamos por defecto los datos que configuramos en postgres.yaml.
DATABASE_URL = os.environ.get(
    'DATABASE_URL', 
    'postgresql://user:password@db-service:5432/mi_base_datos'
)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==========================================
# MODELO DE LA BASE DE DATOS (TABLA SQL)
# ==========================================
class Tarea(db.Model):
    __tablename__ = 'tarea' # Nombre explícito de la tabla en SQL
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        """Método utilitario para convertir el objeto SQL a JSON"""
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descripcion": self.descripcion
        }

# ==========================================
# ENDPOINT DE SALUD (KUBERNETES PROBES)
# ==========================================
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "database": "connected"}), 200

# ==========================================
# OPERACIONES CRUD
# ==========================================

# 1. CREATE (Crear una nueva tarea)
@app.route('/tareas', methods=['POST'])
def crear_tarea():
    datos = request.get_json()
    
    if not datos or 'titulo' not in datos:
        return jsonify({"error": "El campo 'titulo' es obligatorio"}), 400
        
    nueva_tarea = Tarea(
        titulo=datos['titulo'],
        descripcion=datos.get('descripcion', '') # Opcional
    )
    
    db.session.add(nueva_tarea)
    db.session.commit()
    return jsonify({"message": "Tarea creada con éxito", "tarea": nueva_tarea.to_dict()}), 201

# 2. READ (Leer todas las tareas o una específica)
@app.route('/tareas', methods=['GET'])
def obtener_tareas():
    tareas = Tarea.query.all()
    return jsonify([t.to_dict() for t in tareas]), 200

@app.route('/tareas/<int:id>', methods=['GET'])
def obtener_tarea_por_id(id):
    tarea = Tarea.query.get_or_404(id)
    return jsonify(tarea.to_dict()), 200

# 3. UPDATE (Actualizar una tarea existente)
@app.route('/tareas/<int:id>', methods=['PUT'])
def actualizar_tarea(id):
    tarea = Tarea.query.get_or_404(id)
    datos = request.get_json()
    
    if 'titulo' in datos:
        tarea.titulo = datos['titulo']
    if 'descripcion' in datos:
        tarea.descripcion = datos['descripcion']
        
    db.session.commit()
    return jsonify({"message": "Tarea actualizada con éxito", "tarea": tarea.to_dict()}), 200

# 4. DELETE (Eliminar una tarea)
@app.route('/tareas/<int:id>', methods=['DELETE'])
def borrar_tarea(id):
    tarea = Tarea.query.get_or_404(id)
    db.session.delete(tarea)
    db.session.commit()
    return jsonify({"message": "Tarea eliminada correctamente"}), 200

# ==========================================
# INICIALIZACIÓN AUTOMÁTICA DE TABLAS
# ==========================================
# Este bloque asegura que Flask cree la tabla 'tarea' en Postgres al arrancar
with app.app_context():
    print("Verificando y creando tablas en la base de datos...")
    db.create_all()
    print("¡Base de datos sincronizada!")

if __name__ == '__main__':
    # Escucha en el puerto 8080 (que mapea con el targetPort de tu service.yaml)
    app.run(host='0.0.0.0', port=8080)
