from django.db import models
from django.shortcuts import render

from modelcluster.fields import ParentalKey

from wagtail.api import APIField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    InlinePanel,
    StreamFieldPanel,
    PageChooserPanel,
    ObjectList,
    TabbedInterface,
)
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from rest_framework.fields import Field
from blog.models import BlogDetailPage
from streams import blocks
from blog.models import BlogDetailPage, BlogLikes
from search.views import get_recent_blogs
from content.models import EventDetailPage, ScholarshipDetailPage, EventLikes, ScholarshipLikes




class HomePageCarouselImages(Orderable):
    """Between 1 and 5 images for the home page carousel."""

    page = ParentalKey("home.HomePage", related_name="carousel_images")
    carousel_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        ImageChooserPanel("carousel_image")
    ]

    api_fields = [
        APIField("carousel_image"),
    ]


class HomePage(RoutablePageMixin, Page):
    template = "home/home_page.html"

    # parent_page_type = [
    #     'wagtailcore.Page'
    # ]

    content = StreamField([
        ("cta", blocks.CTABlock()),
    ], null=True, blank=True)

    api_fields = [
        APIField("carousel_images"),
        APIField("content"),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [InlinePanel("carousel_images", max_num=5, min_num=1, label="Image")],
            heading="Carousel Images 1320x585",
        ),

        StreamFieldPanel("content"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading='Content'),
            # ObjectList(banner_panels, heading="Banner Settings"),
            ObjectList(Page.promote_panels, heading='Promotional Stuff'),
            ObjectList(Page.settings_panels, heading='Settings Stuff'),
        ]
    )

    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        # "posts" will have child pages; you'll need to use .specific in the template
        # in order to access child properties, such as youtube_video_id and subtitle
        limit_top = 5

        blog_likes = BlogLikes.objects.all().count()
        event_likes = EventLikes.objects.all().count()
        scholarship_likes = ScholarshipLikes.objects.all().count()

        print("++++++++++++++++++++++++++++++++++++++++++++")
        print("Blog Likes: ", blog_likes)
        print("Events Likes: ", event_likes)
        print("Scholarship Likes: ", scholarship_likes)

        # get News
        # latest_news = BlogDetailPage.objects.live().filter(categories='news').order_by('-first_published_at')
        recent_news_blogs = BlogDetailPage.objects.live().public().order_by(
                        'first_published_at')[:limit_top][::-1]

        recent_events = EventDetailPage.objects.live().public().order_by(
            'first_published_at')[:limit_top][::-1]

        recent_scholarships = ScholarshipDetailPage.objects.live().public().order_by(
            'first_published_at')[:limit_top][::-1]

        context['recent_news_blogs'] = recent_news_blogs
        context['recent_events'] = recent_events
        context['recent_scholarships'] = recent_scholarships

        return context
