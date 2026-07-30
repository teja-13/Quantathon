from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from patients.models import Patient

class PatientsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='doc', first_name='Sarah', last_name='Jenkins', password='pwd')
        self.patient = Patient.objects.create(
            first_name='Eleanor',
            last_name='Vance',
            age=54,
            gender='Female',
            blood_group='A+',
            phone='+1 (555) 234-5678',
            doctor_name='Dr. Sarah Jenkins'
        )

    def test_patient_list_and_search(self):
        self.client.login(username='doc', password='pwd')
        response = self.client.get(reverse('patients:list') + '?q=Eleanor')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Eleanor Vance')

    def test_patient_detail(self):
        self.client.login(username='doc', password='pwd')
        response = self.client.get(reverse('patients:detail', kwargs={'pk': self.patient.pk}))
        self.assertEqual(response.status_code, 200)

    def test_patient_create_defaults_doctor(self):
        self.client.login(username='doc', password='pwd')
        response = self.client.get(reverse('patients:add'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dr. Sarah Jenkins')

        response = self.client.post(reverse('patients:add'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'age': 45,
            'gender': 'Male',
            'blood_group': 'O+',
            'phone': '+1555000111',
            'doctor_name': 'Dr. Sarah Jenkins',
        })
        self.assertEqual(response.status_code, 302)
        new_patient = Patient.objects.get(first_name='John', last_name='Doe')
        self.assertEqual(new_patient.doctor_name, 'Dr. Sarah Jenkins')
