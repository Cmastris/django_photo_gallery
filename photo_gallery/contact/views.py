from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from .models import ContactMessage


class ContactMessageCreateView(CreateView):
    model = ContactMessage
    fields = ['first_name', 'last_name', 'email_address', 'subject', 'message']
    success_url = reverse_lazy('contact_success')
    template_name = "contact/contact.html"


class ContactSuccessView(TemplateView):
    template_name = "contact/contact_success.html"
