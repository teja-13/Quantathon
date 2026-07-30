class FeatureSelector:
    def transform(self, features, pipeline):
        """
        Executes sequential feature selection pipeline:
        1. StandardScaler
        2. SelectKBest (28,298 -> 1,000)
        3. RFECV (1,000 -> 660)
        4. QUBO Selected Indices (660 -> 330)
        """
        scaler = pipeline.get("scaler")
        selector = pipeline.get("selector")
        rfecv = pipeline.get("rfecv")
        selected_indices = pipeline.get("selected_indices")

        curr_features = features
        if scaler is not None and hasattr(scaler, "transform"):
            curr_features = scaler.transform(curr_features)

        if selector is not None and hasattr(selector, "transform"):
            curr_features = selector.transform(curr_features)

        if rfecv is not None and hasattr(rfecv, "transform"):
            curr_features = rfecv.transform(curr_features)

        if selected_indices is not None:
            curr_features = curr_features[:, selected_indices]

        return curr_features

feature_selector = FeatureSelector()