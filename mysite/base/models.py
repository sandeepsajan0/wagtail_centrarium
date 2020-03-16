from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.core import blocks
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index

# Create your models here.

class HomePage(Page):
    """
    Home
    """
    name = models.CharField(max_length=250)
    profession = models.CharField(max_length=250)
    bg_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('profession'),
        ImageChooserPanel('bg_image'),
    ]

class AboutPage(Page):
    """
    About
    """
    profile_pic=  models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    body = StreamField([
        ('paragraph', blocks.RichTextBlock()),
    ])

    content_panels = Page.content_panels + [
        ImageChooserPanel('profile_pic'),
        StreamFieldPanel('body'),
    ]

class BlogPage(Page):
    """
    Blog
    """
    body =StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ("image", ImageChooserBlock()),
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel("body"),
    ]