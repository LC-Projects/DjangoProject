from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

# Assuming you have a model named Chat for creating test instances
from .models import Chat, Category


class ChatFilterViewTests(TestCase):

    def setUp(self):
        # Create a test user
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        # Log in the test user
        self.client.login(username='testuser', password='testpass')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/chats/list/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('chats:chat_list'))
        self.assertEqual(response.status_code, 200)
        # Update the template name according to your project structure
        self.assertTemplateUsed(response, 'chats/home.html')

class ChatDetailViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user and chat instance for testing the detail view
        User = get_user_model()
        test_user = User.objects.create_user(username='testuser', password='12345')
        category = Category.objects.create(name='Test Category')
        Chat.objects.create(name='Test Chat', user=test_user, category=category)

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='testuser', password='12345')
        # Assuming the first chat has id=1
        response = self.client.get('/chats/detail/1/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('chats:chat_detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        # Update the template name according to your project structure
        self.assertTemplateUsed(response, 'chats/chat_detail.html')

class PublicChatDetailViewTests(TestCase):
    # Similar setup and tests as ChatDetailViewTests, adjusted for public chats
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        test_user = User.objects.create_user(username='testuser2', password='54321')
        category = Category.objects.create(name='Test Category')
        Chat.objects.create(name='Public Test Chat', user=test_user, is_private=False, category=category)

    def test_view_url_exists_at_desired_location(self):
        # Assuming the public chat has id=2
        response = self.client.get('/chats/public/detail/1/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('chats:public_chat_detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        # Update the template name according to your project structure
        self.assertTemplateUsed(response, 'chats/public_chat_detail.html')
