import logging
import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)

# Logs estructurados para que aparezcan impecables en GCP Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] TraceID: %(request_id)s - %(message)s')

# Base de datos SQLite en memoria para pruebas rápidas
def init_db():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id TEXT, plan_type TEXT, status TEXT)')
    # Insertamos un usuario VIP activo y uno inactivo para pruebas de soporte
    cursor.execute("INSERT INTO users VALUES ('user_vip_01', 'PREMIUM', 'ACTIVE')")
    cursor.execute("INSERT INTO users VALUES ('user_vip_02', 'PREMIUM', 'INACTIVE')")
    conn.commit()
    return conn

db_conn = init_db()

@app.before_request
def inject_trace_id():
    # Captura el Header de Postman o genera uno por defecto
    request.request_id = request.headers.get('X-Request-ID', 'SYSTEM-GEN')

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "UP"}), 200

@app.route('/api/v1/matches/<match_id>/goals', methods=['GET'])
def get_goals(match_id):
    # SIMULACIÓN DE ERROR L2: 504 Gateway Timeout con proveedor externo (ej. SportRadar)
    logging.error(f"Failed to fetch live stats from external provider. Connection timeout after 5000ms.", extra={'request_id': request.request_id})
    return jsonify({"error": "Gateway Timeout", "message": "External sports feed API not responding"}), 504

@app.route('/api/v1/users/<user_id>/premium-content', methods=['GET'])
def get_premium_content(user_id):
    # SIMULACIÓN DE ERROR L2: 403 Forbidden / Data Mismatch
    conn = sqlite3.connect(':memory:') # Para simulación aislada
    
    # Lógica de soporte L2 simplificada
    if user_id == "user_vip_02":
        logging.warning(f"User {user_id} attempted access. Authentication valid but subscription status is INACTIVE.", extra={'request_id': request.request_id})
        return jsonify({"error": "Forbidden", "message": "Your subscription has expired. Please contact support."}), 403
    elif user_id == "user_vip_01":
        return jsonify({"user_id": user_id, "status": "ACTIVE", "content": "🏅 Welcome to the Olympic Live VIP Stream! 🏅"}), 200
    else:
        logging.error(f"User {user_id} not found in database.", extra={'request_id': request.request_id})
        return jsonify({"error": "Not Found", "message": "User record missing."}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
