from django.db import models
from django import forms

from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, InlinePanel
from .blog_detail_page import BlogDetailPage
from wagtail.images.edit_handlers import ImageChooserPanel


# First subclassed blog post page
class ArticleBlogPage(BlogDetailPage):
    """A subclassed blog post page for articles."""

    template = "blog/article_blog_page.html"

    subtitle = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    intro_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text='Best size for this image will be 1400x400'
    )

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        FieldPanel("subtitle"),
        ImageChooserPanel("banner_image"),
        ImageChooserPanel("intro_image"),
        MultiFieldPanel(
            [
                InlinePanel("blog_authors", label="Author", min_num=1, max_num=4)
            ],
            heading="Author(s)"
        ),
        MultiFieldPanel(
            [
                FieldPanel("categories", widget=forms.CheckboxSelectMultiple)
            ],
            heading="Categories"
        ),
        StreamFieldPanel("content"),
    ]


