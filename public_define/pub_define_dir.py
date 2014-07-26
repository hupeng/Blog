#coding: utf-8

"""
this file for define params of program
"""

from pub_define import G_DEBUG

if G_DEBUG:
    PROJECT_PATH = '/home/danny/project/Blog/'

    PROJECT_NAME = 'Blog'

    DATABASES_G = {
                'default': {
                    'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
                    'NAME': 'blog_db',     # Or path to database file if using sqlite3.
                    'USER': 'root',                      # Not used with sqlite3.
                    'PASSWORD': 'hupeng',                  # Not used with sqlite3.
                    'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
                    'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
                }
            }

else:       # 正式发布服务器 
    PROJECT_PATH = ''
    PROJECT_NAME = ''

    DATABASES_G = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': '',     # Or path to database file if using sqlite3.
            'USER': '',                      # Not used with sqlite3.
            'PASSWORD': '',                  # Not used with sqlite3.
            'HOST': '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
        }
    }
