from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from patients.models import Patient
from diagnosis.models import Diagnosis
from reports.models import MedicalReport

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Stats metrics
        context['total_patients'] = Patient.objects.count()
        context['total_diagnoses'] = Diagnosis.objects.count()
        context['total_reports'] = MedicalReport.objects.count()
        context['reports_generated'] = MedicalReport.objects.count()
        
        # Recent lists
        context['recent_patients'] = Patient.objects.all()[:5]
        context['recent_diagnoses'] = Diagnosis.objects.select_related('patient')[:5]
        context['recent_reports'] = MedicalReport.objects.select_related('diagnosis', 'diagnosis__patient')[:5]
        
        # Chart Data aggregations
        cancer_types = ['Brain Cancer', 'Breast Cancer', 'Lung Cancer', 'Liver Cancer', 'Kidney Cancer']
        cancer_counts = [
            Diagnosis.objects.filter(cancer_type=ct).count() or 1 for ct in cancer_types
        ]
        context['cancer_types_json'] = cancer_types
        context['cancer_counts_json'] = cancer_counts
        
        return context
