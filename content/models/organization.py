from django.db import models

from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet


class OrganizationsOrderable(Orderable):
    """This allows us to select one or more organizations from Snippets."""

    page = ParentalKey("content.EventDetailPage", related_name="organizations")
    organization = models.ForeignKey(
        "content.Organization",
        on_delete=models.CASCADE,
    )

    panels = [
        SnippetChooserPanel("organization"),
    ]


class ScholarshipOrganizationsOrderable(Orderable):
    """This allows us to select one or more organizations from Snippets."""

    page = ParentalKey("content.ScholarshipDetailPage", related_name="organizations")
    organization = models.ForeignKey(
        "content.Organization",
        on_delete=models.CASCADE,
    )

    panels = [
        SnippetChooserPanel("organization"),
    ]


class Organization(models.Model):
    """ Organization Snippet """
    name = models.CharField(max_length=50)
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
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'
        ordering = ['name']

    def __str__(self):
        return self.name


register_snippet(Organization)

