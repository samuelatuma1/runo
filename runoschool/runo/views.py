from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
import datetime

from .models import Intro, News, ImportantDates, FooterDetails, Gallery, AboutSchool, Academics, UserClass, Result, AllResults
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
    aboutSchool = FooterDetails.objects.first()
    context = {'form': form, 'form2': form2, 'section': 'register', 'aboutSchool': aboutSchool}
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
                
                
                
                
                if user_type == 'is_teacher':
                    class_for_user = UserClass(Class=user_class, is_student=False, is_teacher=True)
                    class_for_user.save()
                    class_for_user.users.add(new_user)
                    class_for_user.save()
                    new_user.groups.add(teacher_group)
                    
                    msg = 'User registered as teacher'
                    
                elif user_type == 'is_student':
                    
                    class_for_user = UserClass(Class=user_class, is_student=True)
                    class_for_user.save()
                    class_for_user.users.add(new_user)
                    class_for_user.save()
                    result = Result(user=new_user, current_class=user_class)
                    result.save()
                    
                    new_user.groups.add(pupil_group)
                    msg = 'User registered as pupil'
                    
                elif user_type == 'not_sure':
                    class_for_user = UserClass(Class=user_class, is_student=False)
                    class_for_user.save()
                    class_for_user.users.add(new_user)
                    class_for_user.save()
                    msg = 'User saved, but has not ben assigned a role'
                
                context['error_msg'] = msg
                return render(request, 'registration/login.html', context) 
                
                
        
    return return_file

aboutSchool = FooterDetails.objects.first()
# @login_required
# @permission_required('runo.is_teacher')
# @permission_required('runo.is_pupil')

all_classes = [('1', 'Pre-Nursery'), ('2', 'Nursery 1'), ('3', 'Nursery 2'), ('4', 'Nursery 3'),
               ('5', 'Basic 1'), ('6', 'Basic 2'), ('7', 'Basic 3'), ('8', 'Basic 4'),
               ('9', 'Basic 5'), ('10', 'Basic 6')]

from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage

@permission_required('runo.is_teacher')
def teacher(request):
    
    
    aboutSchool = FooterDetails.objects.first()
    try:
        Class = request.user.userclass_set.first().Class
        #return HttpResponse(Class)
        class_name = all_classes[int(Class) -1][1]
        
        Users = UserClass.objects.filter(in_class=True, Class=Class, is_student=True).filter().all() or []
        
        
        paginator = Paginator(Users, 15)
        page = request.GET.get('page')
        try:
            Users = paginator.page(page)
        except PageNotAnInteger:
            Users = paginator.page(1)
        except EmptyPage:
            Users = paginator.page(paginator.num_pages)
            
        context =  {'page': page, 'Class': Class, 'class_name': class_name, 'Users':Users, 'aboutSchool': aboutSchool}
        
        return render(request, 'runo/sms/class.html', context)
    except:
        return HttpResponse('User Does not Have a specified class')
    
    



@permission_required('runo.is_teacher')
def result(request, Class, username):
    pupil_class = Class
    pupil = get_object_or_404(User, username=username)
    success_msg = None
    
    is_class_teacher = False
    teacher_class = None
    
    try:
        teacher_class = request.user.userclass_set.first().Class
        #return HttpResponse(f'{teacher_class} {Class}')
    
    except:
        pass
    
    if teacher_class == Class:
        is_class_teacher = True
        
    if request.method == 'POST':
        try:
            result_file = request.FILES['resultFile']
            result_for = request.POST['resultFor']
            
            former_result = AllResults.objects.filter(student=pupil, term=result_for, Class=pupil_class).first()
            if former_result is not None:
                former_result.result = result_file
                former_result.save()
            else:
                add_result = AllResults(student=pupil, term=result_for, Class=pupil_class, result=result_file)
                add_result.save()
                
            res = Result.objects.get(user=pupil)
            results = eval(res.results)
            new_result = AllResults.objects.filter(student=pupil, term=result_for, Class=pupil_class).first()
            
            for result in results:
                if result['Class'] == pupil_class:
                    result[result_for] = new_result.result.url
            
            res.results = str(results)
            
            res.save()     
            
            success_msg = f'Successfully uploaded {result_for} result for {pupil}'
            
        except:
            errorMsg = 'You attempted to submit an empty result'
            href= reverse('runo:result', args=[Class, username])
            return render(request, 'error.html', {'is_class_teacher': is_class_teacher, 'errorMsg': errorMsg, 'href': href})
        
    
    
        
        
    res = Result.objects.get(user=pupil)
    results = eval(res.results)
    has_result = False
    pupil_result = None
    for result in results:
        if result['Class'] == Class:
            has_result = True
            pupil_result = result
    
    if not has_result:
        result_for = {
            'Class': Class
        }
        pupil_result = result_for
        results.append(result_for)
    
    res.results = str(results)
    res.save()
    class_name = all_classes[int(pupil_class) -1][1]
    
    Users = UserClass.objects.filter(in_class=True, Class=Class, is_student=True).filter().all() or []
    
    
    
    context =  {'is_class_teacher': is_class_teacher, 'pupil':pupil, 'Class': Class, 'class_name': class_name, 'Users': Users, 'result': pupil_result, 'aboutSchool': aboutSchool, 'success_msg': success_msg}
    return render (request, 'runo/sms/pupilResult.html', context)
    return HttpResponse(f'Welcome {username} in class {res.results}')

@permission_required('runo.is_teacher')
def result_page(request, Class, username):
    return HttpResponse(f'Welcome {username} in class {Class}')

@permission_required('runo.is_teacher')
def changeclass(request, Class, username, status):
    return HttpResponse(f'{status}, {username}, {Class}')