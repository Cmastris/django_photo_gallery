from .models import NavSection


def navigation(request):
    """Add all NavSection objects to template context data (via settings.py `TEMPLATES`).
    https://docs.djangoproject.com/en/4.0/ref/templates/api/#writing-your-own-context-processors
    https://docs.djangoproject.com/en/4.0/ref/models/querysets/#prefetch-related
    """
    return {
        "nav_sections": NavSection.objects.prefetch_related('navlink_set').all(),
    }
