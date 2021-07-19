from django.db import models
from django.urls import reverse
# Create your models here.
class Intro(models.Model):
    schoolName = models.CharField(max_length=50, default='RUNO DAYSPRING SCHOOL')
    img = models.ImageField(upload_to='intro/')
    desc = models.TextField()
    uploaded = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded']
        
    def __str__(self):
        return self.schoolName
        
        
class News(models.Model):
    img = models.ImageField(upload_to='news/')
    desc = models.CharField(max_length=250, default='short description of the news')
    title = models.CharField(max_length=250, default='News title')
    slug = models.SlugField(max_length=250)
    newsBody = models.TextField()
    publish = models.BooleanField(default=False)
    published = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-published']
        
    def get_absolute_url(self):
        return reverse('runo:news', args=[
            self.slug,
            self.published.year,
            self.published.month,
            self.published.day
        ])
        
    def __str__(self):
        return self.title
    
    
class ImportantDates(models.Model):
    date = models.DateField()
    event = models.CharField(max_length=150, default='what event is happening on this date')
    
    def __str__(self):
        return f'{self.date}, {self.event}'


class FooterDetails(models.Model):
    school_name = models.CharField(max_length=100)
    school_address = models.CharField(max_length=250)
    school_phone = models.CharField(max_length=18)
    school_email = models.EmailField()
    school_address = models.CharField(max_length=400)
    
    def __str__(self):
        return self.school_name