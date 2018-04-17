from django.conf.urls import url
from . import views

app_name = 'interface'

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'login/', views.login_form, name='login'),
    url(r'signup/', views.signup_form, name='signup'),
]
