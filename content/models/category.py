from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.snippets.models import register_snippet


class ContentCategory(models.Model):
    """ Content category for snippet """

    name = models.CharField(max_length=255)
    slug = models.SlugField(
        verbose_name='slug',
        allow_unicode=True,
        max_length=255,
        help_text='A slug to identify posts by this category',
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('slug')
    ]

    class Meta:
        verbose_name = 'Blog Category'
        verbose_name_plural = 'Blog categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class EventCategory(ContentCategory):
    class Meta:
        verbose_name = 'Event Category'
        verbose_name_plural = 'Event categories'
        ordering = ['name']


class ScholarshipCategory(ContentCategory):
    class Meta:
        verbose_name = 'Scholarship Category'
        verbose_name_plural = 'Scholarship categories'
        ordering = ['name']


register_snippet(EventCategory)
register_snippet(ScholarshipCategory)
