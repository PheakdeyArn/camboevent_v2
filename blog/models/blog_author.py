from django.db import models
from wagtail.core.models import Orderable
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.snippets.edit_handlers import SnippetChooserPanel


class BlogAuthorsOrderable(Orderable):
    """This allows us to select one or more blog authors from Snippets."""

    page = ParentalKey("blog.BlogDetailPage", related_name="blog_authors")
    author = models.ForeignKey(
        "content.Author",
        on_delete=models.CASCADE,
    )

    panels = [
        SnippetChooserPanel("author"),
    ]



