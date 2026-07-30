from flask import jsonify
from datetime import datetime


def health():

    return jsonify({

        "status": "healthy",

        "service": "Cancer Detection AI",

        "version": "1.0.0",

        "timestamp": datetime.utcnow().isoformat()

    })