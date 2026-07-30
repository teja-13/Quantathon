from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, DeleteView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from .models import MedicalReport
from .forms import MedicalReportForm
from diagnosis.models import Diagnosis
from services.api_client import generate_report

class GenerateReportView(LoginRequiredMixin, View):
    """
    Creates or retrieves a MedicalReport for the specified Diagnosis instance using the Service Layer.
    """
    def get(self, request, diagnosis_id):
        diagnosis = get_object_or_404(Diagnosis, pk=diagnosis_id)
        
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
            messages.success(request, f"Medical Report #{report.report_number} generated successfully.")
        
        return redirect('reports:detail', pk=report.pk)

class ReportDetailView(LoginRequiredMixin, DetailView):
    model = MedicalReport
    template_name = 'reports/report.html'
    context_object_name = 'report'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MedicalReportForm(instance=self.get_object())
        return context

    def post(self, request, *args, **kwargs):
        report = self.get_object()
        form = MedicalReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            messages.success(request, "Report notes and clinical guidelines saved.")
        return self.get(request, *args, **kwargs)

class ReportPDFView(LoginRequiredMixin, DetailView):
    model = MedicalReport
    template_name = 'reports/report_print.html'
    context_object_name = 'report'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        report = self.get_object()
        from services.api_client import ai_client
        info = ai_client.CANCER_DESCRIPTIONS.get(
            report.diagnosis.cancer_type,
            ai_client.CANCER_DESCRIPTIONS['Brain Cancer']
        )
        context['feature_importance'] = info['features']
        return context

class ReportHistoryListView(LoginRequiredMixin, ListView):
    model = MedicalReport
    template_name = 'reports/report_history.html'
    context_object_name = 'reports'
    paginate_by = 8

    def get_queryset(self):
        queryset = MedicalReport.objects.select_related('diagnosis', 'diagnosis__patient').all()
        query = self.request.GET.get('q')
        cancer_type = self.request.GET.get('cancer_type')
        prediction = self.request.GET.get('prediction')

        if query:
            queryset = queryset.filter(
                Q(report_number__icontains=query) |
                Q(diagnosis__patient__first_name__icontains=query) |
                Q(diagnosis__patient__last_name__icontains=query) |
                Q(diagnosis__patient__doctor_name__icontains=query)
            )
        if cancer_type:
            queryset = queryset.filter(diagnosis__cancer_type=cancer_type)
        if prediction:
            queryset = queryset.filter(diagnosis__prediction=prediction)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['selected_cancer_type'] = self.request.GET.get('cancer_type', '')
        context['selected_prediction'] = self.request.GET.get('prediction', '')
        context['cancer_types'] = [ct[0] for ct in Diagnosis.CANCER_TYPES]
        return context

class ReportDeleteView(LoginRequiredMixin, DeleteView):
    model = MedicalReport
    template_name = 'base/modal.html'
    success_url = reverse_lazy('reports:history')

    def delete(self, request, *args, **kwargs):
        report = self.get_object()
        messages.success(request, f"Report #{report.report_number} deleted successfully.")
        return super().delete(request, *args, **kwargs)
