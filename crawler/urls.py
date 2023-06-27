from django.urls import path
from crawler import views
from django.shortcuts import render

def dashboard(request):
    return render(request, 'admin_index.html')

def ads_page(request):
    return render(request, 'ads.html')

def calender(request):
    return render(request, 'calendar.html')

def search(request):
    return render(request, 'search.html')

def ad_info(request):
    return render(request, 'ad_info.html')

def dialer(request):
    return render(request, 'dialer.html')

urlpatterns = [
    path('crawler/dashboard', dashboard),
    path('crawler/ads', ads_page),
    path('crawler/calender', calender),
    path('', search),
    path('crawler/ad_info', ad_info),
    path('crawler/dialer', dialer),
    path('crawler/<int:ad_id>', views.single_ad_info.as_view()),
    path('v1/crawler/delete_ad/<int:ad_id>', views.ad_delete.as_view()),
    path('v1/crawler/update_ad/<int:ad_id>', views.ad_update.as_view()),
    path('v1/scraper/number_of_ads', views.ads_count.as_view()),
    path('v1/scraper/ad_queries_count', views.ad_queries_count.as_view()),
]