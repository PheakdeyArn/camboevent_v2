from django.db import models
from wagtail.core.models import Page
from wagtail.contrib.routable_page.models import RoutablePageMixin
from wagtail.admin.edit_handlers import FieldPanel
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.snippets.models import register_snippet

from .blog_detail_page import BlogDetailPage
from .blog_category import BlogCategory


class BlogListingPage(RoutablePageMixin, Page):
    """Listing page lists all the Blog Detail Pages."""

    template = "blog/blog_listing_page.html"

    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Overwrites the default title',
    )

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
    ]

    def get_context(self, request, *args, **kwargs):
        """ Adding custom stuff into our context"""
        context = super().get_context(request, *args, **kwargs)
        # "posts" will have child pages; you'll need to use .specific in the template
        # in order to access child properties, such as youtube_video_id and subtitle
        # context["posts"] = BlogDetailPage.objects.live().public()

        # Get all posts
        all_posts = BlogDetailPage.objects.live().public().order_by('-first_published_at')
        # Paginate all posts by 2 per page
        paginator = Paginator(all_posts, 2)
        # Try to get the ?page=x value
        page = request.GET.get("page")
        try:
            # If the page exists and the ?page=x is an int
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If the ?page=x is not an int; show the first page
            posts = paginator.page(1)
        except EmptyPage:
            # If the ?page=x is out of range (too high most likely)
            # Then return the last page
            posts = paginator.page(paginator.num_pages)

        context["posts"] = posts
        context["page_title"] = "Blog List"
        context["special_link"] = self.reverse_subpage('latest_post')
        return context

    @route(r'^latest/?$', name="latest_post")
    def show_latest_blog(self, request, *arg, **kwarg):
        context = self.get_context(request, *arg, **kwarg)
        context['posts'] = context['posts'][:1]
        context["categories"] = BlogCategory.objects.all()
        context["page_title"] = "Latest Blog List"

        return render(request, "blog/latest_blog.html", context)

    @route(r'^past/$')
    def past_events(self, request):
        """
        View function for the past events page
        """

        # NOTE: We are overriding the template here, as well as few context values
        return self.render(
            request,
            context_overrides={
                'title': "Past events",
            },
            template="blog/past_events.html",
        )
