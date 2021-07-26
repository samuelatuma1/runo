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
    display = models.BooleanField(default=True)
    event = models.CharField(max_length=150, default='what event is happening on this date')
    
    def __str__(self):
        return f'{self.date}, {self.event}'


class FooterDetails(models.Model):
    school_name = models.CharField(max_length=100)
    school_address = models.CharField(max_length=250)
    school_phone = models.CharField(max_length=18)
    school_email = models.EmailField()
    #school_direction = models.CharField(max_length=400)
    
    def __str__(self):
        return self.school_name
    

class Gallery(models.Model):
    galleryImage = models.ImageField(upload_to='gallery/')
    name = models.CharField(max_length=60)
    desc = models.CharField(max_length=250)
    display = models.BooleanField(default=True)
    uploaded = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    
class AboutSchool(models.Model):
    img = models.ImageField(upload_to='about/')
    desc = models.CharField(max_length=250, default='Image description')
    title = models.CharField(max_length=250, default='Title')
    aboutBody = models.TextField()
    publish = models.BooleanField(default=False)
    published = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-published']
    
    def __str__(self):
        return self.title
        
        
class Academics(models.Model):
    img = models.ImageField(upload_to='about/')
    desc = models.CharField(max_length=250, default='Image description')
    title = models.CharField(max_length=250, default='Title')
    aboutBody = models.TextField()
    publish = models.BooleanField(default=False)
    published = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-published']
        
    def __str__(self):
        return self.title
    

from django.contrib.auth.models import Group, Permission, User
class Users(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        permissions = [
            ('is_teacher', 'is_teacher'),
            ('is_pupil', 'is_pupil')
        ]
        
        
        
class UserClass(models.Model):
    user = models.ManyToManyField(User, related_query_name='classes')
    in_class = models.BooleanField(default=True)
    classes = [('1', 'Pre-Nursery'), ('2', 'Nursery 1'), ('3', 'Nursey 2'), ('3', 'Nursery 3')]
    Class = models.CharField(max_length=30, choices=classes, default='1')
    prev_classes = models.CharField(max_length=250, blank=True, null=True)
    
    def __str__(self):
        return f'{self.user}, {self.Class}'