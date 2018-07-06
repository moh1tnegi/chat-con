from django.conf.urls import url
from . import views

app_name = 'chat'

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^login/$', views.login_form, name='login'),
    url(r'^signup/$', views.signup_form, name='signup'),
    url(r'^logout/$', views.log_out, name='logout'),
    url(r'^contact_us/$', views.contact_form, name='contact'),
]
