from django.contrib import admin
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "applicant", "vehicle", "application_type", "status", "created_at")
    list_filter = ("status", "application_type")
