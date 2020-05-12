from django.conf.urls import url
from log_in import views

# TEMPLATE URLs

app_name = 'log_in'

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^userlogin/$', views.user_login, name='user_login')
]
