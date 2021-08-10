from django.contrib import admin
from .models import Intro, News, ImportantDates, FooterDetails, Gallery, AboutSchool
from .models import Academics, UserClass, Result, UserProfile
# Register your models here.
@admin.register(Intro)
class adminIntro(admin.ModelAdmin):
    list_display = ['schoolName', 'img', 'desc']
    ordering = ['-uploaded']
    

@admin.register(News)
class adminNews(admin.ModelAdmin):
    list_display = ['title', 'newsBody', 'desc', 'publish']
    prepopulated_fields = {'slug': ['title']}
    search_fields = ['title', 'newsBody']
    ordering = ['-published']
    
@admin.register(AboutSchool)
class adminAboutSchool(admin.ModelAdmin):
    list_display = ['title', 'aboutBody', 'desc', 'publish']
    search_fields = ['title', 'aboutBody']
    ordering = ['-published']
    
admin.site.register(ImportantDates)

admin.site.register(FooterDetails)

@admin.register(Gallery)
class adminGallery(admin.ModelAdmin):
    list_display = ['name', 'galleryImage',  'desc', 'display']
    search_fields = ['name', 'desc']
    ordering = ['-uploaded']
    
@admin.register(Academics)
class AdminAcademic(admin.ModelAdmin):
    list_display = ['title', 'aboutBody', 'desc', 'publish']
    search_fields = ['title', 'aboutBody']
    ordering = ['-published']
    
#admin.site.register(Result)
#admin.site.register(UserProfile)