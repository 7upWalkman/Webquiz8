"""
Flask configurations for different stages of the project.

See:
    https://flask.palletsprojects.com/en/2.1.x/config/
    https://flask.palletsprojects.com/en/2.1.x/config/#builtin-configuration-values
    https://hackersandslackers.com/configure-flask-applications/

(c) Joao Galamba, 2022
$LICENSE(MIT)
"""

from os import environ
from datetime import timedelta
from logging import INFO, DEBUG as LOG_DEBUG, CRITICAL


class Config:
    """
    Base config. Used just for defaults, which will be extracted from 
    environment variables and available via inheritance.

    See:
    https://flask.palletsprojects.com/en/2.1.x/quickstart/#sessions
    https://flask.palletsprojects.com/en/2.0.x/security/#security-cookie
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie
    """

    ENV = environ.get('ENV')
    TESTING = environ.get('TESTING')
    DEBUG = environ.get('DEBUG')
    LOG_LEVEL = environ.get('LOG_LEVEL')

    SESSION_COOKIE_NAME = 'session'
    SESSION_COOKIE_HTTPONLY = environ.get('SESSION_COOKIE_HTTPONLY') 
    SESSION_COOKIE_SECURE = environ.get('SESSION_COOKIE_SECURE') 
    SESSION_COOKIE_SAMESITE = environ.get('SESSION_COOKIE_SAMESITE')

    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
#:

class Development(Config):
    ENV = 'development'
    TESTING = True
    DEBUG = True
    LOG_LEVEL = LOG_DEBUG

    SECRET_KEY = '8e10d234a1f8eb6f9dd6dfc3a325a0613ad2e620e5b8844cb011470492422bee'
    SESSION_COOKIE_NAME = 'devsession'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(seconds=60)

    DATABASE = 'WebQuiz'
    DATABASE_HOST = '192.168.56.104'
    DATABASE_USER = 'admin'
    DATABASE_PASSWORD = 'abc'
#:

class Production(Config):
    ENV = 'production'
    TESTING = False
    DEBUG = False
    LOG_LEVEL = INFO

    SECRET_KEY = '8e10d234a1f8eb6f9dd6dfc3a325a0613ad2e620e5b8844cb011470492422bee'
    SESSION_COOKIE_NAME = 'prodsession'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(days=5)

    # DATABASE = 'WebQuiz'
    # DATABASE_HOST = '192.168.56'
    # DATABASE_USER = 'admin'
    # DATABASE_PASSWORD = 'abc'
#:
