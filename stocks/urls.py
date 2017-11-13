from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
        url(r'^index/', views.index, name='index'),
        url(r'^signup/', views.signup, name='signup'),
        url(r'^dashboard/', views.dashboard, name='dashboard'),
        url(r'^(?P<slug>[^\.]+)/$', views.view_stock, name='view_stocks'),
        url(r'^$', views.index, name='index'),
    ]
