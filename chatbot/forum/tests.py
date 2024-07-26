from django.test import TestCase
from django.urls import reverse

class ForumURLsTest(TestCase):
    def test_all_forums_view_url(self):
        # Test the URL for the all forums view
        response = self.client.get(reverse('forum:home'))
        self.assertEqual(response.status_code, 200)

    def test_forum_by_category_view_url(self):
        # Test the URL for the forum by category view
        # Assuming there's a Category instance with a slug 'test-category'
        response = self.client.get(reverse('forum:home_slug', kwargs={'slug': 'test-category'}))
        self.assertEqual(response.status_code, 200)