"""
URL configuration for emotion_tracker_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import HttpResponseNotAllowed
from django.urls import path, re_path

from emotion_tracker_django.views import index_view, day_list, day_detail, day_create, entry_delete

def days(request):
    if request.method == 'GET':
        return day_list(request)
    elif request.method == 'POST':
        return day_create(request)
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

def days_fetch(request):
    if request.method == 'POST':
        return day_detail(request)
    else:
        return HttpResponseNotAllowed(['POST'])

urlpatterns = [
    path('admin/', admin.site.urls),

    # Root URL that serves the React front-end
    path('', index_view.index, name='index'),


    path('days', days, name='days'),


    path('days/fetch', days_fetch, name='day_detail'),  # Expecting date as string


    path('entries/<str:uuid>', entry_delete, name='entry_delete'),

    # Catch-all for React Router, which handles frontend routes
    # re_path(r'^.*$', index_view.index, name='react_app'),
]
