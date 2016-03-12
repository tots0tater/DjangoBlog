from django.conf.urls import url, include
from django.contrib.auth import views

from . import views

app_name = 'blog'
urlpatterns = [
    # ex: /blogs/
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^post_blog/$', views.post_blog, name='post_blog'),
    # ex: /blogs/5/
    url(r'^(?P<pk>[0-9]+)$', views.BlogView.as_view(), name='blog_post'),
    # For all of our authentication urls
    url('^', include('django.contrib.auth.urls')),
    url(r'^logout/$', views.logout_view, name='logout_view'),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^create_account/$', views.create_account, name='create_account'),

    # Comment manipulation urls
    url(r'^post_comment/$', views.post_comment, name='post_comment'),
    url(r'^delete_comment/$', views.delete_comment, name='delete_comment'),
    url(r'^edit_comment/$', views.edit_comment, name='edit_comment'),
]