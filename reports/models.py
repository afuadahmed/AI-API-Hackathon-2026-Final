from django.db import models


class Report(models.Model):
    CATEGORY_CHOICES = [
        ("Road", "Road"),
        ("Garbage", "Garbage"),
        ("Water", "Water"),
        ("Electricity", "Electricity"),
        ("Other", "Other"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to="reports/", blank=True, null=True)

    priority = models.CharField(max_length=50, blank=True)
    department = models.CharField(max_length=200, blank=True)
    summary = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title