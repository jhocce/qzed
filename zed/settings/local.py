from .base import *



# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR + "/" + 'db.sqlite3',
#     }
# }

DATABASES = {
	'default': {
    	'ENGINE': 'django.db.backends.postgresql_psycopg2',
    	'NAME': 'postgre',
    	'USER': 'postgre',
    	'PASSWORD': 'postgre',
    	'HOST': 'db_postgres',
    	'PORT': '5432',
	}
}