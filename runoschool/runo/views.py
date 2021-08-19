from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
import datetime
from django.core.mail import send_mail

from .models import Intro, News, ImportantDates, FooterDetails, Gallery, AboutSchool, Academics, UserClass, Result, AllResults
from .models import UserProfile, Message
from .forms import UserClassName, UserProfileForm
from django.db.models import Q

# Create your views here.

#def searchBase(request):
    
        
        
def index(request):
    introImgs = Intro.objects.all().order_by('-uploaded')[:1]
    news = News.objects.filter(publish=True).order_by('-published').all()[:6]
    dates = ImportantDates.objects.filter(date__gte=datetime.date.today()).order_by('date')[:12]
    aboutSchool = FooterDetails.objects.order_by('-id')[0]
    
    allNews = None
    if request.method == 'POST':
        searchData = request.POST['searchData']
        newsSearch = News.objects.filter(Q(title__icontains=searchData) | Q(newsBody__icontains=searchData) | Q(desc__icontains=searchData)).all() 
        events = ImportantDates.objects.filter(event__icontains=searchData).all()
        
        allNews = newsSearch
    
    
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
            
        return render(request, 'runo/index.html', {'section': 'home', 'allNews': allNews,
                                                   'introImg': introImg,
                                                   'news': news, 'upcoming_event': upcoming_event,
                                                   'dates': dates, 'aboutSchool': aboutSchool})

    return render(request, 'runo/index.html', {'section': 'home', 'news': news, 'allNews': allNews,
                                               'upcoming_event': upcoming_event,
                                               'dates': dates, 'aboutSchool': aboutSchool})


def news(request, slug, year, month, day):
    newsItem = News.objects.filter(slug=slug, published__day=day,
                                 published__month=month, published__year=year).first()
    
    news = News.objects.filter(publish=True).order_by('-published').all()[:6]
    aboutSchool = FooterDetails.objects.order_by('-id')[0]
    return render(request, 'runo/news.html', {'aboutSchool': aboutSchool, 'newsItem': newsItem, 'news': news})


def gallery(request):
    gallery = Gallery.objects.filter(display=True).order_by('-uploaded').all()
    aboutSchool = FooterDetails.objects.order_by('-id')[0]
    return render(request, 'runo/gallery.html', {'galleries': gallery, 'aboutSchool': aboutSchool})



def aboutUs(request):
    newsItem = AboutSchool.objects.filter(publish=True).order_by('-published').first()
    news = News.objects.filter(publish=True).order_by('-published').all()[:6]
    aboutSchool = FooterDetails.objects.order_by('-id')[0]
    return render(request, 'runo/about.html', {'aboutSchool': aboutSchool, 'newsItem': newsItem, 'news': news, 'section': 'about'})

from django.contrib.auth.models import Group, Permission
from django.contrib.auth.decorators import login_required, permission_required


def academics(request):
    newsItem = Academics.objects.order_by('-published').first()
    news = News.objects.filter(publish=True).order_by('-published').all()[:6]
    aboutSchool = FooterDetails.objects.order_by('-id')[0]
    
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

#@staff_member_required
def register(request):
    form = Register()
    form2 = UserClassName()
    aboutSchool = FooterDetails.objects.order_by('-id')[0]
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
                    
                    new_user_profile = UserProfile(user=new_user)
                    new_user_profile.save()
                    
                    msg = 'User registered as teacher'
                    
                elif user_type == 'is_student':
                    
                    class_for_user = UserClass(Class=user_class, is_student=True)
                    class_for_user.save()
                    class_for_user.users.add(new_user)
                    class_for_user.save()
                    result = Result(user=new_user, current_class=user_class)
                    result.save()
                
                    new_user.groups.add(pupil_group)
                    
                    new_user_profile = UserProfile(user=new_user)
                    new_user_profile.save()
                    
                    msg = 'User registered as pupil'
                    
                elif user_type == 'not_sure':
                    class_for_user = UserClass(Class=user_class, is_student=False)
                    class_for_user.save()
                    class_for_user.users.add(new_user)
                    class_for_user.save()
                    
                    new_user_profile = UserProfile(user=new_user)
                    new_user_profile.save()
                    
                    msg = 'User saved, but has not ben assigned a role'
                    
                    
                
                context['error_msg'] = msg
                return render(request, 'registration/login.html', context) 
                      
    return return_file

aboutSchool = FooterDetails.objects.order_by('-id')[0]
# @login_required
# @permission_required('runo.is_teacher')
# @permission_required('runo.is_pupil')

all_classes = [('1', 'Pre-Nursery'), ('2', 'Nursery 1'), ('3', 'Nursery 2'), ('4', 'Nursery 3'),
               ('5', 'Basic 1'), ('6', 'Basic 2'), ('7', 'Basic 3'), ('8', 'Basic 4'),
               ('9', 'Basic 5'), ('10', 'Basic 6')]

from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage

@permission_required('runo.is_teacher')
def teacher(request):
    
    
    aboutSchool = FooterDetails.objects.order_by('-id')[0]
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
            errorMsg = 'You attempted to submit an empty result. To return to previous page, '
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

@permission_required('runo.is_teacher')
def result_page(request, Class, username):
    return HttpResponse(f'Welcome {username} in class {Class}')

@permission_required('runo.is_teacher')
def changeclass(request, Class, username, status):
    is_class_teacher = False
    teacher_class = None
    new_class = None
    
    try:
        teacher_class = request.user.userclass_set.first().Class
        #return HttpResponse(f'{teacher_class} {Class}')
    
    except:
        pass
    
    if teacher_class == Class:
        is_class_teacher = True
    
    if is_class_teacher:
        pupil = User.objects.filter(username=username).first()
        pupil_classes = pupil.userclass_set.all()
    
        pupil_class = pupil_classes.filter(Class=teacher_class).first()
        if status == 'promote':
            #return HttpResponse(pupil_class.Class)
            pupil_class.in_class = False
            pupil_class.save()
            
            if int(teacher_class) < 10:
                
                new_class = str(int(teacher_class) + 1)
                
                was_in_class = pupil_classes.filter(Class=new_class).first()
                if was_in_class is not None:
                    was_in_class.in_class = True
                    was_in_class.save()
                else:
                    new_class_for_pupil = UserClass(Class=new_class, is_student=True)
                    new_class_for_pupil.save()
                    new_class_for_pupil.users.add(pupil)
                    new_class_for_pupil.save()
                
                
        elif status == 'demote':
            #return HttpResponse('demote') 
            pupil_class.in_class = False
            pupil_class.save()
            
            if int(teacher_class) > 1:
                new_class = str(int(teacher_class) - 1)
                
                was_in_class = pupil_classes.filter(Class=new_class).first()
                if was_in_class is not None:
                    was_in_class.in_class = True
                    was_in_class.save()
                else:
                    new_class_for_pupil = UserClass(Class=new_class, is_student=True)
                    new_class_for_pupil.save()
                    new_class_for_pupil.users.add(pupil)
                    new_class_for_pupil.save()
        
            #return HttpResponse(pupil_class.Class)
        
        
        href = reverse('runo:teacher', args=[])
        if new_class is not None:
            pupils_new_class = all_classes[int(new_class)][1]
            successMsg = f'{username} has been {status}d to {pupils_new_class}. To continue editing, '
        else:
            successMsg = f'{username} has been {status}d. To continue editing, '
        return render(request, 'success.html', {'href': href, 'successMsg': successMsg})
        
    else:
        href = reverse('runo:login')
        errorMsg = 'You are not authorized to update pupil\'s result. Login with the authorized user to do this.'
        return render(request, 'error.html', {'is_class_teacher': is_class_teacher, 'errorMsg': errorMsg, 'href': href})
    
    
@permission_required('runo.is_pupil')
def pupil(request):
    try:
        pupil = request.user
        current_class = pupil.userclass_set.all().filter(in_class=True).first().Class
        class_code = current_class
        current_class = all_classes[int(current_class)][1]
        context = {'class_code': class_code, 'aboutSchool': aboutSchool, 'pupil': pupil, 'current_class': current_class}
        return render(request, 'runo/sms/pupil.html', context)
        
    except:
        href = reverse('runo:login', args = [])
        errorMsg = 'You are not authorized to view user profile. Login with the authorized user to do this.'
        return render(request, 'error.html', {'errorMsg': errorMsg, 'href': href})
  
@permission_required('runo.is_pupil')
def updateProfile(request):
    try:
        current_class = request.user.userclass_set.all().filter(in_class=True).first().Class
        current_class = all_classes[int(current_class)][1]
        user_profile = UserProfileForm(instance=request.user.userprofile)
        context = {}
        if request.method == 'POST':
            user_profile  = UserProfileForm(instance=request.user.userprofile, files=request.FILES, data=request.POST)
            if user_profile.is_valid():
                
                user_profile.save()
                
        return render(request, 'runo/sms/editProfile.html', {'current_class': current_class, 'user_profile': user_profile, 'aboutSchool': aboutSchool})
    
    except:
        href = reverse('runo:login', args = [])
        errorMsg = 'You are not authorized to view user profile. Login with the authorized user to do this.'
        return render(request, 'error.html', {'errorMsg': errorMsg, 'href': href})
       
@permission_required('runo.is_pupil')
def sendMsg(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST['message']
        
        new_msg = Message(sender=request.user, subject=subject, message=message, reply='')
        new_msg.save()
        
        msg_url = request.build_absolute_uri(new_msg.get_absolute_url())
        email_subject = f'mesage From {request.user.username}'
        msg_body = f'{subject}. view at {msg_url}'
        send_mail(email_subject, msg_body, 'admin@gmail.com', ['admin@gmail.com'], fail_silently=True)
        
    user_msgs = Message.objects.filter(sender=request.user).order_by('-sent').all()[:6]
    messages = []
    for user_msg in user_msgs:
        msg_details = {
            'sent': str(user_msg.sent)[:21],
            'subject': user_msg.subject,
            'message': user_msg.message,
            'reply': user_msg.reply
        }
        messages.append(msg_details)
    messages.reverse()
    return JsonResponse({'messages': str(messages)})



@permission_required('runo.is_pupil')
def viewResults(request, Class=None):
    try:
        AllRes = Result.objects.filter(user=request.user).first()
        results = eval(AllRes.results)
        res_in_view = None
        for result in results:
            
            try:
                result['className'] = all_classes[int(result['Class'])][1]
            except:
                result['className'] = 'Unable to resolve class name'
            if result['Class'] == Class:
                res_in_view = result
        
        context = {
            'Class': Class,
            'results': results,
            'res_in_view': res_in_view,
            'all_classes': all_classes,
            'aboutSchool': aboutSchool
        }
        return render(request, 'runo/sms/resultForPupil.html', context)

    except:
        href = reverse('runo:login', args = [])
        errorMsg = "You are not authorized to view this user's result. Login with the authorized user to do this."
        return render(request, 'error.html', {'errorMsg': errorMsg, 'href': href})
    


from django.contrib.admin.views.decorators import staff_member_required

#@staff_member_required
def msg_for_admin(request, id=None):
    try:
        msg = Message.objects.filter(id=id).first() 
        unreplied_msgs = Message.objects.filter(replied=False).all()
        context = {
            'unreplied_msgs': unreplied_msgs,
            'aboutSchool': aboutSchool,
            'msg': msg
        }
        
        if request.method == 'POST':
            reply = request.POST['reply']
            msg.reply = reply
            msg.replied = True
            msg.save()
            return JsonResponse({'success_msg': 'reply successful'})
        return render(request, 'admin/message.html', context)
    
    except:
        pass

#@staff_member_required
def msg_for_admin2(request):
    msg = Message.objects.filter(replied=False).first()
    unreplied_msgs = Message.objects.filter(replied=False).all()
    context = {
            'unreplied_msgs': unreplied_msgs,
            'aboutSchool': aboutSchool,
            'msg': msg
        }
    return render(request, 'admin/message.html', context)
    
#@staff_member_required   
from django.db.models import Q
def admin_update_user(request, username):
    user = User.objects.filter(Q(username=username) | Q(email=username)).first()
    
    if request.method == 'POST':
        toChange = request.POST['toChange']
        changeTo = request.POST['changeTo']
        
        if changeTo is not None:
            if toChange == 'first_name':
                # user = User.objects.get(username=username)
                user.first_name = changeTo
                
            elif toChange == 'last_name':
                user.last_name = changeTo
                
            elif toChange == 'email':
                user.email = changeTo
            
            elif toChange == 'DOB':
                userprofile = UserProfile.objects.filter(user=user).first()
                userprofile.DOB = changeTo
                userprofile.save()
            elif toChange == 'password':
                user.set_password(changeTo)
            user.save()
            return JsonResponse({'msg': f'{toChange} changed to {changeTo}'})
    context = {
        'aboutSchool': aboutSchool,
        'user': user
    }
    return render(request, 'admin/updateUser.html', context)
    #return HttpResponse(last_name)

from django.contrib.auth.decorators import login_required

def password_verify(password, password2):
    if password != password2:
        return False
    if len(password) < 6:
        return False
    first_char = password[0]
    all_similar = True
    for char in password:
        if char != first_char:
            all_similar = False
    
    return not all_similar
    
        

@login_required
def change_password(request):
    msg=None
    if request.method == 'POST':
        password = request.POST['oldPassword']
        
        
        if request.user.check_password(password):
            new_password = request.POST['newPassword']
            retype_password = request.POST['retypePassword']
            
            if password_verify(new_password, retype_password):
                request.user.set_password(new_password)
                request.user.save()
                msg = 'Password successfully changed'
            else:
                msg = 'New passwords do not match or consist of only one character'
        else:
            msg = 'incorrect password'
    
    context = {
            'aboutSchool': aboutSchool,
            'msg': msg
        }
            
            
    return render(request, 'registration/password_change_form.html', context)



from django.contrib import admin
def adminPanel(request):
    context = {'aboutSchool': aboutSchool}
    if request.method == 'POST':
        username = request.POST['username']
        if len(username) < 1 or ('/' in username):
            return HttpResponseRedirect(reverse('runo:adminPanel', args=[]))
        
        href = reverse('runo:admin_update_user', args=[username])
        return HttpResponseRedirect(href)

    return render(request, 'admin/routes.html', context)
    

from .models import MessageAllUsers
#@staff_member_required   
def message_all_users(request):
    if request.method == 'POST':
        title = request.POST['title']
        message = request.POST['message']
        
        Message = MessageAllUsers.objects.first()
        if Message:
            Message.title = title
            Message.message = message
            Message.save()
        else:
            Message = MessageAllUsers(title=title, message=message)
            Message.save()
        return HttpResponse(Message.message)
    return render(request, 'admin/messageAll.html')

@login_required
def viewSchoolMessage(request):
    message = MessageAllUsers.objects.first()
    message_to_disp = {
        'title': message.title,
        'message': message.message
    }
    return JsonResponse({'message': message_to_disp})