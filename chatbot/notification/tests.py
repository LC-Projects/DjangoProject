from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from chats.models import Chat, Category
from notification.models import Notification


class NotificationURLsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user and chat instance for testing the detail view
        User = get_user_model()
        test_user = User.objects.create_user(username='testuser', password='12345')

    def test_notification_list_url(self):
        self.client.login(username='testuser', password='12345')
        # Test the URL for the notification list view
        response = self.client.get(reverse('notification:notification_list'))
        self.assertEqual(response.status_code, 200)

    def test_create_notification_url(self):
        self.client.login(username='testuser', password='12345')
        # Test the URL for the create notification view
        response = self.client.get(reverse('notification:create'))
        self.assertEqual(response.status_code, 200)

        self.client.logout()
        # Replace the assertTemplateUsed with assertRedirects
        # Assuming 'home:home' is the name of your home page URL
        response = self.client.get(reverse('notification:create'))
        self.assertRedirects(response, f"{reverse('auth:login')}?next={reverse('notification:create')}", status_code=302, target_status_code=200)


class NotificationModelTest(TestCase):
    def setUp(self):
        # Create a user instance for testing
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')

        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )

        self.chat = Chat.objects.create(
            name='Test Chat',
            user=self.user,
            category=self.category,
        )

        # Create a notification instance for testing
        self.notification = Notification.objects.create(
            title='Test Notification',
            description='This is a test notification.',
            user=self.user,
            slug='test-notification',
            chatId=self.chat,
        )

    def test_notification_creation(self):
        # Verify that the Notification instance exists and has the expected attributes
        self.assertTrue(isinstance(self.notification, Notification))
        self.assertEqual(self.notification.title, 'Test Notification')
        self.assertEqual(self.notification.description, 'This is a test notification.')
        self.assertEqual(self.notification.user, self.user)
        self.assertEqual(self.notification.chatId, self.chat)
        self.assertEqual(str(self.notification), 'Test Notification')