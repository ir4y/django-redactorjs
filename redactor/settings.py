# -*- coding: utf8 -*-
from django.conf import settings

__author__ = 'ir4y'

IS_REDACTOR_PUBLIC = getattr(settings, 'IS_REDACTOR_PUBLIC', False)
REDACTOR_UPLOAD = getattr(settings, 'REDACTOR_UPLOAD', "uploads/%Y/%m/%d/")