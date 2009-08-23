from django.db import models
from markdown import markdown

class News(models.Model):
    slug = models.SlugField(unique=True, help_text="Autogenerated from title. Must be unique.")
    title = models.CharField(max_length=50)
    pub_date = models.DateTimeField(editable=False, auto_now_add=True)
    content = models.TextField(help_text="You can use Markdown syntax (http://daringfireball.net/projects/markdown/syntax).")
    content_html = models.TextField(editable=False, blank=True)
    
    @models.permalink
    def get_absolute_url(self):
        return ('news_news_detail', (), {'slug': self.slug })

    def __unicode__(self):
        return self.title
    
    def save(self, force_insert=False, force_update=False):
        self.content_html = markdown(self.content)
        super(News, self).save(force_insert, force_update)

    
    class Meta:
        verbose_name_plural = "news"
        ordering = ['-pub_date']
