import os

#get the current directory
current_dir = os.getcwd()

STATIC_ROOT = ''
STATIC_URL = '/static/'
MEDIA_ROOT = '{0}/gisweb_app/static/'.format(current_dir)
MEDIA_URL = 'uploaded_files/'
