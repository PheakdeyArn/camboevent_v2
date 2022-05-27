""" Flexible Pages """
from django.db import models
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from streams import blocks


# Create your models here.
class FlexPage(Page):
    """ Flexible Page Class"""
    template = "flex/flex_page.html"

    # @TODO - add streamfields
    subtitle = models.CharField(max_length=100, null=True, blank=True)

    # add streamfield
    """ Create a stream field """
    # @TODO
    """
        - create streamfield in streams/block.py
        - add it into Streamfields function
    """

    content = StreamField([
        ("h2", blocks.H2Block()),
        ("h3", blocks.H3Block()),
        ("h4", blocks.H4Block()),
        ("quote", blocks.QuoteBlock()),
        ("title_and_text", blocks.TitleAndTextBlock()),
        ("full_richText", blocks.RichTextBlock()),
        ("simple_richText", blocks.SimpleRichTextBlock()),
        ("cards", blocks.CardBlock()),
        ("cta", blocks.CTABlock()),
        ("button", blocks.ButtonBlock()),
        ("singe_image", blocks.SingleImageBlock()),
        ("image_and_caption", blocks.ImageAndCaptionBlock()),
        ("carousel", blocks.CarouselBlock()),
        ("gallery", blocks.GalleryBlock()),
    ], null=True, blank=True)

    # add content panels to wagtail admin
    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        StreamFieldPanel("content")
    ]

    class Meta:
        verbose_name = "Flex Page"
        verbose_name_plural = "Flex Pages"
