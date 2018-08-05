from django.db import models
from django.db.models import Count
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from taggit.managers import TaggableManager


# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,
                     self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(User,
                               related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, 
                              choices=STATUS_CHOICES,
                              default='draft')

    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post-detail',
                       args=[self.publish.year,
                             self.publish.strftime('%m'),
                             self.publish.strftime('%d'),
                             self.slug])

    def get_similiar_posts(self, count=4):
        post_tags_ids = self.tags.values_list('id', flat=True)
        similiar_posts = Post.published.filter(tags__in=post_tags_ids)\
                .exclude(id=self.id)
        similiar_posts = similiar_posts.annotate(same_tags=Count('tags'))\
                .order_by('-same_tags', '-publish')[:count]
        return similiar_posts


