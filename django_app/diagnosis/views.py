from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, FormView, DetailView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from .models import Diagnosis
from .forms import UploadDiagnosisForm
from patients.models import Patient
from services.api_client import predict_cancer, ai_client

class CancerSelectionView(LoginRequiredMixin, TemplateView):
    template_name = 'diagnosis/select_cancer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = [
            {'code': 'all', 'label': 'All Regions'},
            {'code': 'brain', 'label': 'Brain'},
            {'code': 'lung', 'label': 'Lung'},
            {'code': 'liver', 'label': 'Liver'},
            {'code': 'breast', 'label': 'Breast'},
            {'code': 'kidney', 'label': 'Kidney'},
        ]
        context['cancer_types'] = [
            {
                'name': 'Brain Cancer',
                'code': 'Brain Cancer',
                'category': 'brain',
                'icon': 'bi-brain',
                'description': 'MRI scan analysis for Glioblastoma, Astrocytoma, and tumor segmentation.',
                'color': '#1565C0',
                'image': 'images/brain-cancer.svg'
            },
            {
                'name': 'Lung Cancer',
                'code': 'Lung Cancer',
                'category': 'lung',
                'icon': 'bi-lungs',
                'description': 'Low-dose Chest CT nodule detection, malignancy prediction, and volume quantification.',
                'color': '#009688',
                'image': 'images/lung-cancer.svg'
            },
            {
                'name': 'Liver Cancer',
                'code': 'Liver Cancer',
                'category': 'liver',
                'icon': 'bi-capsule',
                'description': 'Multiphasic CT/MRI LI-RADS lesion classification and liver parenchymal profiling.',
                'color': '#FF9800',
                'image': 'images/liver-cancer.svg'
            },
            {
                'name': 'Breast Cancer',
                'code': 'Breast Cancer',
                'category': 'breast',
                'icon': 'bi-activity',
                'description': 'Digital mammography and ultrasound feature extraction for BI-RADS assessment.',
                'color': '#E91E63',
                'image': 'images/breast-cancer.svg'
            },
            {
                'name': 'Kidney Cancer',
                'code': 'Kidney Cancer',
                'category': 'kidney',
                'icon': 'bi-segmented-nav',
                'description': 'Renal Corticomedullary CT/MRI lesion classification and RCC staging.',
                'color': '#9C27B0',
                'image': 'images/kidney-cancer.svg'
            },
        ]
        return context

class UploadDiagnosisView(LoginRequiredMixin, FormView):
    template_name = 'diagnosis/upload.html'
    form_class = UploadDiagnosisForm

    def get_initial(self):
        initial = super().get_initial()
        cancer_type = self.request.GET.get('type', 'Brain Cancer')
        patient_id = self.request.GET.get('patient')
        if cancer_type and cancer_type not in ['Auto-Detect', 'Colon Cancer']:
            initial['cancer_type'] = cancer_type
        if patient_id:
            try:
                initial['patient'] = Patient.objects.get(pk=patient_id)
            except Patient.DoesNotExist:
                pass
        return initial

    def form_valid(self, form):
        diagnosis = form.save(commit=False)
        diagnosis.status = 'Processing'
        diagnosis.save()

        # Call Service Layer (AI malignancy prediction)
        res = predict_cancer(
            image_file=diagnosis.medical_image,
            cancer_type=form.cleaned_data.get('cancer_type', 'Brain Cancer'),
            patient_name=diagnosis.patient.full_name
        )

        # Update Diagnosis model with prediction payload
        diagnosis.cancer_type = res['cancer_type']
        diagnosis.prediction = res['prediction']
        diagnosis.confidence = res['confidence']
        diagnosis.probability = res['probability']
        diagnosis.processing_time = res['processing_time']
        diagnosis.estimated_stage = res.get('estimated_stage', '')
        diagnosis.model_explanation = res['model_explanation']
        diagnosis.status = 'Completed'
        diagnosis.save()

        # Automatically generate and save MedicalReport to history archive
        from reports.models import MedicalReport
        from services.api_client import generate_report
        from accounts.models import ActivityLog

        report, created = MedicalReport.objects.get_or_create(diagnosis=diagnosis)
        if created or not report.report_number:
            payload = generate_report({
                'cancer_type': diagnosis.cancer_type,
                'patient_name': diagnosis.patient.full_name,
            })
            report.report_number = payload['report_number']
            report.treatment_guidelines = payload['treatment_guidelines']
            report.doctor_notes = payload['doctor_notes']
            report.save()

        if self.request.user.is_authenticated:
            ActivityLog.objects.create(
                user=self.request.user,
                action=f"Generated & Saved Medical Report #{report.report_number} for Patient {diagnosis.patient.full_name} ({diagnosis.cancer_type} - {diagnosis.prediction})"
            )

        messages.success(self.request, f"Scan analyzed & Medical Report #{report.report_number} saved to history archive!")
        return redirect('diagnosis:processing', pk=diagnosis.pk)

class ProcessingView(LoginRequiredMixin, DetailView):
    model = Diagnosis
    template_name = 'diagnosis/processing.html'
    context_object_name = 'diagnosis'

class PredictionResultView(LoginRequiredMixin, DetailView):
    model = Diagnosis
    template_name = 'diagnosis/prediction.html'
    context_object_name = 'diagnosis'

class ExplainabilityView(LoginRequiredMixin, DetailView):
    model = Diagnosis
    template_name = 'diagnosis/explainability.html'
    context_object_name = 'diagnosis'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        diagnosis = self.get_object()
        
        info = ai_client.CANCER_DESCRIPTIONS.get(
            diagnosis.cancer_type,
            ai_client.CANCER_DESCRIPTIONS['Brain Cancer']
        )
        context['feature_importance'] = info['features']
        context['model_explanation'] = info['explanation']
        return context
