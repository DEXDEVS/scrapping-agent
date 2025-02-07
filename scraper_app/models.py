from django.db import models

class ScrapedData(models.Model):
    source_name = models.CharField(max_length=255, default="Unknown")  # Stores URL or file name
    content = models.TextField()  # Extracted full content
    question = models.TextField(default="N/A")  # Question (for DOCX files)
    answer = models.TextField(default="N/A")  # Answer (for DOCX files)

    def __str__(self):
        return f"{self.source_name}: {self.question[:50]}"
