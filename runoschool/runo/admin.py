from django.contrib import admin
from .models import Intro, News, ImportantDates
# Register your models here.
@admin.register(Intro)
class adminIntro(admin.ModelAdmin):
    list_display = ['schoolName', 'img', 'desc']
    ordering = ['-uploaded']
    

@admin.register(News)
class adminNews(admin.ModelAdmin):
    list_display = ['img', 'title', 'newsBody', 'desc', 'publish']
    prepopulated_fields = {'slug': ['title']}
    search_fields = ['title', 'newsBody']
    ordering = ['-published']
    
admin.site.register(ImportantDates)
