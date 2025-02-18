from django.conf import settings
from django.db import models

# Model to store extracted data
class ScrapedData(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    source_name = models.CharField(max_length=255)
    content = models.TextField()
    question = models.TextField(null=True, blank=True)
    answer = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Track extraction time
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.source_name} - {self.user.username if self.user else 'No User'}"
