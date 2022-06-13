"""

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

"""

from ._env import *
from ._dj_db import *
from ._dj_auth import *
from ._asgi import *
from ._wsgi import *
from ._login_pass import *
from ._base import *
from ._drf import *
from ._cors import *
from ._graphql import *
from ._plugin_debug_tool import *
from ._plugin_doc_yasg import *
from ._plugin_grapplli import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-1o#h4jxrjcq1=g=4zy@r=s+e0dgb00ml8fzaji5*xtx0nemqtb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']



# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

import mimetypes

mimetypes.add_type("text/javascript", ".js", True)