import os
import io
import zipfile
import joblib
import torch
import torchvision.models as models
from utils.logger import logger

class ModelLoader:
    def __init__(self):
        self.models = {}
        self.feature_extractors = {}

    def get_model_dir(self, cancer_type):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # 1. Primary check: root trained_models/<cancer_type>
        root_dir = os.path.abspath(os.path.join(base_dir, "..", "trained_models", cancer_type.lower()))
        root_pipeline = os.path.join(root_dir, "final_pipeline.pkl")
        if os.path.exists(root_pipeline) and os.path.getsize(root_pipeline) > 0:
            return root_dir

        # 2. Secondary check: flask_ai/models/<cancer_type>
        target_dir = os.path.join(base_dir, "models", cancer_type.lower())
        pipeline_file = os.path.join(target_dir, "final_pipeline.pkl")
        if os.path.exists(pipeline_file) and os.path.getsize(pipeline_file) > 0:
            return target_dir
        
        # 3. Default fallback to trained_models/liver
        fallback_dir = os.path.abspath(os.path.join(base_dir, "..", "trained_models", "liver"))
        return fallback_dir

    def load_feature_extractor(self, cancer_type="liver"):
        cancer_key = cancer_type.lower()
        if cancer_key in self.feature_extractors:
            return self.feature_extractors[cancer_key]

        model_dir = self.get_model_dir(cancer_key)
        extractor_path = os.path.join(model_dir, "resnet50_feature_extractor")

        logger.info(f"Loading ResNet50 Feature Extractor from: {extractor_path}")
        
        resnet = models.resnet50(weights=None)
        resnet.fc = torch.nn.Identity()

        if os.path.exists(extractor_path) and os.path.isdir(extractor_path):
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_STORED) as zip_file:
                for root, dirs, files in os.walk(extractor_path):
                    for file in files:
                        full_path = os.path.join(root, file)
                        arcname = 'archive/' + os.path.relpath(full_path, extractor_path)
                        zinfo = zipfile.ZipInfo(arcname, date_time=(2026, 1, 1, 0, 0, 0))
                        with open(full_path, 'rb') as f:
                            zip_file.writestr(zinfo, f.read())
            zip_buffer.seek(0)
            state_dict = torch.load(zip_buffer, weights_only=False, map_location='cpu')
            resnet.load_state_dict(state_dict, strict=False)

        resnet.eval()
        self.feature_extractors[cancer_key] = resnet
        return resnet

    def load(self, cancer_type="liver"):
        cancer_key = cancer_type.lower()
        if cancer_key in self.models:
            return self.models[cancer_key]

        model_dir = self.get_model_dir(cancer_key)
        pipeline_path = os.path.join(model_dir, "final_pipeline.pkl")

        if not os.path.exists(pipeline_path):
            logger.warning(f"Pipeline path not found: {pipeline_path}. Falling back to liver model.")
            model_dir = self.get_model_dir("liver")
            pipeline_path = os.path.join(model_dir, "final_pipeline.pkl")

        logger.info(f"Loading ML Pipeline dictionary from: {pipeline_path}")
        pipeline = joblib.load(pipeline_path)
        self.models[cancer_key] = pipeline
        return pipeline

model_loader = ModelLoader()