from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# La URL de conexión se pasa por variable de entorno (Práctica DevOps)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db-service:5432/mi_base_datos'
db = SQLAlchemy(app)

# Definimos el Modelo (La tabla en SQL)
class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(80), nullable=False)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

# === OPERACIONES CRUD ===

# 1. CREATE (Crear un registro)
@app.route('/tareas', methods=['POST'])
def crear_tarea():
    datos = request.get_json()
    nueva_tarea = Tarea(titulo=datos['titulo'])
    db.session.add(nueva_tarea)
    db.session.commit()
    return jsonify({"message": "Tarea creada", "id": nueva_tarea.id}), 201

# 2. READ (Leer todos los registros)
@app.route('/tareas', methods=['GET'])
def obtener_tareas():
    tareas = Tarea.query.all()
    return jsonify([{"id": t.id, "titulo": t.titulo} for t in tareas]), 200

# 3. UPDATE (Actualizar un registro)
@app.route('/tareas/<int:id>', methods=['PUT'])
def actualizar_tarea(id):
    tarea = Tarea.query.get_or_404(id)
    datos = request.get_json()
    tarea.titulo = datos['titulo']
    db.session.commit()
    return jsonify({"message": "Tarea actualizada"}), 200

# 4. DELETE (Borrar un registro)
@app.route('/tareas/<int:id>', methods=['DELETE'])
def borrar_tarea(id):
    tarea = Tarea.query.get_or_404(id)
    db.session.delete(tarea)
    db.session.commit()
    return jsonify({"message": "Tarea eliminada"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
