from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
        url(r'^index/', views.index, name='index'),
        url(r'^signup/', views.signup, name='signup'),
        url(r'^dashboard/', views.dashboard, name='dashboard'),
        url(r'^profile/', views.profile, name='profile'),
        url(r'^leaderboard/', views.leaderboard, name='leaderboard'),
        url(r'^more/', views.more, name='more'),
        url(r'^stocks/(?P<slug>[^\.]+)/comment/$', views.add_comment_to_stock, name='add_comment_to_stock'),
        url(r'^stocks/(?P<slug>[^\.]+)/$', views.view_stock, name='view_stocks'),
        # url(r'^comment/(?P<comment_id>[0-9]+)/$', views.comments_view, name='comment'),

        url(r'^$', views.index, name='index'),
    ]
