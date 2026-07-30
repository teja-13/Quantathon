from core.confidence import calculate


def build_response(
    prediction,
    probabilities
):

    confidence = calculate(probabilities)

    return {

        "prediction": int(prediction),

        "confidence": confidence,

        "probabilities": {

            "negative": float(probabilities[0]),

            "positive": float(probabilities[1]),

        }

    }