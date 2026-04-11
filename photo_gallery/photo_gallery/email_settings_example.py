# https://docs.djangoproject.com/en/5.2/topics/email/
# These settings will be imported and used in the main settings file  
# so environment-specific settings can be defined outside of version control
# The example settings below are suitable for local development

# https://docs.djangoproject.com/en/5.2/topics/email/#email-backends
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# https://docs.djangoproject.com/en/5.2/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = 'from_email@example.com'

# https://docs.djangoproject.com/en/5.2/ref/settings/#std-setting-SERVER_EMAIL
SERVER_EMAIL = 'from_email@example.com'

# https://docs.djangoproject.com/en/5.2/ref/settings/#admins
ADMINS = [('Admin1', 'email1@example.com'), ('Admin2', 'email2@example.com')]
