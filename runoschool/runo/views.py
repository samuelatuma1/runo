from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
import datetime

from .models import Intro, News, ImportantDates

# Create your views here.
def index(request):
    introImgs = Intro.objects.all().order_by('-uploaded')[:1]
    news = News.objects.filter(publish=True).order_by('-published').all()[:6]
    dates = ImportantDates.objects.all().order_by('date')[:12]
    
    
    # Show upcoming events 14 days prior
    upcoming_event = None
    if len(dates) > 0:
        upcoming = dates[0]
        time = ( datetime.date(upcoming.date.year, upcoming.date.month, upcoming.date.day) - datetime.date.today()).days
        if time > -1 and time < 8:
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
                                                   'dates': dates})

    return render(request, 'runo/index.html', {'section': 'home', 'news': news,
                                               'upcoming_event': upcoming_event,
                                               'dates': dates})


def news(request, slug, year, month, day):
    newsItem = News.objects.filter(slug=slug, published__day=day,
                                 published__month=month, published__year=year).first()
    
    time = datetime.date(2021, 7, 17) - datetime.date(newsItem.published.year, newsItem.published.month, newsItem.published.day)
    return HttpResponse(f'{newsItem}, {month}, {day}, {slug} {time.days} ')