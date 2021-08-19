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
        verbose_name_plural = 'News'
        
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
    
    class Meta:
        verbose_name_plural = 'Important Dates'
    def __str__(self):
        return f'{self.date}, {self.event}'


class FooterDetails(models.Model):
    school_name = models.CharField(max_length=100)
    school_address = models.CharField(max_length=250)
    school_phone = models.CharField(max_length=18)
    school_email = models.EmailField()
    #school_direction = models.CharField(max_length=400)
    
    class Meta:
        verbose_name_plural = 'Footer Details'
        
    def __str__(self):
        return self.school_name
        
    

class Gallery(models.Model):
    galleryImage = models.ImageField(upload_to='gallery/')
    name = models.CharField(max_length=60)
    desc = models.CharField(max_length=250)
    display = models.BooleanField(default=True)
    uploaded = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Gallery'
    
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
        verbose_name_plural = 'AboutSchool'
    
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
        verbose_name_plural = 'Academics'
        
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
        
        
from datetime import date      
class UserClass(models.Model):
    users = models.ManyToManyField(User, related_query_name='classes') # use userclass_set to query from users
    in_class = models.BooleanField(default=True)
    is_student = models.BooleanField(default=True)
    is_teacher = models.BooleanField(default=False)
    classes = [('1', 'Pre-Nursery'), ('2', 'Nursery 1'), ('3', 'Nursery 2'), ('4', 'Nursery 3'),
               ('5', 'Basic 1'), ('6', 'Basic 2'), ('7', 'Basic 3'), ('8', 'Basic 4'),
               ('9', 'Basic 5'), ('10', 'Basic 6')]
    Class = models.CharField(max_length=30, choices=classes, default='1')
    #prev_classes = models.CharField(max_length=250, blank=True, null=True)
    
    def __str__(self):
        return f'{self.users}, {self.Class}'
    
class Result(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='results')
    current_class = models.CharField(max_length=15)
    DOB = models.DateField(blank=True, null=True)
    
    results = models.CharField(max_length=2000, default='[]')
    
    @property
    def age(self):
        today = date.today()
        plus_one_pseudo = 1 if (today.month, today.day) < (self.DOB.month, self.DOB.day) else 0
        
        return today.year - self.DOB.year - plus_one_pseudo
    def __str__(self) :
        return self.user, self.current_class
     
class AllResults(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    term = models.CharField(max_length=50)
    Class = models.CharField(max_length=25)
    result = models.FileField(upload_to='results/')
    
    def __str__(self):
        return f'{self.student.username}, {self.term}, {self.Class} result'
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, models.CASCADE, related_name='userprofile')
    profile_image = models.ImageField(upload_to='users/', blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    DOB = models.DateField(blank=True, null=True)
    
    @property
    def age(self):
        if self.DOB is not None:
            today = date.today()
            plus_one_pseudo = 1 if (today.month, today.day) < (self.DOB.month, self.DOB.day) else 0
            
            return today.year - self.DOB.year - plus_one_pseudo
        else:
            return 'No date of birth specified'
    
    def __str__(self):
        return self.user.username


class Message(models.Model):
    sent = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=150, blank=True, null=True)
    message = models.TextField()
    reply = models.TextField(blank=True, null=True)
    replied = models.BooleanField(default=False)
    
    def get_absolute_url(self):
        return reverse('runo:msg_for_admin', args=[self.id])
    
class MessageAllUsers(models.Model):
    title = models.CharField(max_length=200, blank=True)
    message = models.TextField()