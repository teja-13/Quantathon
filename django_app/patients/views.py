from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from .models import Patient
from .forms import PatientForm

class PatientListView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'patients/patient_list.html'
    context_object_name = 'patients'
    paginate_by = 8

    def get_queryset(self):
        queryset = Patient.objects.all()
        query = self.request.GET.get('q')
        gender = self.request.GET.get('gender')
        blood_group = self.request.GET.get('blood_group')

        if query:
            queryset = queryset.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(phone__icontains=query) |
                Q(email__icontains=query) |
                Q(doctor_name__icontains=query)
            )
        if gender:
            queryset = queryset.filter(gender=gender)
        if blood_group:
            queryset = queryset.filter(blood_group=blood_group)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['selected_gender'] = self.request.GET.get('gender', '')
        context['selected_blood_group'] = self.request.GET.get('blood_group', '')
        context['gender_choices'] = Patient.GENDER_CHOICES
        context['blood_group_choices'] = Patient.BLOOD_GROUP_CHOICES
        return context

class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = 'patients/patient_profile.html'
    context_object_name = 'patient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = self.get_object()
        context['diagnoses'] = patient.diagnoses.all()
        return context

class PatientCreateView(LoginRequiredMixin, CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patients/add_patient.html'

    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            full_name = self.request.user.get_full_name()
            initial['doctor_name'] = f"Dr. {full_name}" if full_name else f"Dr. {self.request.user.username}"
        return initial

    def form_valid(self, form):
        if not form.cleaned_data.get('doctor_name') and self.request.user.is_authenticated:
            full_name = self.request.user.get_full_name()
            form.instance.doctor_name = f"Dr. {full_name}" if full_name else f"Dr. {self.request.user.username}"
        messages.success(self.request, f"Patient '{form.instance.full_name}' added successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('patients:detail', kwargs={'pk': self.object.pk})

class PatientUpdateView(LoginRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patients/edit_patient.html'

    def form_valid(self, form):
        messages.success(self.request, f"Patient record for '{form.instance.full_name}' updated successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('patients:detail', kwargs={'pk': self.object.pk})

class PatientDeleteView(LoginRequiredMixin, DeleteView):
    model = Patient
    template_name = 'base/modal.html'
    success_url = reverse_lazy('patients:list')

    def delete(self, request, *args, **kwargs):
        patient = self.get_object()
        messages.success(request, f"Patient '{patient.full_name}' record deleted successfully.")
        return super().delete(request, *args, **kwargs)
