from django import forms
from .models import MedicalReport

class MedicalReportForm(forms.ModelForm):
    class Meta:
        model = MedicalReport
        fields = ['doctor_notes', 'treatment_guidelines']
        widgets = {
            'doctor_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'treatment_guidelines': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
