from django.db import models
from modelcluster.fields import ParentalKey
from django.shortcuts import render

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel, MultiFieldPanel
from wagtail.core.fields import StreamField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from streams import blocks

from content.models.event_detail import EventDetailPage

from content.models.scholarship_detail import ScholarshipDetailPage


class EventListingPage(RoutablePageMixin, Page):
    """Listing page lists all the Blog Detail Pages."""

    template = "content/event_listing_page.html"

    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Overwrites the default title',
    )

    body = RichTextField(blank=True)

    content = StreamField([
        ("h2", blocks.H2Block()),
        ("h3", blocks.H3Block()),
        ("h4", blocks.H4Block()),
        ("quote", blocks.QuoteBlock()),
        ("carousel", blocks.CarouselBlock()),
        ("cta", blocks.CTABlock()),
    ], null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),

        MultiFieldPanel([
            InlinePanel('listing_page_sliders', max_num=5, min_num=1, label="sliders"),
        ], heading="Slider Options"),

        FieldPanel('body', classname="full"),
        StreamFieldPanel("content"),
    ]

    def get_context(self, request, *args, **kwargs):
        """ Adding custom stuff into our context"""
        context = super().get_context(request, *args, **kwargs)
        # "posts" will have child pages; you'll need to use .specific in the template
        # in order to access child properties, such as youtube_video_id and subtitle
        # context["events"] = EventDetailPage.objects.live().public()

        # Get all posts
        all_posts = EventDetailPage.objects.live().public().order_by('-first_published_at')
        # Paginate all posts by 2 per page
        paginator = Paginator(all_posts, 5)
        # Try to get the ?page=x value
        page = request.GET.get("page")
        category = request.GET.get('category')

        try:
            # If the page exists and the ?page=x is an int
            events = paginator.page(page)
        except PageNotAnInteger:
            # If the ?page=x is not an int; show the first page
            events = paginator.page(1)
        except EmptyPage:
            # If the ?page=x is out of range (too high most likely)
            # Then return the last page
            events = paginator.page(paginator.num_pages)

        context["posts"] = events
        context["page_title"] = "Event List"
        return context
