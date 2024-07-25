from django.test import TestCase
from django.urls import reverse


# Create your tests here.
class HomeViewTests(TestCase):
    def test_home_view(self):
        response = self.client.get(reverse('home:home'))
        self.assertEqual(response.status_code, 200)

    def test_about_view(self):
        response = self.client.get(reverse('home:about'))
        self.assertEqual(response.status_code, 200)

    def test_licensing_view(self):
        response = self.client.get(reverse('home:licensing'))
        self.assertEqual(response.status_code, 200)

    def test_privacy_view(self):
        response = self.client.get(reverse('home:privacy'))
        self.assertEqual(response.status_code, 200)