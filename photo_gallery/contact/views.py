import traceback
from django.core.mail import BadHeaderError, send_mail
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from photo_gallery.settings import ADMINS, DEFAULT_FROM_EMAIL
from .models import ContactMessage


class ContactMessageCreateView(CreateView):
    model = ContactMessage
    fields = ['first_name', 'last_name', 'email_address', 'subject', 'message']
    success_url = reverse_lazy('contact_success')
    template_name = "contact/contact.html"

    def form_valid(self, form):
        try:
            self.send_email(form)
        except Exception as e:
            trace_str = "".join(traceback.format_tb(e.__traceback__)).strip()
            print("Unexpected error in ContactMessageCreateView.send_email():\n\n"
                  "{}".format(trace_str))
        finally:
            return super().form_valid(form)

    def send_email(self, form):
        """Email the site admin with the valid contact submission's contents."""
        first_name = form.cleaned_data.get('first_name').capitalize()
        last_name = form.cleaned_data.get('last_name').capitalize()
        if last_name != "":
            name = first_name + " " + last_name
        else:
            name = first_name

        email_address = form.cleaned_data.get('email_address')
        msg_subject = form.cleaned_data.get('subject')
        recipients = [a[1] for a in ADMINS]
        email_subject = "Contact Message: " + msg_subject
        message = form.cleaned_data.get('message')
        body = "Contact message received from {} ({}).\n\nSubject: {}\nMessage:\n\n{}" \
               "".format(name, email_address, msg_subject, message)

        try:
            send_mail(email_subject, body, DEFAULT_FROM_EMAIL, recipients)
        except BadHeaderError:
            body = "BadHeaderError raised; view the message via the admin site."
            send_mail("Contact Message Received", body, DEFAULT_FROM_EMAIL, recipients)


class ContactSuccessView(TemplateView):
    template_name = "contact/contact_success.html"
