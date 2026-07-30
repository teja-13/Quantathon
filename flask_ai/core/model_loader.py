import os
import joblib

from utils.logger import logger


class ModelLoader:

    def __init__(self):

        self.models = {}

    def load(self, cancer_type):

        if cancer_type in self.models:
            return self.models[cancer_type]

        path = os.path.join(
            "models",
            cancer_type,
            "model.pkl"
        )

        if not os.path.exists(path):
            raise FileNotFoundError(path)

        logger.info(f"Loading model: {path}")

        model = joblib.load(path)

        self.models[cancer_type] = model

        return model


model_loader = ModelLoader()