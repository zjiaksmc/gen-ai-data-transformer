"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
import environ
from urllib.parse import urlparse

from pathlib import Path
from django.conf.global_settings import ADMINS

GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "docai-warehouse-demo")
# GCP_PROJECT_NUMBER=os.environ.get("GCP_PROJECT_NUMBER", "362647007280")
GCP_LOCATION = os.environ.get("GCP_LOCATION", "us-central1")
DEFAULT_SAMPLE_URL = "/Users/zjia/Workspace/gen-ai-data-transformer/examples/data/pii_test.csv"
# GCP_BQ_HOST=os.environ.get("GCP_BQ_HOST", GCP_PROJECT_ID)
# GCP_BQ_DB=os.environ.get("GCP_BQ_DB", "utah_lakehouse_demo")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j&64k#^26-z#z9(ash42xbfbmif_9j7w@0q!kj6zi)7_in(8k#'

# SECURITY WARNING: don't run with debug turned on in production!
env = environ.Env(DEBUG=(bool, False))
env_file = os.path.join(BASE_DIR, ".env")

DEBUG = env("DEBUG")

APPENGINE_URL = env("APPENGINE_URL", default=None)
if APPENGINE_URL:
    # Ensure a scheme is present in the URL before it's processed.
    if not urlparse(APPENGINE_URL).scheme:
        APPENGINE_URL = f"https://{APPENGINE_URL}"

    ALLOWED_HOSTS = [urlparse(APPENGINE_URL).netloc]
    CSRF_TRUSTED_ORIGINS = [APPENGINE_URL]
    SECURE_SSL_REDIRECT = True
else:
    ALLOWED_HOSTS = ["*"]

# HOST and ADMINS
MANAGERS = ADMINS

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    ## Third Party #####
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'django_filters',
    'rest_framework_swagger',
    'drf_yasg',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth',
    ## Self-defined ########
    'autoclean',
    'copilot',
    'user'
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]
ROOT_URLCONF = 'config.urls'
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
WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'api',
        'USER': 'aidf_admin',
        'PASSWORD': '&C-m>1D.HEndp8X:',
        'HOST': '34.172.23.247',
        'PORT': '5432',
    },
    'gen_ai': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'history_service',
        'USER': 'aidf_admin',
        'PASSWORD': '&C-m>1D.HEndp8X:',
        'HOST': '34.172.23.247',
        'PORT': '5432',
    }
}

# Cache
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://:fKPWbbOrbgvQI46TRiY04UjcFLH33GVTcAzCaMzMmYs=@aidf-cache.redis.cache.windows.net:6379",
        "OPTIONS": {
            "db": "1"
        },
    },
    "gen_ai": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://:fKPWbbOrbgvQI46TRiY04UjcFLH33GVTcAzCaMzMmYs=@aidf-cache.redis.cache.windows.net:6379",
        "OPTIONS": {
            "db": "0"
        },
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Cross Origin WhiteList
CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^.*$'
CORS_PREFLIGHT_MAX_AGE = 300000

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = "static"
STATIC_URL = "/static/"
STATICFILES_DIRS = []

# Framework settings
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
        # 'rest_framework_simplejwt.authentication.JWTAuthentication'
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication'
    ]
}
REST_AUTH = {
    'USE_JWT': True,
    'TOKEN_MODEL': None,
    'SESSION_LOGIN': True,
    'JWT_AUTH_COOKIE': 'auth',
    'JWT_AUTH_HTTPONLY': True,
    'USER_DETAILS_SERIALIZER': 'user.serializers.UserDetailsSerializer'
}
from datetime import timedelta
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
PAGE_SIZE = 20

# Airflow (Cloud composer)
# AIRFLOW = {
#     "HOST": AIRFLOW_HOST.format(os.getenv('MODE', 'uat-')),
#     "USERNAME": AIRFLOW_USERNAME,
#     "PASSWORD": AIRFLOW_PASSWORD,
#     "MODE": os.getenv('MODE', 'uat-')
# }

# ML/AI Settings
GITHUB_SECRET = env("GITHUB_SECRET", default="")
os.environ["GITHUB_SECRET"] = GITHUB_SECRET
COPILOT = {
    "model_id": "codechat-bison@001",
    "tag": "copilot-cleansing",
    "prompt": {
        "context": "You are a data engineer. You help data scientist to clean and standardize raw data.",
        # "context": "",
        # "input_template": "{}. Run the code on the provided sample data and display output."
        "input_template": "{}",
        "web_search_template": "Web search results:\n\n[search_results]\nCurrent date: [current_date]\n\nInstructions: Using the provided web search results, write a comprehensive reply to the given query. Make sure to cite results using [[number](URL)] notation after the reference. If the provided search results refer to multiple subjects with the same name, write separate answers for each subject.\nQuery: [query]",
        "proprietary_search_template": "Resultant LLC's proprietary knowledge:\n\n[search_results]\nInstructions: Using the provided proprietary knowledge from Resultant LLC, write a comprehensive reply to the given query. Make sure to cite results using [[number](URL)] notation after the reference. If the provided search results refer to multiple subjects with the same name, write separate answers for each subject.\nQuery: [query]",
    },
    "parameters": {
        "max_output_tokens": 2048,
        "temperature": 0.2
    }
}
AUTOCLEAN = [
    {
        "model_id": "text-bison@001",
        "tag": "cleansing-ssn",
        "prompt": {
            "context": "you modify or reformat the input according to request. the output must contains same or less characters than the input.",
            "examples": [
                {
                    "input": "reformat input 233-09-1931 into a social security number. Output should only has 9 digits numbers.",
                    "output": "233091931"
                },
                {
                    "input": "reformat input 013031233 into a social security number. Output should only has 9 digits numbers.",
                    "output": "013031233"
                },
                {
                    "input": "reformat input A233919 into social security number. Output should only has 9 digits numbers.",
                    "output": "INVALID"
                }
            ],
            "input_template": "reformat input {} into social security number. Output should only has 9 digits numbers."
        },
        "parameters": {
            "max_output_tokens": 512,
            "temperature": 1,
            "top_p": 1,
            "top_k": 40
        }
    },
    {
        "model_id": "text-bison@001",
        "tag": "cleansing-person-name",
        "prompt": {
            "context": "you modify or reformat the input according to request. the output must contains same or less characters than the input.",
            "examples": [
                {
                    "input": "reformat input Jack into a person name. Output should only contain letters in uppercase.",
                    "output": "JACK"
                },
                {
                    "input": "reformat input JOHN into a person name. Output should only contain letters in uppercase.",
                    "output": "JOHN"
                },
                {
                    "input": "reformat input zhou into a person name. Output should only contain letters in uppercase.",
                    "output": "ZHOU"
                },
                {
                    "input": "reformat input wILLSON into a person name. Output should only contain letters in uppercase.",
                    "output": "WILLSON"
                },
                {
                    "input": "reformat input Wade2339 into a person name. Output should only contain letters in uppercase.",
                    "output": "INVALID"
                }
            ],
            "input_template": "reformat input {} into a person name. Output should only contain letters in uppercase."
        },
        "parameters": {
            "max_output_tokens": 512,
            "temperature": 1,
            "top_p": 1,
            "top_k": 40
        }
    },
    {
        "model_id": "text-bison@001",
        "tag": "cleansing-date",
        "prompt": {
            "context": "you modify or reformat the input according to request. the output must contains same or less characters than the input.",
            "examples": [
                {
                    "input": "reformat input '09/02/1980' into a date in the format yyyymmdd. Output should only contain numbers and be exactly 8 digits.",
                    "output": "19800902"
                },
                {
                    "input": "reformat input '1992-09-13' into a date in the format yyyymmdd. Output should only contain numbers and be exactly 8 digits.",
                    "output": "19920913"
                },
                {
                    "input": "reformat input '99-05-23' into a date in the format yyyymmdd. Output should only contain numbers and be exactly 8 digits.",
                    "output": "19990523"
                },
                {
                    "input": "reformat input '99-34-67' into a date in the format yyyymmdd. Output should only contain numbers and be exactly 8 digits.",
                    "output": "INVALID"
                },
                {
                    "input": "reformat input '20200718' into a date in the format yyyymmdd. Output should only contain numbers and be exactly 8 digits.",
                    "output": "20200718"
                },
                {
                    "input": "reformat input 'Sep 5, 2022' into a date in the format yyyymmdd. Output should only contain numbers and be exactly 8 digits.",
                    "output": "20220905"
                },
                {
                    "input": "reformat input 'March 17th, 1997' into a date in the format yyyymmdd. Output should only contain numbers and be exactly 8 digits.",
                    "output": "19970317"
                },
                {
                    "input": "reformat input 'Sep 98, 2022' into a date in the format yyyymmdd. Output should only contain numbers and be exactly 8 digits.",
                    "output": "INVALID"
                }
            ],
            "input_template": "reformat input '{}' into a date in the format yyyymmdd. Output should only contain numbers and be exactly 8 digits."
        },
        "parameters": {
            "max_output_tokens": 512,
            "temperature": 1,
            "top_p": 1,
            "top_k": 40
        }
    },
    {
        "model_id": "text-bison@001",
        "tag": "cleansing-gender",
        "prompt": {
            "context": "you modify or reformat the input according to request. the output must contains one of the values from 'MALE', 'FEMALE', 'OTHER'.",
            "examples": [
                {
                    "input": "reformat input 'm' into a human gender. Output should only be one 'MALE', 'FEMALE', or 'OTHER'. If cannot convert, return INVALID.",
                    "output": "MALE"
                },
                {
                    "input": "reformat input 'f' into a human gender. Output should only be one 'MALE', 'FEMALE', or 'OTHER'. If cannot convert, return INVALID.",
                    "output": "FEMALE"
                },
                {
                    "input": "reformat input 'Male' into a human gender. Output should only be one 'MALE', 'FEMALE', or 'OTHER'. If cannot convert, return INVALID.",
                    "output": "MALE"
                },
                {
                    "input": "reformat input 'transgender' into a human gender. Output should only be one 'MALE', 'FEMALE', or 'OTHER'. If cannot convert, return INVALID.",
                    "output": "OTHER"
                }
            ],
            "input_template": "reformat input '{}' into a human gender. Output should only be one 'MALE', 'FEMALE', or 'OTHER'. If cannot convert, return INVALID."
        },
        "parameters": {
            "max_output_tokens": 512,
            "temperature": 1,
            "top_p": 1,
            "top_k": 40
        }
    },
    {
        "model_id": "text-bison@001",
        "tag": "cleansing-race",
        "prompt": {
            "context": "you modify or reformat the input according to request. the output must be from one of these values: 'WHITE', 'AA', 'AIAN', 'ASIAN', 'NHOPI', 'OTHER'.",
            "examples": [
                {
                    "input": "reformat input 'asian' into a census race. the output must be from one of these values: 'WHITE', 'AA', 'AIAN', 'ASIAN', 'NHOPI', 'OTHER'. If cannot convert, return INVALID.",
                    "output": "ASIAN"
                },
                {
                    "input": "reformat input 'caucasian' into a census race. the output must be from one of these values: 'WHITE', 'AA', 'AIAN', 'ASIAN', 'NHOPI', 'OTHER'. If cannot convert, return INVALID.",
                    "output": "WHITE"
                },
                {
                    "input": "reformat input 'african american' into a census race. the output must be from one of these values: 'WHITE', 'AA', 'AIAN', 'ASIAN', 'NHOPI', 'OTHER'. If cannot convert, return INVALID.",
                    "output": "AA"
                },
                {
                    "input": "reformat input 'WADASDSA' into a census race. the output must be from one of these values: 'WHITE', 'AA', 'AIAN', 'ASIAN', 'NHOPI', 'OTHER'. If cannot convert, return INVALID.",
                    "output": "INVALID"
                },
                {
                    "input": "reformat input 'american indian' into a census race. the output must be from one of these values: 'WHITE', 'AA', 'AIAN', 'ASIAN', 'NHOPI', 'OTHER'. If cannot convert, return INVALID.",
                    "output": "AIAN"
                },
                {
                    "input": "reformat input 'native alaska' into a census race. the output must be from one of these values: 'WHITE', 'AA', 'AIAN', 'ASIAN', 'NHOPI', 'OTHER'. If cannot convert, return INVALID.",
                    "output": "AIAN"
                },
                {
                    "input": "reformat input 'pacific islander' into a census race. the output must be from one of these values: 'WHITE', 'AA', 'AIAN', 'ASIAN', 'NHOPI', 'OTHER'. If cannot convert, return INVALID.",
                    "output": "NHOPI"
                },
                {
                    "input": "reformat input 'native hawaiian' into a census race. the output must be from one of these values: 'WHITE', 'AA', 'AIAN', 'ASIAN', 'NHOPI', 'OTHER'. If cannot convert, return INVALID.",
                    "output": "NHOPI"
                }
            ],
            "input_template": "reformat input '{}' into a census race. the output must be from one of these values: 'WHITE', 'AA', 'AIAN', 'ASIAN', 'NHOPI', 'OTHER'. If cannot convert, return INVALID."
        },
        "parameters": {
            "max_output_tokens": 512,
            "temperature": 1,
            "top_p": 1,
            "top_k": 40
        }
    },
    {
        "model_id": "text-bison@001",
        "tag": "cleansing-zip",
        "prompt": {
            "context": "you modify or reformat the input according to request. the output must be a valid US zipcode with 5 digits numbers.",
            "examples": [
                {
                    "input": "reformat input '67092' into a zip code. the output must be a valid US zip code with 5 digits numbers. If cannot convert, return INVALID.",
                    "output": "67092"
                },
                {
                    "input": "reformat input '1343s' into a zip code. the output must be a valid US zip code with 5 digits numbers. If cannot convert, return INVALID.",
                    "output": "INVALID"
                },
                {
                    "input": "reformat input '231' into a zip code. the output must be a valid US zip code with 5 digits numbers. If cannot convert, return INVALID.",
                    "output": "INVALID"
                },
                {
                    "input": "reformat input 'sdsad' into a zip code. the output must be a valid US zip code with 5 digits numbers. If cannot convert, return INVALID.",
                    "output": "INVALID"
                },
                {
                    "input": "reformat input '2394845543' into a zip code. the output must be a valid US zip code with 5 digits numbers. If cannot convert, return INVALID.",
                    "output": "INVALID"
                },
                {
                    "input": "reformat input '46256-2031' into a zip code. the output must be a valid US zip code with 5 digits numbers. If cannot convert, return INVALID.",
                    "output": "46256"
                }
            ],
            "input_template": "reformat input '{}' into a zip code. the output must be a valid US zip code with 5 digits numbers. If cannot convert, return INVALID."
        },
        "parameters": {
            "max_output_tokens": 512,
            "temperature": 1,
            "top_p": 1,
            "top_k": 40
        }
    }
]