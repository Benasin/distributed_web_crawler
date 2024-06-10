from celery import Celery

app = Celery('crawler', 
             broker='redis://:redis_password@redis:6379/0', 
             backend='redis://:redis_password@redis:6379/0')

app.conf.update(
    result_expires=3600,
)

app.autodiscover_tasks()
