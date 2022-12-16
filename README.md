# Django Photo Gallery <!-- omit in toc -->

A photo gallery website built using Django 4 and Bootstrap 5. Take a look: https://cmastris.eu.pythonanywhere.com/.

## Contents <!-- omit in toc -->
- [Core features](#core-features)
  - [Photo detail pages](#photo-detail-pages)
  - [Photo listing pages](#photo-listing-pages)
  - [Editable navigation menu](#editable-navigation-menu)
  - [Contact functionality](#contact-functionality)
  - [Customised Django admin site](#customised-django-admin-site)
  - [SEO best practices](#seo-best-practices)
  - [Comprehensively tested](#comprehensively-tested)
- [Setup and deployment](#setup-and-deployment)
- [FAQs](#faqs)
  - [Can I see an example?](#can-i-see-an-example)
  - [How can I ask questions, report bugs, or provide feedback?](#how-can-i-ask-questions-report-bugs-or-provide-feedback)
  - [Is this project in active development?](#is-this-project-in-active-development)

## Core features

### Photo detail pages
Photo detail pages are dynamically populated based on Photo model objects, which are fully editable via the [Django admin site](#customised-django-admin-site). This includes:

- The photo image (resized to desktop and mobile versions during upload, for faster loading)
- Title, location, date, and description content
- A list of Collections that contain the Photo (if applicable)

*Check out the code: [Photo and Collection models](photo_gallery/photos/models.py); [PhotoDetailView](photo_gallery/photos/views.py); [photo detail template](photo_gallery/photos/templates/photos/photo_detail.html); [URL config](photo_gallery/photo_gallery/urls.py).*

### Photo listing pages
Photo listing pages are dynamically populated based on Photo and Collection model objects, which are fully editable via the [Django admin site](#customised-django-admin-site). More specifically, these include:

- The homepage: all published Photos
- Collections: all published Photos in the Collection (with Collection description content)
- Search results: all published Photos whose title, location, or description contains the search query

Listing pages are sorted by featured status and then by newest to oldest by default, while the homepage and collections can also be sorted by newest to oldest or vice versa. All listing pages feature dynamic paginated URLs and links.

*Check out the code: [Photo and Collection models](photo_gallery/photos/models.py); [photo views](photo_gallery/photos/views.py); [list template](photo_gallery/photos/templates/photos/photo_list.html); [collection template](photo_gallery/photos/templates/photos/collection.html); [search template](photo_gallery/photos/templates/photos/search.html); [URL config](photo_gallery/photo_gallery/urls.py).*

### Editable navigation menu
Rather than being hardcoded, the primary site navigation menu is generated based on model objects that are editable via the [Django admin site](#customised-django-admin-site). This includes:

- The type, number, and order of navigation sections (top-level links or dropdowns)
- The number and order of links within a dropdown
- The text and URLs of sections and links

*Check out the code: [NavLink and NavSection models](photo_gallery/nav/models.py); [navigation context processor](photo_gallery/nav/context_processors.py); [base template](photo_gallery/templates/base.html).*

### Contact functionality
Contact functionality is implemented using a [model](photo_gallery/contact/models.py) so that all contact messages are viewable via the [Django admin site](#customised-django-admin-site) and can then be marked as responded to and/or resolved. Optional email alert functionality is also implemented (refer to [setup and deployment](#setup-and-deployment) for configuration details).

*Check out the code: [ContactMessage model](photo_gallery/contact/models.py); [contact views](photo_gallery/contact/views.py); [contact template](photo_gallery/contact/templates/contact/contact.html); [contact success template](photo_gallery/contact/templates/contact/contact_success.html); [URL config](photo_gallery/photo_gallery/urls.py).*

### Customised Django admin site
Model objects can be created, edited, and deleted via the admin site, Django's simple content management system (CMS). Beyond the out-of-the-box implementation, model object listing and detail pages have been customised to provide useful data and functionality. For example:

- Photo listing and change pages include a photo thumbnail image
- Photo and Collection add pages auto-populate the URL slug field
- Collection and Country pages include associated Photo counts
- Photos and ContactMessages can be searched and filtered
- Help text is used to describe some (less obvious) model fields

*Check out the code: [Photo, Collection, and Country admin config](photo_gallery/photos/admin.py); [NavLink and NavSection admin config](photo_gallery/nav/admin.py); [ContactMessage admin config](photo_gallery/contact/admin.py); [Photo, Collection, and Country models](photo_gallery/photos/models.py); [NavLink and NavSection models](photo_gallery/nav/models.py); [ContactMessage model](photo_gallery/contact/models.py).*

### SEO best practices
Fundamental search engine optimisation (SEO) best practices are met, including:
- Dynamically generated page titles, meta descriptions, and Open Graph content (based on Photo and Collection model data)
- Appropriately canonicalised URLs (including sorted and paginated listing pages)
- A dynamically generated XML sitemap
- A robots.txt file that prevents the crawling of search results pages

Note: this website is designed to be a personal portfolio that minimises the effort required to add/edit content. As such, some SEO-related content/tags (e.g. page titles) can't be edited specifically; however, model fields could be added and/or templates changed to support additional customisation.

*Check out the code: template (HTML) files; [XML sitemap config](photo_gallery/photo_gallery/sitemap_config.py); [robots.txt](photo_gallery/templates/robots.txt).*

### Comprehensively tested
Important functionality that extends or modifies Django's code is validated via over 40 unit tests. Wider functionality and cross-device rendering has also been manually tested thoroughly.

*Check out the code: [photo tests](photo_gallery/photos/tests.py); [navigation menu tests](photo_gallery/nav/tests.py); [contact message tests](photo_gallery/contact/tests.py).*

## Setup and deployment
If you're unfamiliar with Django, the [official tutorial](https://docs.djangoproject.com/en/4.0/intro/tutorial01/) explains how to set up a new project.

As an overview, you'll need to clone a local copy of this repository, install the [requirements](requirements.txt), and run the database migrations using `python manage.py migrate` from within the outer `photo_gallery` directory that contains `manage.py`. From there, you can run the application locally using `python manage.py runserver` from within the same directory.

When you're ready to deploy a production (i.e. public) version of the website, be sure to read Django's [deployment documentation](https://docs.djangoproject.com/en/4.0/howto/deployment/) (including the [deployment checklist](https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/)) to avoid security vulnerabilities and other issues.

For this project, the following deployment steps will also be necessary:

- Use [prod_urls.py](photo_gallery/photo_gallery/prod_urls.py) (which removes [development-only media file serving](https://docs.djangoproject.com/en/4.0/howto/static-files/#serving-files-uploaded-by-a-user-during-development)) rather than [urls.py](photo_gallery/photo_gallery/urls.py)
- Configure and use [prod_settings.py](photo_gallery/photo_gallery/prod_settings.py) (which ensures that project settings are safe and appropriate for production), referring to the settings documentation where needed, rather than [settings.py](photo_gallery/photo_gallery/settings.py)
- Run a site name data migration (which is used to construct absolute URLs, e.g. in the XML sitemap and HTML tags) using the template and instructions in [site_name_migration_template.py](photo_gallery/photo_gallery/site_name_migration_template.py)
- Change the [robots.txt](photo_gallery/templates/robots.txt) sitemap link to the correct URL (for simplicity, this doesn't use the site data in the previous step)
- Configure contact message email alerts (implemented in [contact/views.py](photo_gallery/contact/views.py)) via the email settings in [prod_settings.py](photo_gallery/photo_gallery/prod_settings.py), if desired (otherwise, just check messages regularly via the Django admin site)
- Change the [favicon](photo_gallery/global_static/favicon.ico) if desired

## FAQs

### Can I see an example?
Yes! A production version of the website which is populated with content (my own photos) can be found here: https://cmastris.eu.pythonanywhere.com/.

### How can I ask questions, report bugs, or provide feedback?
Feel free to create an issue or open a new discussion.

### Is this project in active development?
There are no further updates/features planned and I'm not looking for contributions, but I'll be happy to fix any (significant) bugs.
