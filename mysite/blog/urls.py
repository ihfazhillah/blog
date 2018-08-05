from django.conf.urls import url
from . import views
from .feeds import LatestPostsFeed
from search.views import search_blog_view

urlpatterns = [
    url(r'^feeds/$', LatestPostsFeed(), name='latest-post-feed'),
    url(r'^search/$', search_blog_view, name='search'),
    url(r'^$', views.post_list, name='post-list'),
    url(r'^tag/(?P<tag_slug>[-\w]+)$', views.post_list,
        name='post-list-by-tag'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'\
        r'(?P<post>[-\w]+)/$',
        views.post_detail,
        name='post-detail'),
    url(r'^(?P<post_id>\d+)/share/email', views.post_share, name='share-email')
]

