from django.contrib import admin
from django.utils.html import format_html
from .models import DeliveryLog


@admin.register(DeliveryLog)
class DeliveryLogAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'certificate_event', 'method_badge', 'status_badge', 'sent_at', 'sent_by')
    list_filter = ('status', 'delivery_method', 'sent_at')
    search_fields = ('certificate__student__first_name', 'certificate__student__last_name', 
                     'recipient', 'certificate__event__name')
    readonly_fields = ('id', 'sent_at', 'certificate_info', 'delivery_info')
    
    fieldsets = (
        ('Delivery Information', {
            'fields': ('id', 'certificate_info', 'delivery_info')
        }),
        ('Recipient', {
            'fields': ('recipient',)
        }),
        ('Status & Error', {
            'fields': ('status', 'error_message')
        }),
        ('Management', {
            'fields': ('sent_by', 'sent_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    ordering = ['-sent_at']
    date_hierarchy = 'sent_at'

    def student_name(self, obj):
        return f"{obj.certificate.student.first_name} {obj.certificate.student.last_name}"
    student_name.short_description = 'Student'

    def certificate_event(self, obj):
        return obj.certificate.event.name
    certificate_event.short_description = 'Event'

    def method_badge(self, obj):
        colors = {
            'email': 'blue',
            'whatsapp': 'green',
            'link': 'purple'
        }
        color = colors.get(obj.delivery_method, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_delivery_method_display()
        )
    method_badge.short_description = 'Method'

    def status_badge(self, obj):
        colors = {
            'success': 'green',
            'error': 'red',
            'pending': 'orange'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def certificate_info(self, obj):
        return format_html(
            '<b>{}</b><br/>Code: {}<br/>Event: {}',
            obj.certificate.student.full_name,
            obj.certificate.verification_code[:20] + '...',
            obj.certificate.event.name
        )
    certificate_info.short_description = 'Certificate'

    def delivery_info(self, obj):
        return format_html(
            '<b>Method:</b> {}<br/><b>Recipient:</b> {}<br/><b>Status:</b> {}',
            obj.get_delivery_method_display(),
            obj.recipient,
            obj.get_status_display()
        )
    delivery_info.short_description = 'Delivery Details'
