import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'catch-me-if-you-can'

    #SQL_DATABASE_URI = os.environ.get('DATABASE_URL')  or 'sqlite:///'+os.path.join(basedir,'app.db')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    POSTS_PER_PAGE = 3

    LANGUAGES = ['en','ar']