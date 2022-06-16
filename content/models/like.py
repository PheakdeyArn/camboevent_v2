from django.db import models
# from blog.models import BlogDetailPage


# create like news
class EventLikes(models.Model):
    user = models.ForeignKey(
        'users.User',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='user_like_event'
    )

    post = models.ForeignKey(
        'content.EventDetailPage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='like_event'
    )

    status = models.BooleanField(default=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Event Like'
        verbose_name_plural = 'Event Likes'


class ScholarshipLikes(models.Model):

    user = models.ForeignKey(
        'users.User',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='user_like_scholarship'
    )

    post = models.ForeignKey(
        'content.ScholarshipDetailPage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='like_scholarship'
    )

    status = models.BooleanField(default=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Scholarship Like'
        verbose_name_plural = 'Scholarship Likes'
