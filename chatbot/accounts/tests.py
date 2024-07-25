from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from accounts.models import Profile


class RegisterViewTests(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('auth:register'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('auth:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    # Add more tests for form submission, etc.

class LoginViewTests(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('auth:login'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('auth:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    # Add more tests for login functionality, etc.

class ProfileViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user for testing the profile view
        User = get_user_model()
        cls.user = User.objects.create_user(username='testuser', password='12345')

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='testuser', password='12345')
        # Corrected to test the profile view URL, assuming 'auth:profile' is the correct namespace and name for the profile view
        response = self.client.get(reverse('auth:profile', args=[self.user.username]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('auth:profile', args=[self.user.username]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')


class UserModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')

    def test_user_creation(self):
        self.assertTrue(isinstance(self.user, get_user_model()))
        self.assertEqual(self.user.__str__(), 'testuser')

class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testprofile', password='12345')
        self.profile = Profile.objects.create(
            user=self.user,
            bio='Test Bio',
            avatar=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'),
            birthdate='2000-01-01',
            emotion='happy',
            location='Test Location',
            language='English'
        )

    def test_profile_creation(self):
        self.assertTrue(isinstance(self.profile, Profile))
        self.assertEqual(self.profile.__str__(), self.user.__str__())
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.bio, 'Test Bio')
        self.assertEqual(self.profile.emotion, 'happy')
        self.assertEqual(self.profile.location, 'Test Location')
        self.assertEqual(self.profile.language, 'English')