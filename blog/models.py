from django.db import models
from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from wagtail.core.models import Page, Orderable
from django.shortcuts import render
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, InlinePanel
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from streams import blocks
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.snippets.models import register_snippet


class BlogAuthorsOrderable(Orderable):
    """This allows us to select one or more blog authors from Snippets."""

    page = ParentalKey("blog.BlogDetailPage", related_name="blog_authors")
    author = models.ForeignKey(
        "blog.BlogAuthor",
        on_delete=models.CASCADE,
    )

    panels = [
        SnippetChooserPanel("author"),
    ]


class BlogAuthor(models.Model):
    """ Blog Author Snippet """
    name = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name='+'
    )

    panels = [
            MultiFieldPanel(
                [
                    FieldPanel("name"),
                    ImageChooserPanel("image"),
                ],
                heading="Name and Image",
            ),
            MultiFieldPanel(
                [
                    FieldPanel("website"),
                ],
                heading="Links"
            )
        ]

    def __str__(self):
        """String repr of this class."""
        return self.name

    class Meta:  # noqa
        verbose_name = "Blog Author"
        verbose_name_plural = "Blog Authors"


register_snippet(BlogAuthor)


class BlogCategory(models.Model):
    """ Blog category for snippet """

    name = models.CharField(max_length=255)
    slug = models.SlugField(
        verbose_name='slug',
        allow_unicode=True,
        max_length=255,
        help_text='A slug to identify posts by this category',
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('slug')
    ]

    class Meta:
        verbose_name = 'Blog Category'
        verbose_name_plural = 'Blog categories'
        ordering = ['name']

    def __str__(self):
        return self.name


register_snippet(BlogCategory)


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


# Second subclassed page
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

