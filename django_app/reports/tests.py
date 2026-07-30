from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from patients.models import Patient
from diagnosis.models import Diagnosis
from reports.models import MedicalReport

class ReportsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='doc', password='pwd')
        self.patient = Patient.objects.create(
            first_name='Sofia', last_name='Rodriguez', age=46, gender='Female', blood_group='B+', phone='+15554321098'
        )
        self.diagnosis = Diagnosis.objects.create(
            patient=self.patient, cancer_type='Breast Cancer', prediction='Cancerous', confidence=97.2
        )
        self.report = MedicalReport.objects.create(
            diagnosis=self.diagnosis, report_number='REP-2026-9999', doctor_notes='Test notes', treatment_guidelines='Test guidelines'
        )

    def test_report_detail_view(self):
        self.client.login(username='doc', password='pwd')
        response = self.client.get(reverse('reports:detail', kwargs={'pk': self.report.pk}))
        self.assertEqual(response.status_code, 200)

    def test_report_history_view(self):
        self.client.login(username='doc', password='pwd')
        response = self.client.get(reverse('reports:history'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'REP-2026-9999')
