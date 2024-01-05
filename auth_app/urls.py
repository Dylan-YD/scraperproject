from django.urls import path

from auth_app.views import register_page, log_out, edit_user_profile

urlpatterns = [

    path('register', register_page),
    path('log-out', log_out),
    path('user/edit', edit_user_profile)
]
