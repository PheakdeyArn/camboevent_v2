from django.db import models
from modelcluster.fields import ParentalKey
from django.shortcuts import render

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, PageChooserPanel, StreamFieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import StreamField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route


class ListingPageSlider(Orderable):

    page = ParentalKey('content.EventListingPage', related_name="listing_page_sliders")

    title = models.CharField(max_length=100, blank=True, null=True)
    short_description = models.CharField(max_length=500, blank=True, null=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    slider_cta = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    panels = [
        FieldPanel('title'),
        FieldPanel('short_description'),
        ImageChooserPanel("image"),
        PageChooserPanel('slider_cta'),
    ]
