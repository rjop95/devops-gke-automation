from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# L2 Feature: Health Check Endpoint for Uptrends/Monitoring
@app.route('/health', methods=['GET'])
def health_check():
    # Demonstrates monitoring awareness
    return jsonify({"status": "healthy", "version": "v7.1", "environment": "production"}), 200

@app.route('/')
def hello():
    return jsonify({"message": "Welcome to the Production API"}), 200

# L2 Troubleshooting Case: API with Permission Logic
@app.route('/api/v1/user/update', methods=['POST'])
def update_user():
    auth_token = request.headers.get('X-Support-Token')
    
    # Simulate a 401/403 for troubleshooting practice
    if not auth_token:
        return jsonify({"error": "Missing X-Support-Token"}), 401
    if auth_token != "L2-SUPER-SECRET":
        return jsonify({"error": "Unauthorized access level"}), 403
        
    return jsonify({"message": "User updated successfully"}), 200

if __name__ == "__main__":
    # Listening on 8080 for GKE compatibility
    app.run(host='0.0.0.0', port=8080)
