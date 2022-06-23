# Generated by Django 3.2.13 on 2022-06-23 08:08

from django.db import migrations, models
import django.db.models.deletion
import streams.blocks
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_rename_bloglikestest_bloglikes'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloglistingpage',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='blog.blogcategory'),
        ),
        migrations.AddField(
            model_name='bloglistingpage',
            name='content',
            field=wagtail.core.fields.StreamField([('h2', streams.blocks.H2Block()), ('h3', streams.blocks.H3Block()), ('h4', streams.blocks.H4Block()), ('quote', wagtail.core.blocks.StructBlock([('quote', wagtail.core.blocks.BlockQuoteBlock(required=True)), ('quote_by', wagtail.core.blocks.CharBlock(max_length=50, required=False))])), ('carousel', wagtail.core.blocks.StructBlock([('carousel', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('title', wagtail.core.blocks.CharBlock(max_length=40, required=False)), ('text', wagtail.core.blocks.TextBlock(max_length=200, required=False)), ('button_page', wagtail.core.blocks.PageChooserBlock(required=False)), ('button_url', wagtail.core.blocks.URLBlock(help_text='If the button page above is selected, that will be used first.', required=False))])))])), ('cta', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=60, required=True)), ('text', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic'], required=True)), ('button_page', wagtail.core.blocks.PageChooserBlock(required=False)), ('button_url', wagtail.core.blocks.URLBlock(required=False)), ('button_text', wagtail.core.blocks.CharBlock(default='Learn More', max_length=40, required=True))]))], blank=True, null=True),
        ),
    ]
