from django.test import TestCase
from news.models import News

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
        self.failUnlessEqual(response.content, '\n\n<h1>Mama are mere</h1>\n<p>Sat 15 Aug 2009 -\n  15:20</p>\n\n\n')