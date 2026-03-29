import uuid
from django.db import models
from django.utils import timezone
from users.models import User
from students.models import Student
from events.models import Event


class Template(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="templates"
    )

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, blank=True)

    background_url = models.TextField()
    preview_url = models.TextField(blank=True)

    layout_config = models.JSONField()

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return f"{self.name} ({self.category})" if self.category else self.name


class Certificate(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('generated', 'Generated'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="certificates"
    )

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="certificates"
    )

    template = models.ForeignKey(
        Template,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="certificates"
    )

    generated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="generated_certificates"
    )

    verification_code = models.CharField(max_length=50, unique=True)

    pdf_url = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    expires_at = models.DateTimeField(null=True, blank=True)

    issued_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'event')
        ordering = ['-issued_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['verification_code']),
            models.Index(fields=['student', 'event']),
        ]

    def __str__(self):
        return f"{self.student} - {self.event.name} [{self.status}]"

    def is_expired(self):
        """Check if certificate has expired"""
        if not self.expires_at:
            return False
        return timezone.now() > self.expires_at