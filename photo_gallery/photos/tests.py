import datetime
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.test import RequestFactory, TestCase
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from pathlib import Path

from .admin import PhotoAdmin
from .models import Photo, validate_lowercase


def create_uploaded_file_object(image_path):
    """Create a `SimpleUploadedFile` object using a specified image path."""
    return SimpleUploadedFile(name='test_image.jpg',
                              content=open(image_path, 'rb').read(),
                              content_type='image/jpeg')


class MockPhoto(models.Model):
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


class PhotoModelTests(TestCase):

    def test_image_downsizing(self):
        """Test that ImageSpecField downsizes a mock upload image to a width of 500px."""
        photo = MockPhoto()
        self.assertEqual(photo.downsized_image.width, 500)

    def test_image_upsizing(self):
        """Test that ImageSpecField upsizes a mock upload image to a width of 500px."""
        photo = MockPhoto()
        self.assertEqual(photo.upsized_image.width, 500)

    def test_photo_str(self):
        """Test the Photo __str__ method."""
        date = datetime.date(2022, 1, 1)
        photo = Photo.objects.create(title="Test Title", slug="test-slug", date_taken=date)

        self.assertEqual(photo.__str__(), "Test Title (test-slug)")


class MockPhotoAdmin(PhotoAdmin):
    def __init__(self):
        pass


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
        fields = photo_admin.get_fields(self.request, obj=MockPhoto())
        self.assertEqual(fields, ['large_image', 'thumbnail_img_tag', 'title', 'slug',
                                  'description', 'location', 'country', 'date_taken',
                                  'collections', 'featured', 'published'])


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
