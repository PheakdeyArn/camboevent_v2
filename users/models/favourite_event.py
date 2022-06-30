from django.db import models
# from content.models.event_detail import EventDetailPage
from wagtail.snippets.models import register_snippet


class FavouriteEvent(models.Model):
    user = models.ForeignKey(
        'users.User',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    event = models.ForeignKey(
        'content.EventDetailPage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    class Meta:
        verbose_name = 'FavoriteEvent'
        verbose_name_plural = 'FavoriteEvents'
        # ordering = ['city']


# register_snippet(FavouriteEvent)
