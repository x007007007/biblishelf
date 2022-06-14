from ._env import *

INSTALLED_APPS = [
    *([
          # 'grappelli.dashboard',
          'grappelli',
      ] if ENABLE_GRAPPELLI else []),
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'mptt',
    'corsheaders',
    'rest_framework',
    'biblishelf_web.apps.config',
    'biblishelf_web.apps.main',
    'biblishelf_web.apps.book',
]

MIDDLEWARE = [
    'biblishelf_web.middleware.DynDBRouterByURLConfigMiddleWare',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASE_ROUTERS = ['biblishelf_web.dbroute.DynDBSwitchByURLRouter']
