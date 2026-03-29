from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count
from .models import Template, Certificate


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'status_badge', 'usage_count', 'created_by', 'created_at')
    list_filter = ('is_active', 'category', 'created_at')
    search_fields = ('name', 'category')
    readonly_fields = ('id', 'created_at', 'updated_at', 'preview_image')
    
    fieldsets = (
        ('Template Information', {
            'fields': ('id', 'name', 'category')
        }),
        ('Assets', {
            'fields': ('background_url', 'preview_image')
        }),
        ('Configuration', {
            'fields': ('layout_config',)
        }),
        ('Management', {
            'fields': ('is_active', 'created_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    ordering = ['-created_at']
    date_hierarchy = 'created_at'

    def status_badge(self, obj):
        color = 'green' if obj.is_active else 'red'
        status = 'Active' if obj.is_active else 'Inactive'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            status
        )
    status_badge.short_description = 'Status'

    def usage_count(self, obj):
        count = obj.certificates.count()
        return format_html('<b>{}</b>', count)
    usage_count.short_description = 'Used'

    def preview_image(self, obj):
        if obj.preview_url:
            return format_html('<img src="{}" width="300" />', obj.preview_url)
        return "No preview available"
    preview_image.short_description = 'Preview'


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'event_name', 'verification_code_short', 'status_badge', 'issued_at')
    list_filter = ('status', 'issued_at', 'template', 'event__category')
    search_fields = ('student__first_name', 'student__last_name', 'student__email', 'verification_code', 'event__name')
    readonly_fields = ('id', 'issued_at', 'verification_code_info', 'student_info', 'event_info', 'template_info')
    
    fieldsets = (
        ('Certificate Information', {
            'fields': ('id', 'verification_code_info', 'status')
        }),
        ('Student & Event', {
            'fields': ('student_info', 'event_info')
        }),
        ('Template', {
            'fields': ('template_info',)
        }),
        ('PDF & Delivery', {
            'fields': ('pdf_url', 'generated_by')
        }),
        ('Expiration', {
            'fields': ('expires_at',)
        }),
        ('Timestamps', {
            'fields': ('issued_at',),
            'classes': ('collapse',)
        }),
    )

    ordering = ['-issued_at']
    date_hierarchy = 'issued_at'

    def student_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}"
    student_name.short_description = 'Student'

    def event_name(self, obj):
        return obj.event.name
    event_name.short_description = 'Event'

    def status_badge(self, obj):
        colors = {
            'pending': 'orange',
            'generated': 'blue',
            'sent': 'green',
            'failed': 'red'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def verification_code_short(self, obj):
        return f"{obj.verification_code[:15]}..." if len(obj.verification_code) > 15 else obj.verification_code
    verification_code_short.short_description = 'Verification Code'

    def verification_code_info(self, obj):
        return format_html('<code style="background-color: #f0f0f0; padding: 5px; border-radius: 3px;">{}</code>', obj.verification_code)
    verification_code_info.short_description = 'Verification Code'

    def student_info(self, obj):
        return format_html(
            '<b>{}</b><br/>Document: {}<br/>Email: {}',
            obj.student.full_name,
            obj.student.document_id,
            obj.student.email
        )
    student_info.short_description = 'Student'

    def event_info(self, obj):
        return format_html(
            '<b>{}</b><br/>Date: {}<br/>Category: {}',
            obj.event.name,
            obj.event.event_date.strftime('%d/%m/%Y'),
            obj.event.category.name if obj.event.category else 'N/A'
        )
    event_info.short_description = 'Event'

    def template_info(self, obj):
        if obj.template:
            return format_html('<b>{}</b><br/>Category: {}', obj.template.name, obj.template.category or 'N/A')
        return "No template assigned"
    template_info.short_description = 'Template'
