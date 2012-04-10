from django.test import TestCase
from news.models import News
from datetime import datetime

class NewsTest(TestCase):
    def setUp(self):
        self.news = News.objects.create(title="Mama are mere", slug="mama-are-mere", content="Test de continut")

    def test_basic_addition(self):
        self.failUnlessEqual(str(self.news), "Mama are mere")

    def test_feed_content(self):
        response = self.client.get('/feeds/news/')
        self.failUnlessEqual(response.status_code, 200)
        self.failUnlessEqual(response.content.count('<title>'), 2)
        self.failUnlessEqual(response.content.count('<description>'), 2)

    def test_list(self):
        response = self.client.get('/news/')
        self.failUnlessEqual(response.status_code, 200)
        self.failUnlessEqual(response.content.count('<li>'), 1)

    def test_detail(self):
        response = self.client.get('/news/mama-are-mere/')
        self.failUnlessEqual(response.status_code, 200)
        self.assertTrue('<h1>Mama are mere</h1>' in response.content)
        self.assertTrue('<p>Test de continut</p>' in response.content)
        
    def test_save(self):
            self.failUnlessEqual(self.news.content_html, '<p>Test de continut</p>')

    def test_is_fresh_fresh(self):
        self.assertTrue(self.news.is_fresh())
        
    def test_is_fresh_old(self):
        old_news = News.objects.create(title="Old news", slug="old_news", content="continut vechi")
        old_news.pub_date = datetime(2007, 7, 15, 12, 00, 53)
        self.assertFalse(old_news.is_fresh())
    