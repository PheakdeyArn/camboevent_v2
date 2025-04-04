from django.db import models

from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, InlinePanel
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.core.fields import StreamField, RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from streams import blocks
from django.utils import timezone
from users.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect


from users.forms import NewCommentForm
from .like import EventLikes


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

    favourites = models.ManyToManyField(User, related_name='favourite_event', default=None, blank=True)

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


    def get_context(self, request, *args, **kwargs):
        """ Adding custom stuff into our context"""
        context = super().get_context(request, *args, **kwargs)
        # "posts" will have child pages; you'll need to use .specific in the template
        # in order to access child properties, such as youtube_video_id and subtitle
        # context["events"] = EventDetailPage.objects.live().public()

        # get comment
        likes = EventLikes.objects.filter(post=self.id).count()
        print("++++++++++++++++++++++++++++")
        print(likes)

        allcomments = self.events_comments.filter(status=True)
        #
        print("+++++++++", allcomments)
        page = request.GET.get('page', 1)

        paginator = Paginator(allcomments, 10)
        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)

        fav = False
        is_like = False

        user_event_like = EventLikes.objects.filter(post_id=self.id, user=request.user.id, status=True)
        user_event_like_id = [x.post_id for x in user_event_like]

        if self.favourites.filter(id=request.user.id).exists():
            fav = True

        if self.id in user_event_like_id:
            is_like = True

        user_comment = None
        if request.method == 'POST':
            comment_form = NewCommentForm(request.POST)
            if comment_form.is_valid():
                user_comment = comment_form.save(commit=False)
                user_comment.post = self
                user_comment.save()
                # return HttpResponseRedirect('/', context)
                # return redirect('/' + self.slug)

        else:
            comment_form = NewCommentForm()

        context["fav"] = fav
        context["is_like"] = is_like
        context["page_title"] = "Event List"
        context["allcomments"] = allcomments
        context["comments"] = comments
        context["comment_form"] = comment_form

        return context


