from django.db import models


class News(models.Model):
    slug = models.SlugField(help_text="Autogenerated from title")
    title = models.CharField(max_length=50)
    pub_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    content_html = models.TextField()
    
    @models.permalink
    def get_absolute_url(self):
        return ('news_news_detail', (), {'slug': self.slug })

    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "news"
        ordering = ['-pub_date']