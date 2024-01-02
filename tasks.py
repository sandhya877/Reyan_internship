import requests
from celery import Celery

app=Celery()
app.config_from_object("config")

@app.task
def fetch_url(url):
    r=requests.get(url)
    return r.status_code