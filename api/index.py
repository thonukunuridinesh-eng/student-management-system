import os
from student_management.wsgi import application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "student_management.settings")

app = application