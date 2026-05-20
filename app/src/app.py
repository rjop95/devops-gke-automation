from flask import Flask, jsonify, request
from models import db, Usuario, Producto, Suscripcion
from datetime import datetime, timedelta

app = Flask(__name__)

# 1. Configuración de la conexión a PostgreSQL
# Usamos las credenciales exactas de tu postgres.yaml (user, password, mi_base_datos)
# 'db-service' es el nombre del Service de Kubernetes que resuelve la IP interna
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db-service:5432/mi_base_datos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 2. Inicializar la base de datos con la aplicación Flask
db.init_app(app)


# --- ENDPOINTS DE PRUEBA ---

@app.route('/')
def home():
    return jsonify({"mensaje": "La API de Usuarios y Suscripciones está corriendo exitosamente."}), 200


@app.route('/init-db', methods=['GET'])
def init_db():
    """Ruta para mapear los modelos de Python y crear las tablas físicas en Postgres."""
    try:
        db.create_all()
        return jsonify({"status": "éxito", "mensaje": "Tablas creadas correctamente en PostgreSQL."}), 200
    except Exception as e:
        return jsonify({"status": "error", "mensaje": str(e)}), 500


@app.route('/usuarios/test', methods=['POST'])
def crear_usuario_test():
    """Ruta de prueba para insertar un usuario y una suscripción simulada."""
    try:
        # 1. Crear un usuario de prueba único usando la hora actual para evitar duplicados de email
        timestamp = datetime.utcnow().strftime('%H%M%S')
        nuevo_usuario = Usuario(
            nombre=f"Usuario Test {timestamp}",
            email=f"test_{timestamp}@ricardojop.com"
        )
        db.session.add(nuevo_usuario)
        db.session.flush() # flush() genera el ID del usuario sin cerrar la transacción

        # 2. Crear un producto/plan de prueba
        nuevo_plan = Producto(
            nombre="Plan Premium DevOps",
            precio=299.00,
            descripcion="Acceso completo al clúster de producción"
        )
        db.session.add(nuevo_plan)
        db.session.flush()

        # 3. Asignar la suscripción amarrando las llaves foráneas
        nueva_suscripcion = Suscripcion(
            usuario_id=nuevo_usuario.id,
            producto_id=nuevo_plan.id,
            estado="activa",
            fecha_fin=datetime.utcnow() + timedelta(days=30) # Vence en 30 días
        )
        db.session.add(nueva_suscripcion)
        
        # Guardar todos los cambios de forma definitiva en Postgres
        db.session.commit()

        return jsonify({
            "status": "usuario_creado",
            "usuario": {
                "id": nuevo_usuario.id,
                "nombre": nuevo_usuario.nombre,
                "email": nuevo_usuario.email
            },
            "suscripcion_asignada": {
                "plan": nuevo_plan.nombre,
                "precio": float(nuevo_plan.precio),
                "estado": nueva_suscripcion.estado
            }
        }), 201

    except Exception as e:
        db.session.rollback() # Cancela la operación si algo falla para no dejar datos corruptos
        return jsonify({"status": "error", "mensaje": str(e)}), 500


@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    """Ruta para listar todos los usuarios registrados y ver sus suscripciones."""
    usuarios = Usuario.query.all()
    resultado = []
    
    for u in usuarios:
        # Gracias a db.relationship, podemos acceder a u.suscripciones directamente
        sub_info = []
        for s in u.suscripciones:
            sub_info.append({
                "plan_id": s.producto_id,
                "estado": s.estado,
                "vence": s.fecha_fin.strftime('%Y-%m-%d')
            })
            
        resultado.append({
            "id": u.id,
            "nombre": u.nombre,
            "email": u.email,
            "suscripciones": sub_info
        })
        
    return jsonify(resultado), 200

@app.route('/usuarios', methods=['POST'])
def crear_usuario_real():
    """Endpoint real para registrar un usuario con validaciones de datos y duplicados."""
    # 1. Obtener los datos enviados en el cuerpo de la petición (JSON)
    datos = request.get_json()

    # Si no mandaron ningún JSON o viene vacío
    if not datos:
        return jsonify({"status": "error", "mensaje": "No se recibieron datos en formato JSON"}), 400

    nombre = datos.get('nombre')
    email = datos.get('email')

    # 2. Validación de campos obligatorios
    if not nombre or not email:
        return jsonify({"status": "error", "mensaje": "Faltan campos obligatorios: 'nombre' y 'email' son requeridos"}), 400

    # Validación extra: Que el email tenga una estructura mínima válida
    if "@" not in email or "." not in email:
        return jsonify({"status": "error", "mensaje": "El formato del correo electrónico no es válido"}), 400

    try:
        # 3. Control de Duplicados: Buscar si ya existe un usuario con ese mismo email
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            return jsonify({"status": "error", "mensaje": f"El correo '{email}' ya se encuentra registrado"}), 400

        # 4. Creación e inserción del nuevo usuario real
        nuevo_usuario = Usuario(
            nombre=nombre,
            email=email
        )
        db.session.add(nuevo_usuario)
        db.session.commit() # Guardamos los cambios de forma definitiva

        return jsonify({
            "status": "éxito",
            "mensaje": "Usuario registrado exitosamente",
            "usuario": {
                "id": nuevo_usuario.id,
                "nombre": nuevo_usuario.nombre,
                "email": nuevo_usuario.email
            }
        }), 201

    except Exception as e:
        db.session.rollback() # Si algo truena con la BD, deshacemos la operación para evitar corrupción
        return jsonify({"status": "error", "mensaje": f"Error interno en el servidor: {str(e)}"}), 500


if __name__ == '__main__':
    # Ejecuta la aplicación escuchando en todas las interfaces para Kubernetes
    app.run(host='0.0.0.0', port=8080, debug=True)
