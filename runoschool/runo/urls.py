from . import views
from django.urls import path, include

app_name = 'runo'
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
   # path('searchBase/', views.searchBase, name='searchBase'),
    path('news/<str:slug>/<int:year>/<int:month>/<int:day>/', views.news, name='news'),
    path('gallery/', views.gallery, name='gallery'),
    path('about/', views.aboutUs, name='about'),
    path('academics/', views.academics, name='academics'),
    
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', views.change_password, name='change_password'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    path('register/', views.register, name='register'),
    path('teacher/', views.teacher, name='teacher'),
    path('result_page/<str:Class>/<str:username>/', views.result_page, name='result_page'),
    path('result/<str:Class>/<str:username>/', views.result, name='result'),
    path('changeclass/<str:Class>/<str:username>/<str:status>', views.changeclass, name='changeclass' ),
    path('pupil/', views.pupil, name='pupil'),
    path('updateProfile/', views.updateProfile, name='updateProfile'),
    path('sendMsg/', views.sendMsg, name='sendMsg'),
    path('viewResults/<str:Class>/', views.viewResults, name='viewResults'),
    
    path('msg_for_admin/<int:id>/', views.msg_for_admin, name='msg_for_admin'),
    path('admin_msgs/', views.msg_for_admin2, name='msg_for_admin2'),
    path('admin_update_user/<str:username>/', views.admin_update_user, name='admin_update_user'),
    
    path('adminPanel/', views.adminPanel, name='adminPanel'),
    path('message_all_users/', views.message_all_users, name='message_all_users'),
    path('viewSchoolMessage/', views.viewSchoolMessage, name='viewSchoolMessage')
    
]