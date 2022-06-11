from django import forms
from django.db import models
from wagtail.core.models import Page, Orderable
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, InlinePanel, PageChooserPanel
from wagtail.snippets.models import register_snippet


class BlogTagsOrderable(Orderable):
    """to select either one or more blog tags from the snippets"""
    page = ParentalKey('blog.BlogDetailPage', related_name='blog_tags')
    tag = models.ForeignKey(
        'blog.BlogTag',  # link to model 'BlogTag' of app 'blog',
        on_delete=models.CASCADE,
    )   # this is a Django model

    panels = [
        SnippetChooserPanel('tag'),  # SnippetChooserPanel => to choose a snippet not field or image
    ]


class BlogTag(models.Model):
    """Blog tag for snippets"""
    name = models.CharField(max_length=100)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('name'),
            ],
            heading='Name of tag'
        ),

    ]

    def __str__(self):
        """string repr of this tag class"""
        return self.name

    class Meta:
        verbose_name = 'Blog Tag'
        verbose_name_plural = 'Blog Tags'


register_snippet(BlogTag)
