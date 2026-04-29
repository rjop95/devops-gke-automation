from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "message": "Hola Ricardo, saludos desde GKE!",
        "team": "Global Support Operations (MX-PL)"
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
