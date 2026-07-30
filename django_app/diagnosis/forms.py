from django import forms
from django.core.exceptions import ValidationError
from .models import Diagnosis
from patients.models import Patient
import os

class UploadDiagnosisForm(forms.ModelForm):
    patient = forms.ModelChoiceField(
        queryset=Patient.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select form-select-lg', 'id': 'patient_select'}),
        empty_label="-- Select Patient --"
    )

    class Meta:
        model = Diagnosis
        fields = ['patient', 'cancer_type', 'medical_image']
        widgets = {
            'cancer_type': forms.Select(attrs={'class': 'form-select form-select-lg', 'id': 'cancer_type_select'}),
            'medical_image': forms.FileInput(attrs={
                'class': 'form-control form-control-lg',
                'id': 'medical_image_input',
                'accept': '.jpg,.jpeg,.png,.nii,.nii.gz,image/jpeg,image/png,application/gzip,application/octet-stream'
            }),
        }

    def clean_medical_image(self):
        image = self.cleaned_data.get('medical_image')
        if not image:
            raise ValidationError("Please upload a medical diagnostic scan image.")
        
        # File extension validation
        filename = image.name.lower()
        valid_extensions = ['.jpg', '.jpeg', '.png', '.nii', '.nii.gz']
        if not any(filename.endswith(ext) for ext in valid_extensions):
            raise ValidationError("Unsupported file format. Only .jpg, .jpeg, .png, .nii, and .nii.gz files are accepted.")
        
        # Max file size validation (5MB)
        max_size = 5 * 1024 * 1024  # 5MB in bytes
        if image.size > max_size:
            raise ValidationError(f"File size ({round(image.size / (1024 * 1024), 2)}MB) exceeds maximum limit of 5MB.")
            
        return image
