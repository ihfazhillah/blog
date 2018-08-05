from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post


class LatestPostsFeed(Feed):
    title = 'My 5 Latest Posts'
    link = '/blog/'
    description = 'This is my last 5 posts of my blog'

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, obj):
        return obj.title

    def item_description(self, obj):
        return truncatewords(obj.body, 30)

