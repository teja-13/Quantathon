from django.urls import path
from . import views

app_name = 'diagnosis'

urlpatterns = [
    path('', views.UploadDiagnosisView.as_view(), name='index'),
    path('select/', views.UploadDiagnosisView.as_view(), name='select'),
    path('upload/', views.UploadDiagnosisView.as_view(), name='upload'),
    path('cards/', views.CancerSelectionView.as_view(), name='cards'),
    path('<int:pk>/processing/', views.ProcessingView.as_view(), name='processing'),
    path('<int:pk>/result/', views.PredictionResultView.as_view(), name='result'),
    path('<int:pk>/explainability/', views.ExplainabilityView.as_view(), name='explainability'),
]
