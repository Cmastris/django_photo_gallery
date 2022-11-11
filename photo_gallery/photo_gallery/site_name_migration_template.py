from django.db import migrations

# https://docs.djangoproject.com/en/4.0/ref/contrib/sites/#enabling-the-sites-framework
# https://docs.djangoproject.com/en/4.0/topics/migrations/#data-migrations
# The sites framework is used to define absolute URLs, e.g. in the XML sitemap and HTML tags
# Edit the functions below to add the site domain, name, and ID if not `1`
# Create an empty migration file using `python manage.py makemigrations --empty sites`
# Edit the migration file to add the functions and operations in this template
# Run `python manage.py migrate` and reload the application to apply the changes
# Check the /sitemap.xml file to check the domain is correct; if not, create a new migration


def define_site_details(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    site = Site.objects.get(id=1)  # TODO (`SITE_ID` in settings.py)
    site.domain = "www.yourdomain.com"  # TODO
    site.name = "Photo Gallery"  # TODO
    site.save()


def reset_site_details(apps, schema_editor):
    # Applied when migrating backwards i.e. reversing the migration
    Site = apps.get_model('sites', 'Site')
    site = Site.objects.get(id=1)  # TODO (`SITE_ID` in settings.py)
    site.domain = "example.com"
    site.name = "example.com"
    site.save()


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.RunPython(define_site_details,
                             reverse_code=reset_site_details),
    ]
