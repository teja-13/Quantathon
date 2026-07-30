from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView
from .forms import UserLoginForm, UserRegisterForm, UserProfileForm, ForgotPasswordForm
from .models import UserProfile

class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'
    form_class = UserLoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, f"Welcome back, Dr. {form.get_user().get_full_name() or form.get_user().username}!")
        return super().form_valid(form)

class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, "You have been logged out successfully.")
        return redirect('accounts:login')

    def post(self, request):
        logout(request)
        messages.info(request, "You have been logged out successfully.")
        return redirect('accounts:login')

class RegisterView(FormView):
    template_name = 'authentication/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('dashboard:index')

    def form_valid(self, form):
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )
        login(self.request, user)
        messages.success(self.request, f"Account created successfully! Welcome to the Cancer Detection System, Dr. {user.last_name}.")
        return redirect('dashboard:index')

class ForgotPasswordView(FormView):
    template_name = 'authentication/forgot_password.html'
    form_class = ForgotPasswordForm
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        messages.success(self.request, "Password reset instructions have been sent to your registered physician email address.")
        return redirect('accounts:login')

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'authentication/change_password.html'
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):
        messages.success(self.request, "Your password has been changed successfully.")
        return super().form_valid(form)

class ProfileView(LoginRequiredMixin, View):
    template_name = 'profile/profile.html'

    def get(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        form = UserProfileForm(instance=profile, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })
        return render(request, self.template_name, {'form': form, 'profile': profile})

    def post(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            request.user.first_name = form.cleaned_data.get('first_name', request.user.first_name)
            request.user.last_name = form.cleaned_data.get('last_name', request.user.last_name)
            request.user.email = form.cleaned_data.get('email', request.user.email)
            request.user.save()
            form.save()
            messages.success(request, "Your physician profile has been updated successfully.")
            return redirect('accounts:profile')
        return render(request, self.template_name, {'form': form, 'profile': profile})
