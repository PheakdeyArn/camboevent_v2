from django.db import models

from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, InlinePanel
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.core.fields import StreamField, RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from streams import blocks
from django.utils import timezone
from users.models import User

from .like import ScholarshipLikes


class ScholarshipDetailPage(Page):

    # template = "content/scholarship_detail.html"

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

    scholarship_category = models.ForeignKey(
        "content.ScholarshipCategory",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    # Exam - Date & Time
    exam_date = models.DateField("Exam Date")
    exam_time = models.TimeField("Exam Time")

    # Exam - Date & Time
    deadline_date = models.DateField("Deadline Date")
    deadline_time = models.TimeField("Deadline Time", blank=True, null=False)

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

    more_detail = RichTextField(blank=True)
    link = models.URLField(blank=True, null=True)
    submit_form_link = models.URLField(blank=True, null=True)

    favourites = models.ManyToManyField(User, related_name='favourite_scholarship', default=None, blank=True)

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
        # FieldPanel("test_field"),
        ImageChooserPanel("banner_image"),
        FieldPanel('scholarship_category', heading="Category"),
        MultiFieldPanel(
            [
                InlinePanel("authors", label="Author", min_num=1, max_num=4)
            ],
            heading="Author(s)"
        ),
        MultiFieldPanel(
            [
                FieldPanel('exam_date'),
                FieldPanel('exam_time'),
            ],
            heading="Exam Date & Time"
        ),
        MultiFieldPanel(
            [
                FieldPanel('deadline_date'),
                FieldPanel('deadline_time'),
            ],
            heading="Deadline Date & Time"
        ),
        MultiFieldPanel(
            [
                InlinePanel("organizations", label="Organization", min_num=1, max_num=5)
            ],
            heading="Organization(s)"
        ),
        MultiFieldPanel(
            [
                FieldPanel('address', heading="Address"),
                FieldPanel('city', heading="City"),
                FieldPanel('country', heading="Country"),
                FieldPanel('link', heading="Learn More"),
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

        likes = ScholarshipLikes.objects.filter(post=self.id).count()
        print("++++++++++++++++++++++++++++")
        print(likes)

        fav = False
        if self.favourites.filter(id=request.user.id).exists():
            fav = True

        context["fav"] = fav
        context["page_title"] = "Event List"

        return context



