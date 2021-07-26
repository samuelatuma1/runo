from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
import datetime

from .models import Intro, News, ImportantDates, FooterDetails, Gallery, AboutSchool, Academics, UserClass
from .forms import UserClassName

# Create your views here.
def index(request):
    introImgs = Intro.objects.all().order_by('-uploaded')[:1]
    news = News.objects.filter(publish=True).order_by('-published').all()[:6]
    dates = ImportantDates.objects.all().order_by('date')[:12]
    aboutSchool = FooterDetails.objects.first()
    
    
    # Show upcoming events 14 days prior
    upcoming_event = None
    if len(dates) > 0:
        closest_event = 100000
        for upcoming in dates:
            
            time = ( datetime.date(upcoming.date.year, upcoming.date.month, upcoming.date.day) - datetime.date.today()).days
            if time < closest_event and time > -1:
                closest_event = time
            if time < 14 and time <= closest_event and time > -1:
                upcoming_event = {'upcoming': upcoming, 'time': time }
            
    if len(introImgs) > 0:
        introImg = []
        for intro in introImgs:
            details = {
                'img': intro.img.url,
                'schoolName': intro.schoolName,
                'desc': intro.desc
            }
            introImg.append(details)
            
        return render(request, 'runo/index.html', {'section': 'home', 
                                                   'introImg': introImg,
                                                   'news': news, 'upcoming_event': upcoming_event,
                                                   'dates': dates, 'aboutSchool': aboutSchool})

    return render(request, 'runo/index.html', {'section': 'home', 'news': news,
                                               'upcoming_event': upcoming_event,
                                               'dates': dates, 'aboutSchool': aboutSchool})


def news(request, slug, year, month, day):
    newsItem = News.objects.filter(slug=slug, published__day=day,
                                 published__month=month, published__year=year).first()
    
    news = News.objects.filter(publish=True).order_by('-published').all()[:6]
    aboutSchool = FooterDetails.objects.first()
    return render(request, 'runo/news.html', {'aboutSchool': aboutSchool, 'newsItem': newsItem, 'news': news})


def gallery(request):
    gallery = Gallery.objects.filter(display=True).order_by('-uploaded').all()
    aboutSchool = FooterDetails.objects.first()
    return render(request, 'runo/gallery.html', {'galleries': gallery, 'aboutSchool': aboutSchool})



def aboutUs(request):
    newsItem = AboutSchool.objects.order_by('-published').first()
    news = News.objects.filter(publish=True).order_by('-published').all()[:6]
    aboutSchool = FooterDetails.objects.first()
    return render(request, 'runo/about.html', {'aboutSchool': aboutSchool, 'newsItem': newsItem, 'news': news, 'section': 'about'})

from django.contrib.auth.models import Group, Permission
from django.contrib.auth.decorators import login_required, permission_required


def academics(request):
    newsItem = Academics.objects.order_by('-published').first()
    news = News.objects.filter(publish=True).order_by('-published').all()[:6]
    aboutSchool = FooterDetails.objects.first()
    
    return render(request, 'runo/about.html', {'aboutSchool': aboutSchool, 'newsItem': newsItem, 'news': news, 'section': 'academics'})



# Student Management System
from .models import Users
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from .forms import Register

teacher_group, created = Group.objects.get_or_create(name='teacher_group')
ct = ContentType.objects.get_for_model(Users)
                
permission = Permission.objects.filter(codename='is_teacher', name='is_teacher', content_type=ct).first()
teacher_group.permissions.add(permission)


pupil_group, created = Group.objects.get_or_create(name='pupil_group')
Content_type = ContentType.objects.get_for_model(Users)
pupil_permission = Permission.objects.filter(codename='is_pupil', name='is_pupil', content_type=Content_type).first()
pupil_group.permissions.add(pupil_permission)

def register(request):
    form = Register()
    form2 = UserClassName()
    context = {'form': form, 'form2': form2, 'section': 'register'}
    return_file = render(request, 'registration/login.html', context)
    if request.method == 'POST':
        form = Register(request.POST)
        form2 = UserClassName(data=request.POST)
        if form.is_valid() and form2.is_valid():
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            email = form.cleaned_data['email']
            used_email = User.objects.filter(email=email).first()
            user_type = form.cleaned_data['usertype']
            user_class = form2.cleaned_data['Class']
            
            if used_email:
                context['error_msg'] = 'Email address already in use'
                return render(request, 'registration/login.html', context)
                
            if password1 != password2:
                context['error_msg'] = 'Passwords do not match'
                return render(request, 'registration/login.html', context)
            elif len(password1) < 6:
                context['error_msg'] = 'password must be at least six characters long'
                return render(request, 'registration/login.html', context)
            
            else:
                new_user = form.save(commit=False)
                new_user.set_password(password1)
                
                new_user.save()
                
                class_for_user = UserClass(Class=user_class)
                class_for_user.save()
                class_for_user.user.add(new_user)
                class_for_user.save()
                
                
                user_class = UserClass.objects.all()
                allUsers = []
                for user in user_class:
                    allUsers.append(user.user.first().username)
                    
                return  HttpResponse(f'{allUsers}')
                
                
                if user_type == 'is_teacher':
                    new_user.groups.add(teacher_group)
                    msg = 'User registered as teacher'
                elif user_type == 'is_student':
                    new_user.groups.add(pupil_group)
                    msg = 'User registered as pupil'
                
                context['error_msg'] = msg
                return render(request, 'registration/login.html', context) 
                
                
        
    return return_file


# @login_required
# @permission_required('runo.is_teacher')
# @permission_required('runo.is_pupil')
