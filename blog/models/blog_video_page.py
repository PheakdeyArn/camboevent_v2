from django.db import models
from wagtail.core.models import Page
from django import forms

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from .blog_detail_page import BlogDetailPage


class VideoBlogPage(BlogDetailPage):
    """A video subclassed page."""

    template = "blog/video_blog_page.html"

    youtube_video_id = models.CharField(max_length=30)

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        ImageChooserPanel("banner_image"),
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
        FieldPanel("youtube_video_id"),
        StreamFieldPanel("content"),
    ]