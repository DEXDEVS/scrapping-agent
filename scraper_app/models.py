from django.db import models

class ScrapedData(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
