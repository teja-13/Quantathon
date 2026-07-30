import os
import uuid
import tempfile

from flask import jsonify, request

from utils.image_utils import read_image
from explainability.gradcam import gradcam
from explainability.shap import shap_generator


def explain():
    temp_path = None

    try:
        # Check if image exists
        if "image" not in request.files:
            return jsonify({
                "success": False,
                "message": "Image is required."
            }), 400

        image_file = request.files["image"]

        if image_file.filename == "":
            return jsonify({
                "success": False,
                "message": "No image selected."
            }), 400

        # Save uploaded image temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp:
            image_file.save(temp.name)
            temp_path = temp.name

        # Read image
        image = read_image(temp_path)

        # Create output folder
        os.makedirs("temp", exist_ok=True)

        # Unique output filenames
        gradcam_path = f"temp/{uuid.uuid4()}_gradcam.png"
        shap_path = f"temp/{uuid.uuid4()}_shap.png"

        # Generate explainability images
        gradcam.generate(image, gradcam_path)
        shap_generator.generate(image, shap_path)

        return jsonify({
            "success": True,
            "message": "Explainability generated successfully.",
            "gradcam": gradcam_path,
            "shap": shap_path
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)