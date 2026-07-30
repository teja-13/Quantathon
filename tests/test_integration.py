import unittest
import io
import json
import sys
import os
import tempfile

import nibabel as nib
import numpy as np

# Add flask_ai and django_app to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../flask_ai')))

from app import app
from PIL import Image

class FlaskAITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def create_dummy_image(self):
        img = Image.new('RGB', (100, 100), color='red')
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        return img_byte_arr

    def create_dummy_nifti(self):
        volume = np.linspace(0, 1, 1000, dtype=np.float32).reshape(10, 10, 10)
        image = nib.Nifti1Image(volume, affine=np.eye(4))
        temp_file = tempfile.NamedTemporaryFile(suffix='.nii.gz', delete=False)
        temp_file.close()
        nib.save(image, temp_file.name)
        return temp_file.name

    def test_health_endpoint(self):
        response = self.app.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data.get('status'), 'healthy')

    def test_explain_endpoint(self):
        response = self.app.post('/api/explain')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data.get('success'))

    def test_predict_endpoint_brain(self):
        img = self.create_dummy_image()
        data = {
            'image': (img, 'test_scan.png'),
            'cancer_type': 'Brain Cancer'
        }
        response = self.app.post('/api/predict', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        res = json.loads(response.data)
        self.assertTrue(res.get('success'))
        self.assertEqual(res.get('cancer_type'), 'Brain Cancer')

    def test_predict_endpoint_all_modalities(self):
        modalities = ['Brain Cancer', 'Breast Cancer', 'Lung Cancer', 'Liver Cancer', 'Kidney Cancer']
        for cancer_type in modalities:
            img = self.create_dummy_image()
            data = {
                'image': (img, 'scan.png'),
                'cancer_type': cancer_type
            }
            response = self.app.post('/api/predict', data=data, content_type='multipart/form-data')
            self.assertEqual(response.status_code, 200)
            res = json.loads(response.data)
            self.assertTrue(res.get('success'))
            self.assertIn('confidence', res)
            self.assertIn('model_explanation', res)

    def test_predict_endpoint_with_nifti_volume(self):
        nifti_path = self.create_dummy_nifti()
        try:
            with open(nifti_path, 'rb') as nifti_file:
                data = {
                    'image': (nifti_file, 'test_scan.nii.gz'),
                    'cancer_type': 'Brain Cancer'
                }
                response = self.app.post('/api/predict', data=data, content_type='multipart/form-data')

            self.assertEqual(response.status_code, 200)
            res = json.loads(response.data)
            self.assertTrue(res.get('success'))
            self.assertEqual(res.get('cancer_type'), 'Brain Cancer')
        finally:
            if os.path.exists(nifti_path):
                os.unlink(nifti_path)

if __name__ == '__main__':
    unittest.main()
