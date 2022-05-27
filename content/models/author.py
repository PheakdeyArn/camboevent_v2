from django.db import models

from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet


class AuthorsOrderable(Orderable):
    """This allows us to select one or more blog authors from Snippets."""

    page = ParentalKey("content.EventDetailPage", related_name="authors")
    author = models.ForeignKey(
        "content.Author",
        on_delete=models.CASCADE,
    )

    panels = [
        SnippetChooserPanel("author"),
    ]


class ScholarshipAuthorsOrderable(Orderable):
    """This allows us to select one or more blog authors from Snippets."""

    page = ParentalKey("content.ScholarshipDetailPage", related_name="authors")
    author = models.ForeignKey(
        "content.Author",
        on_delete=models.CASCADE,
    )

    panels = [
        SnippetChooserPanel("author"),
    ]


class Author(models.Model):
    """ Author Snippet """
    name = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name='+'
    )

    panels = [
            MultiFieldPanel(
                [
                    FieldPanel("name"),
                    ImageChooserPanel("image"),
                ],
                heading="Name and Image",
            ),
            MultiFieldPanel(
                [
                    FieldPanel("website"),
                ],
                heading="Links"
            )
        ]

    def __str__(self):
        """String repr of this class."""
        return self.name

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"


register_snippet(Author)

