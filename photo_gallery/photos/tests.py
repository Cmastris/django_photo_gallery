import datetime
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.test import RequestFactory, tag, TestCase
from django.urls import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from pathlib import Path

from .admin import PhotoAdmin
from .models import Collection, Photo, validate_lowercase


def create_uploaded_file_object(image_path):
    """Create a `SimpleUploadedFile` object using a specified image path."""
    return SimpleUploadedFile(name='test_image.jpg',
                              content=open(image_path, 'rb').read(),
                              content_type='image/jpeg')


class MockPhotoImages(models.Model):
    large_img_path = Path(__file__).resolve().parent / 'test_images/2500x1500.jpg'
    mock_large_upload = create_uploaded_file_object(large_img_path)
    downsized_image = ImageSpecField(source='mock_large_upload',
                                     processors=[ResizeToFit(width=500)],
                                     format='JPEG')

    small_img_path = Path(__file__).resolve().parent / 'test_images/200x100.jpg'
    mock_small_upload = create_uploaded_file_object(large_img_path)
    upsized_image = ImageSpecField(source='mock_small_upload',
                                   processors=[ResizeToFit(width=500)],
                                   format='JPEG')


@tag('models')
class PhotoModelTests(TestCase):

    def test_image_downsizing(self):
        """Test that ImageSpecField downsizes a mock upload image to a width of 500px."""
        photo = MockPhotoImages()
        self.assertEqual(photo.downsized_image.width, 500)

    def test_image_upsizing(self):
        """Test that ImageSpecField upsizes a mock upload image to a width of 500px."""
        photo = MockPhotoImages()
        self.assertEqual(photo.upsized_image.width, 500)

    def test_photo_str(self):
        """Test the Photo __str__ method."""
        photo = create_photo(title="Test Title", slug="test-slug")
        self.assertEqual(photo.__str__(), "Test Title (test-slug)")


class MockPhotoAdmin(PhotoAdmin):
    def __init__(self):
        pass


@tag('admin')
class PhotoAdminTests(TestCase):

    request = RequestFactory()

    def test_get_fields_add(self):
        """Test that `thumbnail_img_tag` is excluded from add view `fields`"""
        photo_admin = MockPhotoAdmin()
        fields = photo_admin.get_fields(self.request)
        self.assertEqual(fields, ['large_image', 'title', 'slug', 'description', 'location',
                                  'country', 'date_taken', 'collections', 'featured', 'published'])

    def test_get_fields_change(self):
        """Test that `thumbnail_img_tag` is included in change view `fields`"""
        photo_admin = MockPhotoAdmin()
        fields = photo_admin.get_fields(self.request, obj=MockPhotoImages())
        self.assertEqual(fields, ['large_image', 'thumbnail_img_tag', 'title', 'slug',
                                  'description', 'location', 'country', 'date_taken',
                                  'collections', 'featured', 'published'])


def create_photo(slug, title="Photo", description="Description", location="Location",
                 date_taken=datetime.date(2022, 1, 1), featured=False, published=True,
                 collections=None):

    large_img_path = Path(__file__).resolve().parent / 'test_images/2500x1500.jpg'
    mock_large_upload = create_uploaded_file_object(large_img_path)

    photo = Photo.objects.create(slug=slug, title=title, description=description, location=location,
                                 date_taken=date_taken, featured=featured, published=published,
                                 large_image=mock_large_upload)

    if collections is not None:
        photo.collections.set(collections)
        photo.save()

    return photo


def create_published_photos(num):
    for x in range(num):
        create_photo(slug="test-slug-" + str(x+1), published=True)


@tag('views', 'photo_detail')
class PhotoDetailViewTests(TestCase):

    def test_published_photo_status(self):
        """Test that a published Photo returns a 200 status code."""
        test_slug = "published-photo"
        create_photo(slug=test_slug, published=True)
        response = self.client.get(reverse("photo_detail", kwargs={"slug": test_slug}))
        self.assertEqual(response.status_code, 200)

    def test_unpublished_photo_status(self):
        """Test that an unpublished Photo returns a 404 status code."""
        test_slug = "unpublished-photo"
        create_photo(slug=test_slug, published=False)
        response = self.client.get(reverse("photo_detail", kwargs={"slug": test_slug}))
        self.assertEqual(response.status_code, 404)

    def test_404_photo_status(self):
        """Test that a slug without an associated Photo returns a 404 status code."""
        test_slug = "404-slug"
        response = self.client.get(reverse("photo_detail", kwargs={"slug": test_slug}))
        self.assertEqual(response.status_code, 404)

    def test_photo_image_in_response(self):
        """Test that a published photo response contains the photo image URLs."""
        test_slug = "image-test"
        photo = create_photo(slug=test_slug, published=True)
        response = self.client.get(reverse("photo_detail", kwargs={"slug": test_slug}))
        self.assertContains(response, photo.large_image.url)
        self.assertContains(response, photo.small_image.url)

    def test_photo_title_in_response(self):
        """Test that a published photo response contains the photo title."""
        test_slug = "title-test"
        test_title = "Test Title"
        create_photo(slug=test_slug, title=test_title, published=True)
        response = self.client.get(reverse("photo_detail", kwargs={"slug": test_slug}))
        self.assertContains(response, test_title)

    def test_photo_description_in_response(self):
        """Test that a published photo response contains the photo description."""
        test_slug = "description-test"
        test_description = "This is a test description."
        create_photo(slug=test_slug, description=test_description, published=True)
        response = self.client.get(reverse("photo_detail", kwargs={"slug": test_slug}))
        self.assertContains(response, test_description)

    def test_collections_in_response(self):
        """Test that the response of a photo in >0 collections contains collections text."""
        col = Collection.objects.create(name="Published Col", slug="test-col", published=True)
        test_slug = "has-collections"
        create_photo(slug=test_slug, published=True, collections=[col])
        response = self.client.get(reverse("photo_detail", kwargs={"slug": test_slug}))
        self.assertContains(response, "Collections:")

    def test_collections_not_in_response(self):
        """Test that the response of a photo in 0 collections doesn't contain collections text."""
        Collection.objects.create(name="Published Col", slug="test-col", published=True)
        test_slug = "no-collections"
        create_photo(slug=test_slug, published=True, collections=None)
        response = self.client.get(reverse("photo_detail", kwargs={"slug": test_slug}))
        self.assertNotContains(response, "Collections:")


@tag('views', 'photo_list')
class PhotoListViewTests(TestCase):
    def test_qs_unpublished_filtering(self):
        """Test that only `published` Photos are included in the queryset."""
        published_photo = create_photo(slug="published-photo", published=True)
        create_photo(slug="unpublished-photo", published=False)

        response = self.client.get(reverse("homepage"))
        self.assertQuerysetEqual(response.context['photo_list'], [published_photo])

    def test_qs_featured_ordering(self):
        """Test that `featured` Photos are ordered first in the queryset."""
        create_photo(slug="unfeatured1", featured=False)
        featured_photo = create_photo(slug="featured", featured=True)
        create_photo(slug="unfeatured2", featured=False)

        response = self.client.get(reverse("homepage"))
        self.assertEqual(response.context['photo_list'][0], featured_photo)

    def test_qs_date_taken_ordering(self):
        """Test that Photos are ordered by descending `date_taken` in the queryset."""
        p_2021 = create_photo(slug="2021", date_taken=datetime.date(2021, 1, 1))
        p_2022 = create_photo(slug="2022", date_taken=datetime.date(2022, 1, 1))
        p_2020 = create_photo(slug="2020", date_taken=datetime.date(2020, 1, 1))

        response = self.client.get(reverse("homepage"))
        self.assertQuerysetEqual(response.context['photo_list'], [p_2022, p_2021, p_2020])

    def test_qs_combined_ordering(self):
        """Test that Photos are ordered by descending `featured` then by descending `date_taken`"""
        old_date = datetime.date(2020, 1, 1)
        new_date = datetime.date(2022, 1, 1)
        p_unfeatured_old = create_photo(slug="unfeatured-old", featured=False, date_taken=old_date)
        p_featured_new = create_photo(slug="featured-new", featured=True, date_taken=new_date)
        p_unfeatured_new = create_photo(slug="unfeatured-new", featured=False, date_taken=new_date)
        p_featured_old = create_photo(slug="featured-old", featured=True, date_taken=old_date)

        response = self.client.get(reverse("homepage"))
        expected_qs = [p_featured_new, p_featured_old, p_unfeatured_new, p_unfeatured_old]
        self.assertQuerysetEqual(response.context['photo_list'], expected_qs)

    def test_qs_new_ordering(self):
        """Test that Photos are ordered by descending `date_taken` with the `new` query string"""
        old_date = datetime.date(2020, 1, 1)
        mid_date = datetime.date(2021, 1, 1)
        new_date = datetime.date(2022, 1, 1)
        p_unfeatured_old = create_photo(slug="unfeatured-old", featured=False, date_taken=old_date)
        p_unfeatured_new = create_photo(slug="unfeatured-new", featured=False, date_taken=new_date)
        p_featured_mid = create_photo(slug="featured-mid", featured=True, date_taken=mid_date)

        response = self.client.get(reverse("homepage") + "?sort=new")
        expected_qs = [p_unfeatured_new, p_featured_mid, p_unfeatured_old]
        self.assertQuerysetEqual(response.context['photo_list'], expected_qs)

    def test_qs_old_ordering(self):
        """Test that Photos are ordered by ascending `date_taken` with the `old` query string"""
        old_date = datetime.date(2020, 1, 1)
        mid_date = datetime.date(2021, 1, 1)
        new_date = datetime.date(2022, 1, 1)
        p_featured_mid = create_photo(slug="featured-mid", featured=True, date_taken=mid_date)
        p_unfeatured_new = create_photo(slug="unfeatured-new", featured=False, date_taken=new_date)
        p_unfeatured_old = create_photo(slug="unfeatured-old", featured=False, date_taken=old_date)

        response = self.client.get(reverse("homepage") + "?sort=old")
        expected_qs = [p_unfeatured_old, p_featured_mid, p_unfeatured_new]
        self.assertQuerysetEqual(response.context['photo_list'], expected_qs)

    def test_paginated_200_status(self):
        """Test that a paginated URL with at least 1 associated Photo returns a 200 status code."""
        # `paginate_by = 6` (6 photos per page)
        create_published_photos(7)
        response = self.client.get(reverse("homepage"), {"page": 2})
        self.assertEqual(response.status_code, 200)

    def test_paginated_404_status(self):
        """Test that a paginated URL with no associated Photos returns a 404 status code."""
        # `paginate_by = 6` (6 photos per page)
        create_photo(slug="test", published=True)
        response = self.client.get(reverse("homepage"), {"page": 2})
        self.assertEqual(response.status_code, 404)


@tag('views', 'collection')
class CollectionViewTests(TestCase):
    def test_published_collection_status(self):
        """Test that a published Collection returns a 200 status code."""
        col = Collection.objects.create(name="Published Col", slug="test-col", published=True)
        response = self.client.get(reverse("collection", kwargs={"collection_slug": col.slug}))
        self.assertEqual(response.status_code, 200)

    def test_unpublished_collection_status(self):
        """Test that an unpublished Collection returns a 404 status code."""
        col = Collection.objects.create(name="Unpublished Col", slug="test-col", published=False)
        create_photo(slug="published-photo", published=True, collections=[col])
        response = self.client.get(reverse("collection", kwargs={"collection_slug": col.slug}))
        self.assertEqual(response.status_code, 404)

    def test_404_collection_status(self):
        """Test that a slug without an associated Collection returns a 404 status code."""
        response = self.client.get(reverse("collection", kwargs={"collection_slug": "404-slug"}))
        self.assertEqual(response.status_code, 404)

    def test_qs_unpublished_filtering(self):
        """Test that only `published` Photos are included in the collection queryset."""
        col = Collection.objects.create(name="Test Col", slug="test-col", published=True)
        published_photo = create_photo(slug="published-photo", published=True, collections=[col])
        create_photo(slug="unpublished-photo", published=False, collections=[col])

        response = self.client.get(reverse("collection", kwargs={"collection_slug": col.slug}))
        self.assertQuerysetEqual(response.context['photo_list'], [published_photo])

    def test_qs_collection_filtering(self):
        """Test that only Photos in a collection are included in the collection queryset."""
        col1 = Collection.objects.create(name="Col 1", slug="col-1", published=True)
        col2 = Collection.objects.create(name="Col 2", slug="col-2", published=True)
        photo1 = create_photo(slug="photo-1", published=True, collections=[col1])
        create_photo(slug="photo-2", published=True, collections=None)
        create_photo(slug="photo-3", published=True, collections=[col2])

        response = self.client.get(reverse("collection", kwargs={"collection_slug": col1.slug}))
        self.assertQuerysetEqual(response.context['photo_list'], [photo1])

    def test_qs_multiple_collection_filtering(self):
        """Test that Photos with multiple collections are included in the collection queryset."""
        col1 = Collection.objects.create(name="Col 1", slug="col-1", published=True)
        col2 = Collection.objects.create(name="Col 2", slug="col-2", published=True)
        photo = create_photo(slug="photo-1", published=True, collections=[col2, col1])

        response = self.client.get(reverse("collection", kwargs={"collection_slug": col1.slug}))
        self.assertQuerysetEqual(response.context['photo_list'], [photo])

    def test_collection_name_in_response(self):
        """Test that a published collection response contains the collection name."""
        test_name = "Collection Test Name"
        col = Collection.objects.create(name=test_name, slug="test-collection", published=True)
        response = self.client.get(reverse("collection", kwargs={"collection_slug": col.slug}))
        self.assertContains(response, test_name)

    def test_collection_description_in_response(self):
        """Test that a published collection response contains the collection description."""
        test_description = "This is a test description."
        col = Collection.objects.create(name="Test Name",
                                        description=test_description,
                                        slug="test-col",
                                        published=True)

        response = self.client.get(reverse("collection", kwargs={"collection_slug": col.slug}))
        self.assertContains(response, test_description)

    def test_photo_link_in_response(self):
        """Test that a published collection response contains an associated photo URL."""
        col = Collection.objects.create(name="Published Col", slug="test-col", published=True)
        photo = create_photo(slug="test-photo-slug", published=True, collections=[col])
        response = self.client.get(reverse("collection", kwargs={"collection_slug": col.slug}))
        self.assertContains(response, photo.get_absolute_url())


@tag('views', 'search')
class SearchViewTests(TestCase):
    def test_qs_search_query_filtering(self):
        """Test that only Photos that match a search criteria are included in the queryset."""
        match1 = create_photo(slug="p1", title="TestSearch", description="desc", location="loc",
                              date_taken=datetime.date(2022, 1, 1))
        create_photo(slug="p2", title="title", description="desc", location="loc",
                     date_taken=datetime.date(2021, 1, 1))
        match2 = create_photo(slug="p3", title="title", description="testsearch", location="loc",
                              date_taken=datetime.date(2020, 1, 1))
        match3 = create_photo(slug="p4", title="title", description="desc", location="testsearch",
                              date_taken=datetime.date(2019, 1, 1))

        response = self.client.get(reverse("search") + "?query=testsearch")
        expected_qs = [match1, match2, match3]
        self.assertQuerysetEqual(response.context['photo_list'], expected_qs)


@tag('validators')
class ValidatorTests(TestCase):
    def test_lowercase_validates(self):
        """Test that `validate_lowercase()` doesn't incorrectly raise a ValidationError"""
        lower_str = "lowercase-string-100! "
        try:
            validate_lowercase(lower_str)
        except ValidationError:
            self.fail("validate_lowercase() raised ValidationError unexpectedly "
                      "for string `{}`.".format(lower_str))

    def test_lowercase_raises(self):
        """Test that `validate_lowercase()` correctly raises a ValidationError"""
        mixed_case_str = "mixed-Case-string-100! "
        with self.assertRaises(ValidationError):
            validate_lowercase(mixed_case_str)
