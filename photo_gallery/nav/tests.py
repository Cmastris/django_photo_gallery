from django.test import override_settings, tag, TestCase
from django.urls import reverse

from photos.models import Collection
from photos.tests import create_photo, TEST_MEDIA_DIR
from .models import NavSection, NavLink


def create_nav_section(order, dropdown=False):
    if dropdown:
        section = NavSection.objects.create(section_order=order, dropdown_label="Label")
        NavLink.objects.create(link_text="Link 1", link_url="/link-1", vertical_order=1,
                               nav_section=section)
        NavLink.objects.create(link_text="Link 2", link_url="/link-2", vertical_order=2,
                               nav_section=section)

    else:
        section = NavSection.objects.create(section_order=order, dropdown_label="")
        NavLink.objects.create(link_text="Link", link_url="/link", nav_section=section)

    return section


@tag('nav', 'context_processors')
@override_settings(MEDIA_ROOT=TEST_MEDIA_DIR)
class NavContextTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up data for all tests in this class."""
        cls.section2 = create_nav_section(2, dropdown=True)
        cls.section1 = create_nav_section(1)
        cls.section3 = create_nav_section(3)

    @tag('photo_list')
    def test_homepage_nav_context(self):
        """Test that the homepage context includes correctly ordered NavSection objects."""
        response = self.client.get(reverse("homepage"))
        self.assertQuerysetEqual(response.context['nav_sections'],
                                 [self.section1, self.section2, self.section3])

    @tag('photo_list')
    def test_collection_nav_context(self):
        """Test that a collection page context includes correctly ordered NavSection objects."""
        col = Collection.objects.create(name="Col1", slug="test-collection", published=True)
        response = self.client.get(reverse("collection", kwargs={"collection_slug": col.slug}))
        self.assertQuerysetEqual(response.context['nav_sections'],
                                 [self.section1, self.section2, self.section3])

    @tag('photo_detail')
    def test_photo_detail_nav_context(self):
        """Test that a photo detail page context includes correctly ordered NavSection objects."""
        photo = create_photo(slug="test-photo", published=True)
        response = self.client.get(reverse("photo_detail", kwargs={"slug":photo.slug}))
        self.assertQuerysetEqual(response.context['nav_sections'],
                                 [self.section1, self.section2, self.section3])
