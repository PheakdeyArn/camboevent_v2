"""  streamFields """
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class TitleAndTextBlock(blocks.StructBlock):
    """ Title and Text """
    title = blocks.CharBlock(required=True, help_text='Add your title')
    text = blocks.TextBlock(required=True, help_text='Add additional text')

    class Meta:
        template = "streams/title_and_text_block.html"
        icon = "edit"
        label = "Title & text"


class CardBlock(blocks.StructBlock):
    """Cards with image and text and button(s)."""

    title = blocks.CharBlock(required=True, help_text="Add your title")

    cards = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image", ImageChooserBlock(required=True)),
                ("title", blocks.CharBlock(required=True, max_length=40)),
                ("text", blocks.TextBlock(required=True, max_length=200)),
                ("button_page", blocks.PageChooserBlock(required=False)),
                ("button_url", blocks.URLBlock(
                    required=False,
                    help_text="If the button page above is selected, that will be used first."
                )),
            ]
        )
    )

    class Meta:  # noqa
        template = "streams/card_block.html"
        icon = "placeholder"
        label = "Staff Cards"


class RichTextBlock(blocks.RichTextBlock):
    """Richtext with all the features."""

    class Meta:  # noqa
        template = "streams/richText_block.html"
        icon = "doc-full"
        label = "Full RichText"


class SimpleRichTextBlock(blocks.RichTextBlock):
    """Richtext without (limited) all the features."""

    def __init__(self, required=True, help_text=None, editor="default", features=None, **kwargs):  # noqa
        super().__init__(**kwargs)
        self.features = ["bold", "italic", "link"]

    class Meta:  # noqa
        template = "streams/richText_block.html"
        icon = "edit"
        label = "Simple RichText"


class CTABlock(blocks.StructBlock):
    """A simple call to action section."""

    title = blocks.CharBlock(required=True, max_length=60)
    text = blocks.RichTextBlock(required=True, features=["bold", "italic"])
    button_page = blocks.PageChooserBlock(required=False)
    button_url = blocks.URLBlock(required=False)
    button_text = blocks.CharBlock(required=True, default='Learn More', max_length=40)

    class Meta:  # noqa
        template = "streams/cta_block.html"
        icon = "placeholder"
        label = "Call to Action"


class LinkStructValue(blocks.StructValue):
    """Additional logic for our urls."""

    def url(self):
        button_page = self.get('button_page')
        button_url = self.get('button_url')
        if button_page:
            return button_page.url
        elif button_url:
            return button_url

        return None


class ButtonBlock(blocks.StructBlock):
    """An external or internal URL."""

    button_page = blocks.PageChooserBlock(required=False, help_text='If selected, this url will be used first')
    button_url = blocks.URLBlock(required=False, help_text='If added, this url will be used secondarily to the button page')

    class Meta:  # noqa
        template = "streams/button_block.html"
        icon = "placeholder"
        label = "Single Button"
        value_class = LinkStructValue


class SingleImageBlock(blocks.StructBlock):

    image = ImageChooserBlock(required=True)

    class Meta:  # noqa
        template = "streams/single_image_block.html"
        icon = "image"
        label = "Single Image"


class ImageAndCaptionBlock(blocks.StructBlock):

    caption = blocks.RichTextBlock(required=True, features=["bold", "italic"])
    image = ImageChooserBlock(required=True)

    class Meta:  # noqa
        template = "streams/image_and_caption_block.html"
        icon = "image"
        label = "Image & Caption"


class CarouselBlock(blocks.StructBlock):
    """Slider with title and text and button(s)."""

    carousel = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image", ImageChooserBlock(required=True)),
                ("title", blocks.CharBlock(required=False, max_length=40)),
                ("text", blocks.TextBlock(required=False, max_length=200)),
                ("button_page", blocks.PageChooserBlock(required=False)),
                ("button_url", blocks.URLBlock(
                    required=False,
                    help_text="If the button page above is selected, that will be used first."
                )),
            ]
        )
    )

    class Meta:  # noqa
        template = "streams/carousel_block.html"
        icon = "image"
        label = "Carousel"


class GalleryBlock(blocks.StructBlock):

    images = blocks.ListBlock(ImageChooserBlock(required=True))

    class Meta:  # noqa
        template = "streams/gallery_block.html"
        icon = "image"
        label = "Gallery"


class H2Block(blocks.RichTextBlock):

    def __init__(self, required=True, help_text=None, editor="default", features='h2', **kwargs):  # noqa
        super().__init__(**kwargs)
        self.features = ["h2"]

    class Meta:  # noqa
        template = "streams/richText_block.html"
        icon = "edit"
        label = "H2"


class H3Block(blocks.RichTextBlock):

    def __init__(self, required=True, help_text=None, editor="default", features=None, **kwargs):  # noqa
        super().__init__(**kwargs)
        self.features = ["h3"]

    class Meta:  # noqa
        template = "streams/richText_block.html"
        icon = "edit"
        label = "H3"


class H4Block(blocks.RichTextBlock):

    def __init__(self, required=True, help_text=None, editor="default", features=None, **kwargs):  # noqa
        super().__init__(**kwargs)
        self.features = ["h4"]

    class Meta:  # noqa
        template = "streams/richText_block.html"
        icon = "edit"
        label = "H4"


class QuoteBlock(blocks.StructBlock):

    quote = blocks.BlockQuoteBlock(required=True)
    quote_by = blocks.CharBlock(max_length=50, required=False)

    class Meta:  # noqa
        template = "streams/quote_block.html"
        icon = "edit"
        label = "Quote"


