from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from .models import UserSettings
from .forms import UserSettingsForm

class SettingsView(LoginRequiredMixin, View):
    template_name = 'settings/settings.html'

    def get(self, request):
        settings_obj, _ = UserSettings.objects.get_or_create(user=request.user)
        form = UserSettingsForm(instance=settings_obj)
        return render(request, self.template_name, {'form': form, 'user_settings': settings_obj})

    def post(self, request):
        settings_obj, _ = UserSettings.objects.get_or_create(user=request.user)
        form = UserSettingsForm(request.POST, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "System preferences and notification settings updated successfully.")
            return redirect('system_settings:settings')
        return render(request, self.template_name, {'form': form, 'user_settings': settings_obj})
