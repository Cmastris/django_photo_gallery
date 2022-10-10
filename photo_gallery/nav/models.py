from django.db import models


class NavLink(models.Model):
    link_text_guidelines = "Enter the clickable link text (anchor text)."
    link_text = models.CharField(max_length=50, help_text=link_text_guidelines)

    link_url_guidelines = "Enter the link destination relative URL. E.g. if the full URL is " \
                          "'https://www.example.com/photos/this-photo' then the relative URL is " \
                          "'/photos/this-photo'."

    link_url = models.CharField("link URL", max_length=255, help_text=link_url_guidelines)

    vertical_order_guidelines = "Select the vertical ordering of the link in the dropdown menu " \
                                "(if applicable), where '1st' refers to the top position."
    ORDER_CHOICES = [
        (0, 'N/A'),
        (1, '1st'),
        (2, '2nd'),
        (3, '3rd'),
        (4, '4th'),
        (5, '5th'),
        (6, '6th'),
        (7, '7th'),
        (8, '8th'),
    ]

    vertical_order = models.IntegerField(choices=ORDER_CHOICES, blank=False, default=0,
                                         help_text=vertical_order_guidelines)

    def __str__(self):
        return self.link_text
