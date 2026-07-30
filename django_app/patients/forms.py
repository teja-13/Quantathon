from django import forms
from .models import Patient

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'first_name', 'last_name', 'age', 'gender',
            'blood_group', 'phone', 'email', 'address',
            'doctor_name', 'medical_notes'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Eleanor'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Vance'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 120, 'placeholder': 'e.g. 54'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'blood_group': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. +1 (555) 234-5678'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'eleanor.vance@example.com'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '742 Evergreen Terrace, Springfield'}),
            'doctor_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dr. Sarah Jenkins'}),
            'medical_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Prior clinical history, allergies, or diagnostic notes...'}),
        }
