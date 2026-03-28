from django.contrib import admin
from django.core.mail import send_mail
from .models import Application, Document

class DocumentInline(admin.TabularInline):
    model = Document
    extra = 0
    readonly_fields = ("document_type", "file", "uploaded_at")

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "applicant", "vehicle", "application_type", "status", "created_at")
    list_filter = ("status", "application_type")
    inlines = [DocumentInline]

    def save_model(self, request, obj, form, change):
        if change:
            old = Application.objects.get(pk=obj.pk)
            if old.status != obj.status:
                send_mail(
                    subject=f"M-Motors — Your application #{obj.pk} has been updated",
                    message=(
                        f"Hello{(' ' + obj.applicant.first_name) if obj.applicant.first_name else ''},\n\n"
                        f"Your application #{obj.pk} for {obj.vehicle} "
                        f"has been updated.\n\n"
                        f"New status: {obj.get_status_display()}\n"
                        f"{('Reason: ' + obj.rejection_reason) if obj.rejection_reason else ''}\n\n"
                        f"M-Motors"
                    ),
                    from_email="noreply@m-motors.fr",
                    recipient_list=[obj.applicant.email],
                    fail_silently=True,
                )
        super().save_model(request, obj, form, change)
