from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class AccountsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testdoctor',
            email='testdoctor@oncovision.med',
            password='password123',
            first_name='Sarah',
            last_name='Jenkins'
        )

    def test_login_view(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('accounts:login'), {
            'username': 'testdoctor',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)

    def test_profile_view(self):
        self.client.login(username='testdoctor', password='password123')
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)
