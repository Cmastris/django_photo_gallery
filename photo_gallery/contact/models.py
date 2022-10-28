from django.core.validators import MinLengthValidator
from django.db import models


class ContactMessage(models.Model):
    first_name = models.CharField(max_length=255, validators=[MinLengthValidator(1)])
    last_name = models.CharField(max_length=255, blank=True)
    email_address = models.EmailField()
    subject = models.CharField(max_length=255, validators=[MinLengthValidator(2)])
    message = models.TextField(max_length=5000, validators=[MinLengthValidator(10)])
    contact_time = models.DateTimeField(auto_now_add=True)
    responded_to = models.BooleanField(default=False)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return self.subject

    class Meta:
        # Recent messages first
        ordering = ['-contact_time']
