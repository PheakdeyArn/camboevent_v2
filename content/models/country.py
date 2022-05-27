from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.snippets.models import register_snippet


class Country(models.Model):
    """ Content Country for snippet """

    name = models.CharField(max_length=50)

    panels = [
        FieldPanel('name'),

    ]

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
        ordering = ['name']

    def __str__(self):
        return self.name


register_snippet(Country)
