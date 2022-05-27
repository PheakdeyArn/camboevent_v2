from django.db import models

from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, InlinePanel
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.core.fields import StreamField, RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from streams import blocks
from django.utils import timezone


class SpeakersOrderable(Orderable):
    page = ParentalKey("content.EventDetailPage", related_name="speakers")
    name = models.CharField(max_length=50)
    url = models.URLField(blank=True, null=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('url')
    ]


class EventDetailPage(Page):

    published_datetime = models.DateTimeField(default=timezone.now, help_text='Published Datetime')
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
    category = models.ForeignKey(
        "content.EventCategory",
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
    date = models.DateField("Date")
    time = models.TimeField("Time")
    host = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Please input the host',
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        null=False,
        help_text='Please input the host',
    )
    mobile = models.CharField(
        max_length=50,
        blank=True,
        null=False,
        help_text='Please input the host',
    )
    email = models.CharField(
        max_length=50,
        blank=True,
        null=False,
        help_text='Please input the host',
    )
    co_host = models.CharField(
        max_length=100,
        blank=True,
        null=False,
        help_text='Input CO-Host is have',
    )
    more_detail = RichTextField(blank=True)
    link = models.URLField(blank=True, null=True)
    submit_form_link = models.URLField(blank=True, null=True)

    content = StreamField([
        ("title_and_text", blocks.TitleAndTextBlock()),
        ("full_richText", blocks.RichTextBlock()),
        ("simple_richText", blocks.SimpleRichTextBlock()),
        ("cards", blocks.CardBlock()),
        ("cta", blocks.CTABlock()),
        ("singe_image", blocks.SingleImageBlock()),
        ("image_and_caption", blocks.ImageAndCaptionBlock()),
        ("carousel", blocks.CarouselBlock()),
    ], null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('published_datetime'),
        FieldPanel("custom_title"),
        ImageChooserPanel("banner_image"),
        FieldPanel('category'),
        MultiFieldPanel(
            [
                InlinePanel("authors", label="Author", min_num=1, max_num=4)
            ],
            heading="Author(s)"
        ),
        MultiFieldPanel(
            [
                FieldPanel('date'),
                FieldPanel('time'),
            ],
            heading="Date / Time"
        ),
        MultiFieldPanel(
            [
                InlinePanel("speakers", label="Speaker", min_num=1, max_num=5)
            ],
            heading="Speaker(s)"
        ),
        MultiFieldPanel(
            [
                InlinePanel("organizations", label="Organization", min_num=1, max_num=5)
            ],
            heading="Organization(s)"
        ),
        MultiFieldPanel(
            [
                FieldPanel('host'),
                FieldPanel('co_host'),
                FieldPanel('address'),
                FieldPanel('city'),
                FieldPanel('country'),
                FieldPanel('link'),
                FieldPanel('submit_form_link', heading="Submit Form Link"),
                FieldPanel('more_detail', heading="More Detail"),
            ],
            heading="Event Detail Info"
        ),
        MultiFieldPanel(
            [
                FieldPanel('mobile'),
                FieldPanel('email'),
            ],
            heading="Contact Info"
        ),
        StreamFieldPanel("content"),
    ]


