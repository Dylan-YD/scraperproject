from .models import Ad_model, company_info
from rest_framework import serializers

class Ad_modelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad_model
        fields = ('ad_id','ad_url', 'ad_title', 'ad_description', 'query', 'screenshot', 'company_contact_number', 'ad_new', 'company_board_members', 'notes', 'disposition', 'created_at', 'company_board_member_role', 'company_email')

class company_infoSerializer(serializers.ModelSerializer):
    class Meta:
        model = company_info
        fields = ('company_name', 'company_address', 'company_phone', 'company_email', 'company_website', 'company_description', 'company_category', 'company_url', 'company_id')
