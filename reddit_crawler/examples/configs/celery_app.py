from __future__ import absolute_import
from os import environ

from celery import Celery

celery_app = Celery('celery_app',
                broker='redis://localhost:6379/0',
                backend='redis://localhost:6379/0',
                include=['reddit_crawler.examples.spider.tasks'])

celery_app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=120,
    CELERYD_CONCURRENCY=1,
)
