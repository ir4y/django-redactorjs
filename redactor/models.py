import datetime
from django.db import models
from settings import REDACTOR_UPLOAD


class RedaktorJsFile(models.Model):
    owner = models.ForeignKey('auth.User')
    upload = models.FileField(upload_to=REDACTOR_UPLOAD)
    date_created = models.DateTimeField(default=datetime.datetime.now)
    is_image = models.BooleanField(default=True)