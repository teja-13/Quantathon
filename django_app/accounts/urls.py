from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('change-password/', views.CustomPasswordChangeView.as_view(), name='change_password'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]
