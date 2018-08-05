from django.db import models
from blog.models import Post

# Create your models here.

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name,
                                            self.post)
    class Meta:
        ordering = ('created',)
