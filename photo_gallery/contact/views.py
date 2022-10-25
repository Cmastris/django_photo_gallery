from django.views.generic import TemplateView


class ContactSuccessView(TemplateView):
    template_name = "contact/contact_success.html"
