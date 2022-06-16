from django.db import models
from blog.models import BlogDetailPage


# create like news
class BlogLikes(models.Model):
    user = models.ForeignKey(
        'users.User',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    blog = models.ForeignKey(
        BlogDetailPage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    status = models.BooleanField(default=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Blog Like'
        verbose_name_plural = 'Blog Likes'

