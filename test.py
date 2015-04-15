import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "data_science_project.settings")

from django.db import models
from news.models import Source

source = Source(name="test", url="www.test.com")
source.save()
