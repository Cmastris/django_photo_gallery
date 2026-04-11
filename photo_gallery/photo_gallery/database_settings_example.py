from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'
BASE_DIR = Path(__file__).resolve().parent.parent

# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
# This will be imported and used in the main settings file (`DATABASES`)  
# so environment-specific settings can be defined outside of version control
# Consider using `load_dotenv()` to retrieve values from env variables
# The example settings below are suitable for local development
DB_SETTINGS = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
