from django.test import TestCase
from news.models import News

class NewsTest(TestCase):
    def test_basic_addition(self):
        news = News(title="Mama are mere", content="Test de continut")
        self.failUnlessEqual(str(news), "Mama are mere")

    def test_feed_content(self):
        response = self.client.get('/feeds/news/')
        self.failUnlessEqual(response.status_code, 200)
        self.failUnlessEqual(response.content.count('<title>'), 1)
        self.failUnlessEqual(response.content.count('<description>'), 1)

