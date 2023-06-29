from .models import Ad_model, company_info
from rest_framework.views import APIView
from datetime import datetime
from crawler.ResponseHelper.response import ResponseHelper
from .serializer import Ad_modelSerializer, company_infoSerializer
from crawler.system.adscraper import scrape_google_ads, geotagging
from crawler.system.webcontent import url_content_scraper
from django.shortcuts import render
import pandas as pd

class Ad_modelList(APIView):
    def post(self, request):
        df = pd.read_csv('keywords.csv')
        try:
            keywords = df['keywords'].tolist()
            for query in keywords:
                looper = 0
                while looper < 2:
                    ads = url_content_scraper(query)
                    if not ads:
                        continue
                    for ad in ads:
                        title = ad["title"]
                        url = ad["url"]
                        description = ad["description"]
                        screenshot = ad["screenshot"]
                        company_contact_number = ad["contact_number"]
                        company_board_members = ad["company_board_members"]
                        company_email = ad["company_email"]
                        company_board_member_role = ad["company_board_members_role"]

                        existing_ad = Ad_model.objects.filter(ad_url=url) or Ad_model.objects.filter(ad_title=title)
                        if existing_ad:
                            continue  

                        ad = Ad_model.objects.create(ad_url=url, ad_title=title, ad_description=description, query=query, screenshot=screenshot, company_contact_number=company_contact_number, company_board_members=company_board_members, company_email=company_email, company_board_member_role=company_board_member_role)
                        ad.save()
                
                    queries = geotagging(query)
                    print(queries)
                    for q in queries:
                        ads = url_content_scraper(q)
                        if not ads:
                            continue
                        for ad in ads:
                            title = ad["title"]
                            url = ad["url"]
                            description = ad["description"]
                            screenshot = ad["screenshot"]
                            company_contact_number = ad["company_contact_number"]
                            company_board_members = ad["company_board_members"]
                            company_email = ad["company_email"]
                            company_board_member_role = ad["company_board_members_role"]

                            existing_ad = Ad_model.objects.filter(ad_url=url) or Ad_model.objects.filter(ad_title=title)
                            if existing_ad:
                                continue  
                            ad = Ad_model.objects.create(ad_url=url, ad_title=title, ad_description=description, query=query, screenshot=screenshot, company_contact_number=company_contact_number, company_board_members=company_board_members, company_email=company_email, company_board_member_role=company_board_member_role)
                            ad.save()
                    looper += 1
            return ResponseHelper.get_success_response (keywords,'successfully scraped data')
        except Exception as e:
            return ResponseHelper.get_internal_server_error_response(str(e))
            
    def get(self, request):
        try:
            ad = Ad_model.objects.all()
            serializer = Ad_modelSerializer(ad, many=True)
            return ResponseHelper.get_success_response(serializer.data, "Success")
        except Exception as e:
            return ResponseHelper.get_internal_server_error_response(str(e))
        
    
class Ad_queryOne(APIView):
    def get(self, request, query):
        try:
            ad = Ad_model.objects.filter(query=query)
            serializer = Ad_modelSerializer(ad, many=True)
            return ResponseHelper.get_success_response(serializer.data, "Success")
        except Exception as e:
            return ResponseHelper.get_internal_server_error_response(str(e))
        
class ads_count(APIView):
    def get(self, request):
        try:
            ad = Ad_model.objects.all().count()
            return ResponseHelper.get_success_response(ad, "Success")
        except Exception as e:
            return ResponseHelper.get_internal_server_error_response(str(e))

class ad_info(APIView):
    def get(self, request, ad_id):
        try:
            ad = Ad_model.objects.get(ad_id=ad_id)
            serializer = Ad_modelSerializer(ad)
            Ad_model.objects.filter(ad_id=ad_id).update(ad_new=False)
            return ResponseHelper.get_success_response(serializer.data, "Success")
        except Exception as e:
            return ResponseHelper.get_internal_server_error_response(str(e))
        
class ad_queries_count(APIView):
    def get(self, request):
        try:
            ad = Ad_model.objects.values('query').distinct().count()
            return ResponseHelper.get_success_response(ad, "Success")
        except Exception as e:
            return ResponseHelper.get_internal_server_error_response(str(e))

class ad_delete(APIView):
    def delete(self, request, ad_id):
        try:
            ad = Ad_model.objects.get(ad_id=ad_id)
            ad.delete()
            return ResponseHelper.get_success_response("Success", "Ad deleted successfully")
        except Exception as e:
            return ResponseHelper.get_internal_server_error_response(str(e))
    
class ad_update(APIView):
    def put(self, request, ad_id):
        try:
            ad = Ad_model.objects.get(ad_id=ad_id)
            serializer = Ad_modelSerializer(ad, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return ResponseHelper.get_success_response(serializer.data, "Success")
            return ResponseHelper.get_bad_request_response(serializer.errors)
        except Exception as e:
            return ResponseHelper.get_internal_server_error_response(str(e))

class single_ad_info(APIView):
    def get(self, request, ad_id):
        try:
            ad = Ad_model.objects.get(ad_id=ad_id)
            serializer = Ad_modelSerializer(ad)
            print(serializer.data)
            return render(request, 'ad_info.html', {"ad_info":serializer.data})
        except Exception as e:
            return ResponseHelper.get_internal_server_error_response(str(e))
