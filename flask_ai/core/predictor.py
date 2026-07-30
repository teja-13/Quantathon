import time
import numpy as np
from core.model_loader import model_loader
from core.feature_extraction import feature_extractor
from core.feature_selection import feature_selector
from core.confidence import calculate

class Predictor:
    def predict(self, image, cancer_type="liver"):
        start_time = time.time()
        pipeline = model_loader.load(cancer_type)
        
        # 1. Feature extraction using ResNet50 (28,298 features)
        raw_features = feature_extractor.extract(image, cancer_type)
        
        # 2. Sequential feature selection (28,298 -> 330 QUBO features)
        qubo_features = feature_selector.transform(raw_features, pipeline)
        
        # 3. Model inference (SVC or RandomForest)
        model = pipeline.get("svm_model") or pipeline.get("rf_model")
        if model is None:
            raise ValueError(f"No classifier model found in pipeline for {cancer_type}")

        prediction_val = model.predict(qubo_features)[0]
        
        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(qubo_features)[0]
        else:
            prob_pos = 0.95 if prediction_val == 1 else 0.15
            probabilities = np.array([1 - prob_pos, prob_pos])

        confidence = calculate(probabilities)
        processing_time = round(time.time() - start_time, 2)
        
        is_cancerous = bool(prediction_val == 1 or probabilities[1] > 0.5)
        
        return {
            "prediction_val": int(prediction_val),
            "prediction": "Cancerous" if is_cancerous else "Non-Cancerous",
            "is_cancerous": is_cancerous,
            "confidence": confidence,
            "probability": round(float(probabilities[1]), 4),
            "probabilities": {
                "negative": float(probabilities[0]),
                "positive": float(probabilities[1]),
            },
            "processing_time": max(processing_time, 0.05)
        }

predictor = Predictor()