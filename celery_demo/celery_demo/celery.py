from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celery_demo.settings')
app = Celery('celery_demo')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Celery4版本以前需要配置settings.CELERY_IMPORTS来导入目录中的tasks.py, 通过autodiscover_tasks会自动发现这些tasks
app.autodiscover_tasks()
