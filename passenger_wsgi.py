import os
import sys

# Add your project directory to the sys.path
sys.path.append(os.getcwd())

# Set environment variable for Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'pnac_project.settings'

# Import the application from your project's wsgi file
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

