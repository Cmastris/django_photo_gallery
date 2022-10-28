from django.test import tag, TestCase
from django.urls import reverse


@tag('views', 'contact')
class TestContactMessageCreateView(TestCase):
    def test_200_status(self):
        """Test that a GET request returns a 200 status."""
        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)


@tag('views', 'contact')
class TestContactSuccessView(TestCase):
    def test_200_status(self):
        """Test that a request returns a 200 status."""
        response = self.client.get(reverse("contact_success"))
        self.assertEqual(response.status_code, 200)
