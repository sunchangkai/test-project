import os

from application.settings import BASE_DIR

# ================================================= #
# ************ mysql DataBase config  ************* #
# ================================================= #
# DataBase ENGINE
# sqlite3 config
# DATABASE_ENGINE = "django.db.backends.sqlite3"
# DATABASE_NAME = os.path.join(BASE_DIR, "db.sqlite3")

# mysql config
DATABASE_ENGINE = "django.db.backends.mysql"
DATABASE_NAME = 'prosafeai'

# DATABASE_HOST = "192.168.31.176"
# DATABASE_HOST = "10.39.20.36"
DATABASE_HOST = "39.105.228.75"

DATABASE_PORT = 3306

DATABASE_USER = "sunck"

DATABASE_PASSWORD = "123456"

#
TABLE_PREFIX = "dvadmin_"
# ================================================= #
# **************** redis config******************** #
# ================================================= #
REDIS_PASSWORD = ''
REDIS_HOST = '39.105.228.75'
# REDIS_HOST = '10.39.20.158'
REDIS_URL = f'redis://:{REDIS_PASSWORD or ""}@{REDIS_HOST}:6379'
# ================================================= #
# ****************** start/stop ******************* #
# ================================================= #
DEBUG = True
# Start the login detailed overview (obtain the IP detailed address by calling the API.
# If it is an internal network, close it)
ENABLE_LOGIN_ANALYSIS_LOG = True
#
LOGIN_NO_CAPTCHA_AUTH = True
# ================================================= #
# ***************** other config ****************** #
# ================================================= #

ALLOWED_HOSTS = ["*"]
# daphne start command
# daphne application.asgi:application -b 0.0.0.0 -p 8000
