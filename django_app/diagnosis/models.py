from django.db import models
from patients.models import Patient

class Diagnosis(models.Model):
    CANCER_TYPES = [
        ('Brain Cancer', 'Brain Cancer'),
        ('Breast Cancer', 'Breast Cancer'),
        ('Lung Cancer', 'Lung Cancer'),
        ('Liver Cancer', 'Liver Cancer'),
        ('Kidney Cancer', 'Kidney Cancer'),
    ]

    PREDICTION_CHOICES = [
        ('Cancerous', 'Cancerous'),
        ('Non-Cancerous', 'Non-Cancerous'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='diagnoses')
    cancer_type = models.CharField(max_length=50, choices=CANCER_TYPES, default='Brain Cancer')
    medical_image = models.ImageField(upload_to='scans/')
    prediction = models.CharField(max_length=20, choices=PREDICTION_CHOICES, default='Cancerous')
    confidence = models.FloatField(default=95.0)
    probability = models.FloatField(default=0.95)
    processing_time = models.FloatField(default=1.20)
    estimated_stage = models.CharField(max_length=50, default='Stage II (Localized)')
    model_explanation = models.TextField(blank=True)
    status = models.CharField(max_length=20, default='Completed')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Diagnoses'

    def __str__(self):
        return f"{self.cancer_type} - {self.patient.full_name} ({self.prediction})"
