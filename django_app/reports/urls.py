from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('generate/<int:diagnosis_id>/', views.GenerateReportView.as_view(), name='generate'),
    path('<int:pk>/', views.ReportDetailView.as_view(), name='detail'),
    path('<int:pk>/pdf/', views.ReportPDFView.as_view(), name='pdf'),
    path('history/', views.ReportHistoryListView.as_view(), name='history'),
    path('<int:pk>/delete/', views.ReportDeleteView.as_view(), name='delete'),
]
