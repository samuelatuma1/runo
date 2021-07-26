from . import views
from django.urls import path, include

app_name = 'runo'
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    path('news/<str:slug>/<int:year>/<int:month>/<int:day>/', views.news, name='news'),
    path('gallery/', views.gallery, name='gallery'),
    path('about/', views.aboutUs, name='about'),
    path('academics/', views.academics, name='academics'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register')
]