from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from feedback.models import Feedback


class FeedbackURLsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user and chat instance for testing the detail view
        User = get_user_model()
        cls.test_superuser = User.objects.create_user(username='testsuperuser', password='12345', is_superuser=True)
        cls.test_user = User.objects.create_user(username='testuser', password='12345')
        feedback = Feedback.objects.create(email='test@gmail.com', subject='Test feedback', description='Test Description')

    def test_contact_url(self):
        response = self.client.get(reverse('feedback:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feedback/contact.html')

    def test_feedback_list_url(self):
        self.client.login(username='testsuperuser', password='12345')
        response1 = self.client.get(reverse('feedback:feedback_list'))
        self.assertEqual(response1.status_code, 200)
        self.assertTemplateUsed(response1, 'feedback/feedback_list.html')

        self.client.logout()
        self.client.login(username='testuser', password='12345')
        response2 = self.client.get(reverse('feedback:feedback_list'))
        # Replace the assertTemplateUsed with assertRedirects
        # Assuming 'home:home' is the name of your home page URL
        self.assertRedirects(response2, reverse('home:home'), status_code=302, target_status_code=200)

    def test_feedback_detail_url(self):
        self.client.login(username='testsuperuser', password='12345')
        response1 = self.client.get(reverse('feedback:feedback_detail', args=[1]))
        self.assertEqual(response1.status_code, 200)
        self.assertTemplateUsed(response1, 'feedback/feedback_detail.html')

        self.client.logout()
        self.client.login(username='testuser', password='12345')
        response2 = self.client.get(reverse('feedback:feedback_detail', args=[1]))
        # Replace the assertTemplateUsed with assertRedirects
        # Assuming 'home:home' is the name of your home page URL
        self.assertRedirects(response2, reverse('home:home'), status_code=302, target_status_code=200)

class FeedbackModelTest(TestCase):
    def setUp(self):
        # Create a Feedback instance for testing
        self.feedback = Feedback.objects.create(email='test@example.com', subject='Test Subject', description='Test Description')

    def test_feedback_creation(self):
        # Verify that the Feedback instance exists and has the expected attributes
        self.assertTrue(isinstance(self.feedback, Feedback))
        self.assertEqual(self.feedback.email, 'test@example.com')
        self.assertEqual(self.feedback.subject, 'Test Subject')
        self.assertEqual(self.feedback.description, 'Test Description')
