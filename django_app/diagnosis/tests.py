from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from patients.models import Patient
from diagnosis.models import Diagnosis

class DiagnosisTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='doc', password='pwd')
        self.patient = Patient.objects.create(
            first_name='Arthur', last_name='Pendelton', age=62, gender='Male', blood_group='O+', phone='+15558765432'
        )
        self.diagnosis = Diagnosis.objects.create(
            patient=self.patient,
            cancer_type='Brain Cancer',
            prediction='Cancerous',
            confidence=96.4
        )

    def test_cancer_selection_view(self):
        self.client.login(username='doc', password='pwd')
        response = self.client.get(reverse('diagnosis:select'))
        self.assertEqual(response.status_code, 200)

    def test_prediction_result_view(self):
        self.client.login(username='doc', password='pwd')
        response = self.client.get(reverse('diagnosis:result', kwargs={'pk': self.diagnosis.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'CANCEROUS')

    def test_explainability_view(self):
        self.client.login(username='doc', password='pwd')
        response = self.client.get(reverse('diagnosis:explainability', kwargs={'pk': self.diagnosis.pk}))
        self.assertEqual(response.status_code, 200)
