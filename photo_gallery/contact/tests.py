from django.core import mail
from django.test import tag, TestCase
from django.urls import reverse

from .models import ContactMessage


@tag('contact', 'views')
class TestContactMessageCreateView(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up data for all tests in this class."""
        cls.contact_data = {'first_name': 'john',
                            'last_name': 'smith',
                            'email_address': 'email@example.com',
                            'subject': 'Message Subject',
                            'message': 'This is the message.'}

    def test_200_status(self):
        """Test that a GET request returns a 200 status."""
        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)

    def test_contact_message_object_creation(self):
        """Test that the form submission results in `ContactMessage` object creation."""
        self.client.post(reverse("contact"), self.contact_data)
        messages = ContactMessage.objects.all()
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message, "This is the message.")

    def test_send_email(self):
        """Test that the form submission results in an email being sent via send_email()."""
        self.client.post(reverse("contact"), self.contact_data)
        self.assertEqual(len(mail.outbox), 1)
        expected_body = "Contact message received from John Smith (email@example.com).\n\n" \
                        "Subject: Message Subject\nMessage:\n\nThis is the message."
        self.assertEqual(mail.outbox[0].body, expected_body)


@tag('contact', 'views')
class TestContactSuccessView(TestCase):
    def test_200_status(self):
        """Test that a request returns a 200 status."""
        response = self.client.get(reverse("contact_success"))
        self.assertEqual(response.status_code, 200)
