from models import News
from django.contrib import admin

class NewsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = [
        (None,               {'fields': ['title','slug', 'content']}),
    ]
    list_display = ('title', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['content']
    date_hierarchy = 'pub_date'

admin.site.register(News, NewsAdmin)
