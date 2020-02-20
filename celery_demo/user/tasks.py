from __future__ import absolute_import, unicode_literals
import time

from celery_demo.celery import app


@app.task()
def test_celery():
    time.sleep(10)
    return "Run test_celery ok"
