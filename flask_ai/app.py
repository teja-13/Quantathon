import os
import uuid
import tempfile
from flask import Flask, jsonify, request
from config import Config
from api.routes import api_bp

app = Flask(__name__)
app.config.from_object(Config)

# Register API Blueprint under /api prefix
app.register_blueprint(api_bp, url_prefix="/api")

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "status": "online",
        "service": "OncoVision AI Inference Service",
        "endpoints": {
            "health": "/api/health",
            "predict": "/api/predict",
            "explain": "/api/explain"
        }
    }), 200

if __name__ == "__main__":
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)