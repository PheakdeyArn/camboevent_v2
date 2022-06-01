from django.db import models
from .user import User
from content.models.city import City
from content.models.country import Country
from wagtail.snippets.models import register_snippet


class Address(models.Model):
    user = models.ForeignKey(
        'users.User',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    city = models.ForeignKey(
        'content.City',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    country = models.ForeignKey(
        'content.Country',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    latitude = models.CharField(
        verbose_name="Latitude",
        max_length=64,
        blank=True,
        null=True,
        help_text='Please input the host',
    )
    longitude = models.CharField(
        verbose_name="Longitude",
        max_length=64,
        blank=True,
        null=True,
        help_text='Please input the host',
    )

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
        ordering = ['city']


register_snippet(Address)


