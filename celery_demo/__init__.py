from __future__ import absolute_import, unicode_literals

# 这样可以确保在Django启动时加载应用
from celery_demo.celery import app as celery_app

__all__ = ('celery_app',)
