from django.db import models
from wagtail.snippets.models import register_snippet


class FavouriteScholarship(models.Model):
    user = models.ForeignKey(
        'users.User',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    scholarship = models.ForeignKey(
        'content.ScholarshipDetailPage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    class Meta:
        verbose_name = 'FavoriteEvent'
        verbose_name_plural = 'FavoriteEvents'
        ordering = ['id']


# register_snippet(FavouriteScholarship)
