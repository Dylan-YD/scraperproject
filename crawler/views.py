import pandas as pd
from .models import Ad_model
from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import Ad_modelSerializer
from crawler.system.adscraper import geotagging
from crawler.system.webcontent import url_content_scraper
from crawler.ResponseHelper.response import ResponseHelper

class Ad_modelList(APIView):
    def post(self, request):
        print("getting data")
        df = pd.read_csv('keywords.csv')
        
        queries = []
        for i in range(0, len(df['keywords'])):
            for j in range(0, len(df['buzzwords'])):
                for k in range(0, len(df["suburb"])):
                # keywords,buzzwords,suburb,Postcode,State
                    query = str(df['keywords'][i])+ " " + str(df['buzzwords'][j])+ " " + str(df['suburb'][k])+ " " + str(df['Postcode'][k]) + " " + str(df['State'][k])
                    queries.append(query) 
            print(queries)
        
        try:
            print("started scraping")
            for query in queries:
                print("*"*100)
                print(query)
                looper = 0
                while looper < 2:
                    print("looper",looper)
                    ads = url_content_scraper(query)
                    if not ads:
                        looper += 1
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
                        whois = ad["whois"]

                        existing_ad = Ad_model.objects.filter(ad_url=url) or Ad_model.objects.filter(ad_title=title)
                        if existing_ad:
                            continue  

                        ad = Ad_model.objects.create(ad_url=url, ad_title=title, ad_description=description, query=query, screenshot=screenshot, company_contact_number=company_contact_number, company_board_members=company_board_members, company_email=company_email, company_board_member_role=company_board_member_role, whois=whois)
                        ad.save()
                        print("data saved")
                
                    # queries = geotagging(query)
                    # print(queries)
                    # for q in queries:
                    #     ads = url_content_scraper(q)
                    #     if not ads:
                    #         continue
                    #     for ad in ads:
                    #         title = ad["title"]
                    #         url = ad["url"]
                    #         description = ad["description"]
                    #         screenshot = ad["screenshot"]
                    #         company_contact_number = ad["contact_number"]
                    #         company_board_members = ad["company_board_members"]
                    #         company_email = ad["company_email"]
                    #         company_board_member_role = ad["company_board_members_role"]
                    #         whois = ad["whois"]

                    #         existing_ad = Ad_model.objects.filter(ad_url=url) or Ad_model.objects.filter(ad_title=title)
                    #         if existing_ad:
                    #             continue  
                    #         ad = Ad_model.objects.create(ad_url=url, ad_title=title, ad_description=description, query=query, screenshot=screenshot, company_contact_number=company_contact_number, company_board_members=company_board_members, company_email=company_email, company_board_member_role=company_board_member_role, whois=whois)
                    #         ad.save()
                    #         print("query data saved")
                    looper += 1
            return ResponseHelper.get_success_response (queries,'successfully scraped data')
        except:
            return ResponseHelper.get_internal_server_error_response("Error in scraping data")
            
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
