from django.db import models
from modelcluster.fields import ParentalKey
from django.shortcuts import render

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel, MultiFieldPanel

from .event import EventListingPage
from content.models.scholarship_detail import ScholarshipDetailPage


class ScholarshipListingPage(EventListingPage):
    """Listing page lists all the Blog Detail Pages."""

    template = "content/scholar_listing_page.html"

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
        all_posts = ScholarshipDetailPage.objects.live().public().order_by('-first_published_at')
        # Paginate all posts by 2 per page
        paginator = Paginator(all_posts, 5)
        # Try to get the ?page=x value
        page = request.GET.get("page")

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
        context["page_title"] = "Scholarship List"
        return context
