from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

# Assuming you have a model named Chat for creating test instances
from .models import Chat, Category, Comment, Message


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


class CategoryModelTest(TestCase):
    def test_category_creation(self):
        category = Category.objects.create(name='Test Category')
        self.assertEqual(category.name, 'Test Category')
        self.assertTrue(category.slug)
        self.assertEqual(str(category), 'Test Category')

class MessageModelTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(username='testuser', password='testpass')
        category = Category.objects.create(name='Test Category')
        chat = Chat.objects.create(name='Test Chat', user=user, category=category)
        self.message = Message.objects.create(chat=chat, content='Test Message', is_bot=False)

    def test_message_creation(self):
        self.assertEqual(self.message.content, 'Test Message')
        self.assertFalse(self.message.is_bot)
        self.assertTrue(str(self.message).startswith('Test Chat'))

class ChatModelTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(username='testuser', password='testpass')
        category = Category.objects.create(name='Test Category')
        self.chat = Chat.objects.create(name='Test Chat', user=user, category=category)

    def test_chat_creation(self):
        self.assertEqual(self.chat.name, 'Test Chat')
        self.assertTrue(self.chat.is_private)
        self.assertEqual(str(self.chat), 'Test Chat')

class CommentModelTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(username='testuser', password='testpass')
        category = Category.objects.create(name='Test Category')
        chat = Chat.objects.create(name='Test Chat', user=user, category=category)
        self.comment = Comment.objects.create(chat=chat, user=user, content='Test Comment')

    def test_comment_creation(self):
        self.assertEqual(self.comment.content, 'Test Comment')
        self.assertEqual(str(self.comment), 'Test Chat-testuser')