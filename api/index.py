import os
import django
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "student_management.settings")

django.setup()

try:
    call_command("migrate", interactive=False, verbosity=0)
except Exception:
    pass

app = get_wsgi_application()