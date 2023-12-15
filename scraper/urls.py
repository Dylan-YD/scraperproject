"""
URL configuration for scraper project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from crawler import views
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render


urlpatterns = [
    path("", include('crawler.urls')),
    path('admin/', admin.site.urls),
    path('v1/scraper', views.Ad_modelList.as_view()),
    path('v1/scraper/csv', views.Ad_modelList.as_view()),
    path ('v1/scraper/query/<str:query>', views.Ad_queryOne.as_view())
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
