from core.model_loader import model_loader
from core.feature_extraction import feature_extractor
from core.feature_selection import feature_selector
from core.postprocessing import build_response


class Predictor:

    def predict(
        self,
        image,
        cancer_type
    ):

        features = feature_extractor.extract(image)

        features = feature_selector.transform(features)

        model = model_loader.load(cancer_type)

        prediction = model.predict(
            [features]
        )[0]

        probabilities = model.predict_proba(
            [features]
        )[0]

        return build_response(
            prediction,
            probabilities
        )


predictor = Predictor()