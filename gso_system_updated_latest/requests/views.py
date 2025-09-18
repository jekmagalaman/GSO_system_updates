from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from django.db.models import Q
from .models import ServiceRequest

from accounts.models import User
from django.utils import timezone





# --- Role checks ---
def is_gso(user):
    return user.is_authenticated and user.role == "gso"

def is_unit_head(user):
    return user.is_authenticated and user.role == "unit_head"

def is_requestor(user):
    return user.is_authenticated and user.role == "employee"  # adjust if needed







# --- GSO Office Views ---
@login_required
@user_passes_test(is_gso)
@require_POST
def approve_request(request, pk):
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    service_request.status = "Approved"
    service_request.save()
    return redirect("request_management")


@login_required
@user_passes_test(is_gso)
def request_management(request):
    requests_qs = ServiceRequest.objects.select_related("requestor").all().order_by("-created_at")

    # Search filter
    search_query = request.GET.get("user_status")
    if search_query:
        requests_qs = requests_qs.filter(
            Q(requestor__username__icontains=search_query) |
            Q(requestor__first_name__icontains=search_query) |
            Q(requestor__last_name__icontains=search_query)
        )

    # Unit filter
    unit_filter = request.GET.get("unit")
    if unit_filter:
        requests_qs = requests_qs.filter(unit=unit_filter)

    context = {
        "user_role": request.user.role,
        "requests": requests_qs,
    }
    return render(request, "gso_office/request_management/request_management.html", context)













# --- Unit Head Views ---
@login_required
@user_passes_test(is_unit_head)
def unit_head_request_management(request):
    unit = request.user.unit
    requests_qs = ServiceRequest.objects.select_related("requestor").filter(unit=unit).order_by("-created_at")

    # Search filter
    search_query = request.GET.get("user_status")
    if search_query:
        requests_qs = requests_qs.filter(
            Q(requestor__username__icontains=search_query) |
            Q(requestor__first_name__icontains=search_query) |
            Q(requestor__last_name__icontains=search_query)
        )

    # Status filter
    status_filter = request.GET.get("status")
    if status_filter:
        requests_qs = requests_qs.filter(status=status_filter)

    context = {
        "requests": requests_qs,
    }
    return render(request, "unit_heads/unit_head_request_management/unit_head_request_management.html", context)





@login_required
def unit_head_review_task(request, pk):
    req = get_object_or_404(ServiceRequest, pk=pk)

    if request.method == "POST":
        if "approve_done" in request.POST:
            req.status = "Completed"
            req.completed_at = timezone.now()
            req.save()

    return render(
        request,
        "unit_head/unit_head_request_management/request_detail.html",
        {"req": req}
    )











@login_required
def request_detail_assign(request, pk):
    req = get_object_or_404(ServiceRequest, id=pk)

    # Get only personnel under the same unit
    personnel = User.objects.filter(role="personnel", unit=req.unit)

    if request.method == "POST":
        personnel_id = request.POST.get("personnel_id")
        if personnel_id:
            selected_personnel = get_object_or_404(User, id=personnel_id)
            req.assigned_personnel = selected_personnel
            # ❌ Do NOT touch req.status here
            req.save()
        return redirect("unit_head_request_management")

    return render(request, "unit_heads/unit_head_request_management/request_detail.html", {
        "req": req,
        "personnel": personnel
    })







@login_required
@user_passes_test(is_unit_head)
def unit_head_request_history(request):
    return render(request, "unit_heads/unit_head_request_history/unit_head_request_history.html")














# --- Personnel Views ---
@login_required
def personnel_task_management(request):
    # Get tasks assigned to the logged-in personnel
    tasks = ServiceRequest.objects.filter(assigned_personnel=request.user)

    # Optional filters
    search_query = request.GET.get("user_status")
    status_filter = request.GET.get("status")   # <- change from unit to status

    if search_query:
        tasks = tasks.filter(requesting_office__icontains=search_query)

    if status_filter:
        tasks = tasks.filter(status=status_filter)   # <- filter by status now

    return render(
        request,
        "personnel/personnel_task_management/personnel_task_management.html",
        {"tasks": tasks}
    )



@login_required
def personnel_task_detail(request, pk):
    task = get_object_or_404(ServiceRequest, pk=pk, assigned_personnel=request.user)

    if request.method == "POST":
        if "start" in request.POST:
            task.status = "In Progress"
            task.save()
        elif "done" in request.POST:
            task.status = "Done for Review"
            task.save()

    return render(
        request,
        "personnel/personnel_task_management/personnel_task_detail.html",
        {"task": task}
    )












@login_required
def personnel_history(request):
    # Only completed tasks for this personnel
    history = ServiceRequest.objects.filter(
        assigned_personnel=request.user,
        status="Completed"
    ).order_by("-created_at")  # use created_at instead of date_submitted

    return render(
        request,
        "personnel/personnel_history/personnel_history.html",
        {"history": history}
    )












# --- Requestor Views ---
@login_required
@user_passes_test(is_requestor)
def requestor_request_management(request):
    requests_qs = ServiceRequest.objects.filter(requestor=request.user).order_by("-created_at")
    return render(request, "requestor/requestor_request_management/requestor_request_management.html", {"requests": requests_qs})


@login_required
@user_passes_test(is_requestor)
def add_request(request):
    if request.method == "POST":
        ServiceRequest.objects.create(
            requestor=request.user,
            unit=request.POST.get("unit"),
            description=request.POST.get("description"),
            status="Pending",
        )
        return redirect("requestor_request_management")
    return redirect("requestor_request_management")


@login_required
@user_passes_test(is_requestor)
def requestor_request_history(request):
    return render(request, "requestor/requestor_request_history/requestor_request_history.html")
