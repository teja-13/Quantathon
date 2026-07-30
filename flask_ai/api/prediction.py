import os
import tempfile

from flask import jsonify, request

from core.preprocessing import ImagePreprocessor
from core.predictor import predictor

from utils.image_utils import read_image
from utils.validators import (
    allowed_file,
    validate_cancer_type
)

from utils.logger import logger


def predict():

    try:

        # Check image

        if "image" not in request.files:

            return jsonify({

                "success": False,

                "message": "Image file is required."

            }), 400

        image_file = request.files["image"]

        if image_file.filename == "":

            return jsonify({

                "success": False,

                "message": "No image selected."

            }), 400

        # Validate extension

        if not allowed_file(image_file.filename):

            return jsonify({

                "success": False,

                "message": "Unsupported image format."

            }), 400

        # Cancer Type

        cancer_type = request.form.get(
            "cancer_type",
            ""
        ).lower()

        if not validate_cancer_type(cancer_type):

            return jsonify({

                "success": False,

                "message": "Invalid cancer type."

            }), 400

        # Save temporarily

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".png"
        ) as temp:

            image_file.save(temp.name)

            image = read_image(temp.name)

        os.remove(temp.name)

        # Preprocess

        image = ImagePreprocessor.preprocess(image)

        # Prediction

        result = predictor.predict(

            image,

            cancer_type

        )

        logger.info(

            f"{cancer_type} prediction completed."

        )

        return jsonify({

            "success": True,

            "cancer_type": cancer_type,

            "result": result

        })

    except Exception as e:

        logger.exception(str(e))

        return jsonify({

            "success": False,

            "message": str(e)

        }), 500