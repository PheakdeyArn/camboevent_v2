from django.db import models
from wagtail.core.models import Page
from django import forms
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.core.fields import StreamField
from streams import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel


class BlogDetailPage(Page):
    """ Parental Blog Detail Page """

    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Overwrites the default title',
    )

    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )

    categories = ParentalManyToManyField("blog.BlogCategory", blank=True)

    content = StreamField([
        ("title_and_text", blocks.TitleAndTextBlock()),
        ("full_richText", blocks.RichTextBlock()),
        ("simple_richText", blocks.SimpleRichTextBlock()),
        ("cards", blocks.CardBlock()),
        ("cta", blocks.CTABlock()),
    ], null=True, blank=True)

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
            heading='Categories'
        ),
        StreamFieldPanel("content"),
    ]

