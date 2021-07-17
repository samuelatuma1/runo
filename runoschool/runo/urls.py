from . import views
from django.urls import path, include

app_name = 'runo'


urlpatterns = [
    path('', views.index, name='index')
]