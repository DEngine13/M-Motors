from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from vehicles.models import Vehicle
from .models import Application, Document

@login_required
def apply_purchase(request, vehicle_pk):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_pk, is_active=True)

    if request.method == "POST":
        Application.objects.create(
            applicant=request.user,
            vehicle=vehicle,
            application_type=Application.PURCHASE,
        )
        application = Application.objects.create(
            applicant=request.user,
            vehicle=vehicle,
            application_type=Application.PURCHASE,
        )
        return redirect("applications:upload_documents", pk=application.pk)
    
    return render(request, "applications/apply_purchase.html", {"vehicle": vehicle})

@login_required
def apply_rental(request, vehicle_pk):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_pk, is_active=True)

    if request.method == "POST":
        duration = request.POST.get("rental_duration")
        Application.objects.create(
            applicant=request.user,
            vehicle=vehicle,
            application_type=Application.RENTAL,
            rental_duration=duration,
        )
        application = Application.objects.create(
            applicant=request.user,
            vehicle=vehicle,
            application_type=Application.RENTAL,
            rental_duration=duration,
        )
        return redirect("applications:upload_documents", pk=application.pk)
    
    return render(request, "applications/apply_rental.html", {
        "vehicle": vehicle,
        "duration_choices": Application.DURATION_CHOICES,
    })

@login_required
def upload_documents(request, pk):
    application = get_object_or_404(Application, pk=pk, applicant=request.user)
    existing_docs = {doc.document_type: doc for doc in application.files.all()}

    if request.method == "POST":
        doc_type = request.POST.get("document_type")
        file = request.FILES.get("file")

        if doc_type and file:
            if doc_type in existing_docs:
                existing_docs[doc_type].file.delete()
                existing_docs[doc_type].delete()

            Document.objects.create(
                application=application,
                document_type=doc_type,
                file=file,
            )
            return redirect("applications:upload_documents", pk=pk)
    
    doc_status = []
    for code, label in Document.TYPE_CHOICES:
        doc_status.append({
            "code": code,
            "label": label,
            "uploaded": code in existing_docs,
        })

    return render(request, "applications/upload_documents.html", {
        "application": application,
        "doc_status": doc_status,
        "docs_uploaded": len(existing_docs),
        "docs_total": len(Document.TYPE_CHOICES),
    })

@login_required
def application_detail(request, pk):
    application = get_object_or_404(Application, pk=pk, applicant=request.user)
    documents = application.files.all()
    return render(request, "applications/application_detail.html", {
        "application": application,
        "documents": documents,
    })