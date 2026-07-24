from django.db import models
import uuid


class Report(models.Model):

    CATEGORY_CHOICES = [
        ("Road", "Road"),
        ("Garbage", "Garbage"),
        ("Water", "Water"),
        ("Electricity", "Electricity"),
        ("Other", "Other"),
    ]

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Resolved", "Resolved"),
    ]

    tracking_code = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        blank=True,
    )

    title = models.CharField(max_length=200)

    description = models.TextField()

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
    )

    location = models.CharField(max_length=200)

    image = models.ImageField(
        upload_to="reports/",
        blank=True,
        null=True,
    )

    priority = models.CharField(
        max_length=50,
        blank=True,
    )

    severity_score = models.IntegerField(
        default=0,
    )

    confidence = models.IntegerField(
        default=0,
    )

    department = models.CharField(
        max_length=200,
        blank=True,
    )

    summary = models.TextField(
        blank=True,
    )

    reason = models.TextField(
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending",
    )

    is_duplicate = models.BooleanField(
        default=False,
    )

    duplicate_of = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="duplicate_reports",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def save(self, *args, **kwargs):

        if not self.tracking_code:
            self.tracking_code = (
                "TRK-"
                + uuid.uuid4().hex[:8].upper()
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tracking_code} - {self.title}"


class ProgressLog(models.Model):

    report = models.ForeignKey(
        Report,
        on_delete=models.CASCADE,
        related_name="progress_logs",
    )

    message = models.CharField(
        max_length=255,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.report.tracking_code} - {self.message}"