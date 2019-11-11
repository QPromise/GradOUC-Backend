from django.conf.urls import url

from . import views

app_name = 'OUC'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^do_login/$', views.do_login, name='do_login'),
    url(r'^get_schedule/$', views.get_schedule, name='get_schedule'),
    url(r'^get_news/$', views.get_news, name='get_news'),
    url(r'^get_config/$', views.get_config, name='get_config'),
    url(r'^get_course/$', views.get_course, name='get_course'),
    url(r'^get_score/$', views.get_score, name='get_score'),
    url(r'^search_book/$', views.search_book, name='search_book'),
    url(r'^get_bookDetail/$', views.get_bookDetail, name='get_bookDetail'),
    url(r'^get_schoolNews/$', views.get_schoolNews, name='get_schoolNews'),
    url(r'^get_schoolNewsDetail/$', views.get_schoolNewsDetail, name='get_schoolNewsDetail'),
]
