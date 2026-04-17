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
    list_filter = ("status", "application_type", "created_at")
    search_fields = ("applicant__first_name", "applicant__last_name", "applicant__email", "vehicle__brand", "vehicle__model")
    readonly_fields = ("applicant", "vehicle", "application_type", "rental_duration", "created_at")
    inlines = [DocumentInline]
    actions = ["mark_reviewing", "mark_approved", "mark_rejected"]

    def save_model(self, request, obj, form, change):
        if change:
            old = Application.objects.get(pk=obj.pk)
            status_changed = old.status != obj.status
        else:
            status_changed = False
        super().save_model(request, obj, form, change)
        if status_changed:
            self._notify(obj)
            
    def _notify(self, application):
        send_mail(
            subject=f"M-Motors — Your application #{application.pk} has been updated",
            message=(
                f"Hello{(' ' + application.applicant.first_name) if application.applicant.first_name else ''},\n\n"
                f"Your application #{application.pk} for {application.vehicle} "
                f"has been updated.\n\n"
                f"New status: {application.get_status_display()}\n"
                f"{('Reason: ' + application.rejection_reason) if application.rejection_reason and application.status == 'rejected' else ''}\n\n"
                f"M-Motors"
            ),
            from_email="noreply@m-motors.fr",
            recipient_list=[application.applicant.email],
            fail_silently=True,
        )

    @admin.action(description="Mark as In Review")
    def mark_reviewing(self, request, queryset):
        for app in queryset:
            app.status = Application.REVIEWING
            app.save()
            self._notify(app)
        self.message_user(request, f"{queryset.count()} application(s) marked as In Review.")

    @admin.action(description="Approve selected applications")
    def mark_approved(self, request, queryset):
        for app in queryset:
            app.status = Application.APPROVED
            app.save()
            self._notify(app)
        self.message_user(request, f"{queryset.count()} application(s) approved.")

    @admin.action(description="Reject selected applications")
    def mark_rejected(self, request, queryset):
        for app in queryset:
            app.status = Application.REJECTED
            app.save()
            self._notify(app)
        self.message_user(request, f"{queryset.count()} application(s) rejected.")

