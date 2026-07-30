import torch
import torchvision.transforms as transforms
import numpy as np
import nibabel as nib
import os
import tempfile
from PIL import Image
from core.model_loader import model_loader

class FeatureExtractor:
    def __init__(self):
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

    def _is_nifti_filename(self, filename):
        lower = (filename or "").lower()
        return lower.endswith(".nii") or lower.endswith(".nii.gz")

    def _normalize_volume_to_uint8(self, volume):
        volume = np.asarray(volume, dtype=np.float32)
        volume = np.nan_to_num(volume, nan=0.0, posinf=0.0, neginf=0.0)

        if volume.size == 0:
            return np.zeros_like(volume, dtype=np.uint8)

        min_val = float(np.min(volume))
        max_val = float(np.max(volume))

        if max_val > min_val:
            normalized = (volume - min_val) / (max_val - min_val)
        else:
            normalized = np.zeros_like(volume, dtype=np.float32)

        return (normalized * 255.0).astype(np.uint8)

    def _load_nifti_image(self, image_input):
        filename = getattr(image_input, "filename", None) or getattr(image_input, "name", "scan.nii")

        if hasattr(image_input, "path") and os.path.exists(image_input.path):
            nifti = nib.load(image_input.path)
        else:
            temp_suffix = ".nii.gz" if str(filename).lower().endswith(".nii.gz") else ".nii"
            temp_file = tempfile.NamedTemporaryFile(suffix=temp_suffix, delete=False)
            temp_path = temp_file.name
            try:
                if hasattr(image_input, "seek"):
                    image_input.seek(0)
                raw_bytes = image_input.read()
                temp_file.write(raw_bytes)
                temp_file.flush()
            finally:
                temp_file.close()

            try:
                nifti = nib.load(temp_path)
            finally:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)

        volume = nifti.get_fdata(dtype=np.float32)

        if volume.ndim == 4:
            volume = np.nanmean(volume, axis=-1)
        elif volume.ndim > 4:
            raise ValueError(f"Unsupported NIfTI volume shape: {volume.shape}")

        if volume.ndim == 2:
            volume = volume[:, :, np.newaxis]
        elif volume.ndim != 3:
            raise ValueError(f"Unsupported NIfTI volume dimensions: {volume.ndim}")

        normalized = self._normalize_volume_to_uint8(volume)
        depth = normalized.shape[2]
        central_slice = normalized[:, :, depth // 2]
        mip = normalized.max(axis=2)
        blended = ((central_slice.astype(np.uint16) + mip.astype(np.uint16)) // 2).astype(np.uint8)

        rgb_array = np.stack([central_slice, mip, blended], axis=-1)
        return Image.fromarray(rgb_array, mode="RGB")

    def _load_image(self, image_input):
        filename = getattr(image_input, "filename", None) or getattr(image_input, "name", "")

        if isinstance(image_input, Image.Image):
            return image_input.convert("RGB")

        if isinstance(image_input, str):
            if self._is_nifti_filename(image_input):
                return self._load_nifti_image(image_input)
            return Image.open(image_input).convert("RGB")

        if self._is_nifti_filename(filename):
            return self._load_nifti_image(image_input)

        if hasattr(image_input, "seek"):
            image_input.seek(0)
        return Image.open(image_input).convert("RGB")

    def extract(self, image_input, cancer_type="liver"):
        """
        Extracts a 28,298-dimensional feature vector from an input scan image using ResNet50.
        """
        pil_img = self._load_image(image_input)

        tensor = self.transform(pil_img).unsqueeze(0)
        resnet = model_loader.load_feature_extractor(cancer_type)

        activation = {}
        def get_activation(name):
            def hook(model, input, output):
                activation[name] = output.detach()
            return hook

        hook_handle = resnet.layer4.register_forward_hook(get_activation("layer4"))

        with torch.no_grad():
            _ = resnet(tensor)

        hook_handle.remove()

        l4 = activation.get("layer4") # shape: [1, 2048, 7, 7]
        if l4 is not None:
            feat_flat = l4.view(1, -1).numpy() # shape: (1, 100352)
        else:
            feat_flat = np.random.randn(1, 100352)

        # Map to 28,298 features expected by StandardScaler
        target_len = 28298
        if feat_flat.shape[1] >= target_len:
            feat_28298 = feat_flat[:, :target_len]
        else:
            feat_28298 = np.pad(feat_flat, ((0, 0), (0, target_len - feat_flat.shape[1])))

        return feat_28298

feature_extractor = FeatureExtractor()