from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics

PORT = 8080

app = Flask(__name__)
metrics = PrometheusMetrics(app)

@app.route('/')
def home():
    return jsonify ({
        "message" : "Devops Capstone V1 Active"
    })

@app.route('/health')
def health():
    return jsonify ({
        "status" : "healthy"
    }), 200 # status code

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT) 
