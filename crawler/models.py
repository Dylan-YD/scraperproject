from django.db import models
import datetime

class Ad_model(models.Model):
    ad_id = models.AutoField(primary_key=True)
    query = models.CharField(max_length=200, blank=True)
    ad_url = models.CharField(max_length=200, blank=True)
    ad_title = models.CharField(max_length=200, blank=True)
    ad_description = models.CharField(max_length=200, blank=True)
    screenshot = models.FileField(max_length=250, default=None, blank=True)
    company_board_members = models.CharField(max_length=200, blank=True)
    company_contact_number = models.CharField(max_length=200, blank=True)
    company_email = models.CharField(max_length=200, blank=True)
    company_board_member_role = models.CharField(max_length=200, blank=True)
    notes = models.CharField(max_length=200, blank=True)
    ad_new = models.BooleanField(default=True)
    disposition = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    whois = models.CharField(max_length=200, blank=True)
    secondary_contact = models.CharField(max_length=200, blank=True)

    def save(self, *args, **kwargs):
        if not self.ad_id:
            last_ad = Ad_model.objects.order_by('-ad_id').first()
            if last_ad:
                self.ad_id = last_ad.ad_id + 1
            else:
                self.ad_id = 1

        super(Ad_model, self).save(*args, **kwargs)

    def change_ad_new(self):
        if datetime.datetime.now() - self.created_at > datetime.timedelta(days=1):
            self.ad_new = False
            self.save()

    def __str__(self):
        return self.query + " | " + self.ad_title + " | " + self.ad_url

class company_info(models.Model):
    company_name = models.CharField(max_length=200)
    company_address = models.CharField(max_length=200)
    company_phone = models.CharField(max_length=200)
    company_email = models.CharField(max_length=200)
    company_website = models.CharField(max_length=200)
    company_description = models.CharField(max_length=200)
    company_category = models.CharField(max_length=200)
    company_url = models.CharField(max_length=200)
    company_id = models.CharField(max_length=200)

    def __str__(self):
        return self.company_name + " | " + self.company_address + " | " + self.company_phone 