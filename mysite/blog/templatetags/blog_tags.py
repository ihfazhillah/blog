import markdown
from django import template
from django.utils.safestring import mark_safe

from ..models import Post
from search.forms import SearchForm

register = template.Library()

@register.simple_tag
def total_posts():
    return Post.published.count()

@register.assignment_tag
def search_form():
    return SearchForm()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {
        'latest_posts': latest_posts
    }

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

