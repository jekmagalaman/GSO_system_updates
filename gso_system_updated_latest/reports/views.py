from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import WorkAccomplishmentReport

@login_required
def accomplishment_report(request):
    reports = WorkAccomplishmentReport.objects.all().order_by("-date_started")
    return render(
        request,
        "gso_office/accomplishment_report/accomplishment_report.html",
        {"reports": reports}
    )
