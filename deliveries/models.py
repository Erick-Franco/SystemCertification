import uuid
from django.db import models
from users.models import User
from certificados.models import Certificate

class DeliveryLog(models.Model):
    METHOD_CHOICES = (
        ('email', 'Email'),
        ('whatsapp', 'WhatsApp'),
        ('link', 'Link'),
    )

    STATUS_CHOICES = (
        ('success', 'Success'),
        ('error', 'Error'),
        ('pending', 'Pending'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    certificate = models.ForeignKey(
        Certificate,
        on_delete=models.CASCADE,
        related_name='deliveries'
    )
    sent_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='delivery_logs')
    delivery_method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    recipient = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-sent_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['delivery_method']),
            models.Index(fields=['certificate']),
        ]

    def __str__(self):
        return f"{self.certificate.student.first_name} - {self.delivery_method} [{self.status}]"