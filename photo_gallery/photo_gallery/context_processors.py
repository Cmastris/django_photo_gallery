from django.contrib.sites.models import Site


def global_context(request):
    """Add global variables to template context data (via settings.py `TEMPLATES`).
    https://docs.djangoproject.com/en/5.2/ref/templates/api/#writing-your-own-context-processors
    https://docs.djangoproject.com/en/5.2/ref/contrib/sites/
    """
    # Used to construct absolute URLs, e.g. canonical links in the HTML head
    absolute_root = "https://" + Site.objects.get_current().domain
    return {
        "absolute_root_url": absolute_root,  # E.g. `https://www.example.com`
    }
