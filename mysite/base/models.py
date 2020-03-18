from django.db import models
from django_extensions.db.fields import AutoSlugField
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.core import blocks
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, StreamFieldPanel, PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.snippets.models import register_snippet
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

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        blogpages = BlogPage.objects.live().order_by("-first_published_at")
        context["blogpages"] = blogpages
        return context

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
    resume = models.ForeignKey(
        'wagtaildocs.Document',
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
        DocumentChooserPanel('resume'),
        StreamFieldPanel('body'),
    ]


class BlogPage(Page):
    """
    Blog
    """
    featured_intro = models.CharField(max_length=250, blank=False, null=True)
    body =StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ("image", ImageChooserBlock()),
    ])
    date = models.DateField("Post date", null=True, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("featured_intro"),
        StreamFieldPanel("body"),
        FieldPanel("date")
    ]


class BlogIndexPage(Page):
    """
    Blog Index page
    """
    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by("-first_published_at")
        context["blogpages"] = blogpages
        return context

    content_panels = Page.content_panels

class Projects(Orderable):
    """

    """
    project_name = models.CharField(max_length=250)
    project_description = models.CharField(max_length=250)
    project_url = models.URLField()

    page = ParentalKey(
        "ProjectsPage", related_name="projects",
    )
    panels =[
        FieldPanel("project_name"),
        FieldPanel("project_description"),
        FieldPanel("project_url"),
    ]

class ProjectsPage(Page):
    """
    Projects
    """

    content_panels = Page.content_panels + [
        InlinePanel("projects", label="Projects")
    ]



# Snippets
class MenuItem(Orderable):
    link_title = models.CharField(max_length=250, blank=True, null=True)
    link_url = models.CharField(max_length=250, blank=True, null=True)
    link_page = models.ForeignKey(
        "wagtailcore.Page",
        blank=True,
        null=True,
        related_name="+",
        on_delete=models.CASCADE,
    )
    open_in_new_tab = models.BooleanField(default=False, blank=True)

    page = ParentalKey("Menu", related_name="menu_items")

    panels=[
        FieldPanel("link_title"),
        FieldPanel("link_url"),
        PageChooserPanel("link_page"),
        FieldPanel("open_in_new_tab"),
    ]

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_url:
            self.link_url
        return "#"

    @property
    def title(self):
        if self.link_page:
            return self.link_page.title
        elif self.link_title:
            return self.link_title
        return "Missing title"


@register_snippet
class Menu(ClusterableModel):
    """

    """
    title = models.CharField(max_length=250)
    slug = AutoSlugField(populate_from="title", editable=True)

    panels =[
        MultiFieldPanel([
            FieldPanel("title"),
            FieldPanel("slug"),
        ], heading="Menu"),
        InlinePanel("menu_items",label="Menu Items" )
    ]

    def __str__(self):
        return self.title


class FooterContact(Orderable):
    link_title = models.CharField(max_length=250, blank=True, null=True)
    link_url = models.CharField(max_length=250, blank=True, null=True)
    link_class = models.CharField(max_length=250, blank=True, null=True)

    page = ParentalKey("Footer", related_name="footer_contacts")

    panels = [
        FieldPanel("link_title"),
        FieldPanel("link_url"),
        FieldPanel("link_class"),
    ]

@register_snippet
class Footer(ClusterableModel):
    """

    """
    title = models.CharField(max_length=250)
    slug = AutoSlugField(populate_from="title", editable=True)

    footer_heading = models.CharField(max_length=250)
    panels=[
        MultiFieldPanel([
            FieldPanel("title"),
            FieldPanel("slug"),
        ], heading="Footer"),
        FieldPanel("footer_heading"),
        InlinePanel("footer_contacts", label="Footer Contacts")
    ]

    def __str__(self):
        return self.title


@register_snippet
class Header(models.Model):
    """

    """
    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    panels = [
        ImageChooserPanel("logo"),
    ]