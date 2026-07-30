from django.db import models
from diagnosis.models import Diagnosis

class MedicalReport(models.Model):
    diagnosis = models.OneToOneField(Diagnosis, on_delete=models.CASCADE, related_name='report')
    report_number = models.CharField(max_length=50, unique=True)
    doctor_notes = models.TextField(blank=True)
    treatment_guidelines = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Report {self.report_number} - {self.diagnosis.patient.full_name}"
