# prod.py 예시

from .base import *

DEBUG = False

ALLOWED_HOSTS = ['3.39.237.55', 'ec2-3-39-237-55.ap-northeast-2.compute.amazonaws.com']

INSTALLED_APPS += [
    'storages',
]

# Static
STATIC_URL = 'static/'
STATIC_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / '.static_root'

# Media
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# DB
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': SECRET['DB']['NAME'],               # 데이터베이스 이름
        'USER': SECRET['DB']['USER'],               # 사용자 이름
        'PASSWORD': SECRET['DB']['PASSWORD'],       # 비밀번호
        'HOST': SECRET['DB']['HOST'],               # 데이터베이스 서버 주소
        'PORT': SECRET['DB']['PORT'],               # MySQL의 기본 포트
    }
}

# S3 Storage
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": SECRET["S3"]["ACCESS"],
            "secret_key": SECRET["S3"]["SECRET"],
            "bucket_name": SECRET["S3"]["NAME"],
            "region_name": SECRET["S3"]["REGION"],
            "location": "media",
            "default_acl": "public-read",
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": SECRET["S3"]["ACCESS"],
            "secret_key": SECRET["S3"]["SECRET"],
            "bucket_name": SECRET["S3"]["NAME"],
            "region_name": SECRET["S3"]["REGION"],
            "custom_domain": f'{SECRET["S3"]["NAME"]}.s3.amazonaws.com',
            "location": "static",
            "default_acl": "public-read",
        },
    },
}

# Static, Media URL
STATIC_URL = f'https://{SECRET["S3"]["NAME"]}.s3.amazonaws.com/static/'
MEDIA_URL = f'https://{SECRET["S3"]["NAME"]}.s3.amazonaws.com/media/'

ROOT_URLCONF = 'config.urls'





