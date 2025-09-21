from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from django.db.models import Q
from .models import ServiceRequest, InventoryItem, RequestMaterial, TaskReport


from django.contrib import messages


from accounts.models import User
from django.utils import timezone





# --- Role checks ---
def is_gso(user):
    return user.is_authenticated and user.role == "gso"

def is_unit_head(user):
    return user.is_authenticated and user.role == "unit_head"

def is_requestor(user):
    return user.is_authenticated and user.role == "requestor"  # adjust if needed







# --- GSO Office Views ---
@login_required
@user_passes_test(is_gso)
@require_POST
def approve_request(request, pk):
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    service_request.status = "Approved"
    service_request.save()
    messages.success(request, f"Request {pk} has been approved.")
    return redirect("request_management")










@login_required
@user_passes_test(is_gso)
def request_management(request):
    requests_qs = (
        ServiceRequest.objects
        .select_related("requestor")
        .prefetch_related("assigned_personnel", "reports__personnel")  # ✅ include reports + personnel
        .all()
        .order_by("-created_at")
    )

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
@user_passes_test(is_unit_head)
def unit_head_request_detail(request, pk):
    req = get_object_or_404(ServiceRequest, id=pk)
    personnel = User.objects.filter(role="personnel", unit=req.unit)
    materials = InventoryItem.objects.filter(is_active=True)

    # ✅ Fetch reports linked to this request
    reports = req.reports.select_related("personnel").order_by("-created_at")

    if request.method == "POST":
        # ✅ Assign personnel
        if "personnel_ids" in request.POST and req.status not in ["Done for Review", "Completed"]:
            selected_ids = request.POST.getlist("personnel_ids")
            req.assigned_personnel.set(selected_ids)
            req.save()

        # ✅ Assign materials (with inventory deduction)
        elif "material_ids" in request.POST and req.status not in ["Done for Review", "Completed"]:
            selected_materials = request.POST.getlist("material_ids")

            # Clear old materials first (restore inventory before reassigning)
            for rm in req.requestmaterial_set.all():
                rm.material.quantity += rm.quantity  # return stock
                rm.material.save()
            req.requestmaterial_set.all().delete()

            # Deduct new selections
            for mid in selected_materials:
                material = get_object_or_404(InventoryItem, id=mid)
                qty = int(request.POST.get(f"quantity_{mid}", 1))

                # Check stock availability
                if material.quantity < qty:
                    messages.error(request, f"Not enough stock for {material.name}. Available: {material.quantity}")
                    return redirect("unit_head_request_detail", pk=req.id)

                # Deduct from inventory
                material.quantity -= qty
                material.save()

                # Save request-material relation
                RequestMaterial.objects.create(
                    request=req,
                    material=material,
                    quantity=qty
                )

            messages.success(request, "Materials assigned and deducted from inventory.")

        # ✅ Approve completion
        elif "approve_done" in request.POST and req.status == "Done for Review":
            req.status = "Completed"
            req.completed_at = timezone.now()
            req.save()

        # ✅ Reject completion
        elif "reject_done" in request.POST and req.status == "Done for Review":
            req.status = "In Progress"
            req.save()

        return redirect("unit_head_request_detail", pk=req.id)

    return render(request, "unit_heads/unit_head_request_management/request_detail.html", {
        "req": req,
        "personnel": personnel,
        "materials": materials,
        "reports": reports,  # ✅ Now available in template
    })
















@login_required
@user_passes_test(is_unit_head)
def unit_head_request_history(request):
    return render(request, "unit_heads/unit_head_request_history/unit_head_request_history.html")














# --- Personnel Views ---
@login_required
def personnel_task_management(request):
    # Always start with tasks assigned to the logged-in personnel
    tasks = ServiceRequest.objects.filter(assigned_personnel=request.user).distinct()

    # Optional search filter
    search_query = request.GET.get("user_status")
    if search_query:
        tasks = tasks.filter(
            Q(requestor__department__icontains=search_query) |
            Q(full_name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Optional status filter
    status_filter = request.GET.get("status")
    if status_filter:
        tasks = tasks.filter(status=status_filter)

    return render(
        request,
        "personnel/personnel_task_management/personnel_task_management.html",
        {"tasks": tasks}
    )









@login_required
def personnel_task_detail(request, pk):
    task = get_object_or_404(ServiceRequest, pk=pk, assigned_personnel=request.user)

    if request.method == "POST":
        # ✅ Handle status update
        if "start" in request.POST and task.status == "Approved":
            task.status = "In Progress"
            task.started_at = timezone.now()
            task.save()

        elif "done" in request.POST and task.status == "In Progress":
            task.status = "Done for Review"
            task.done_at = timezone.now()
            task.save()

        # ✅ Handle adding a TaskReport
        elif "add_report" in request.POST:
            report_text = request.POST.get("report_text", "").strip()
            if report_text:
                TaskReport.objects.create(
                    request=task,
                    personnel=request.user,
                    report_text=report_text,
                )

        return redirect("personnel_task_detail", pk=task.id)

    # ✅ Fetch assigned materials correctly
    materials = task.requestmaterial_set.select_related("material")

    # ✅ Fetch reports for display
    reports = task.reports.select_related("personnel").order_by("-created_at")

    return render(
        request,
        "personnel/personnel_task_management/personnel_task_detail.html",
        {"task": task, "materials": materials, "reports": reports}
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
            full_name=request.POST.get("full_name"),
            email=request.POST.get("email"),
            contact_number=request.POST.get("contact_number"),
            unit=request.POST.get("unit"),
            description=request.POST.get("description"),
            status="Pending",
            department=request.user.department
        )
        return redirect("requestor_request_management")
    return redirect("requestor_request_management")




@login_required
def cancel_request(request, pk):
    req = get_object_or_404(ServiceRequest, pk=pk, requestor=request.user)

    if req.status in ["Pending", "Approved"]:  # allow cancel only if not yet done
        req.status = "Cancelled"
        req.save()

    return redirect("requestor_request_management")  # adjust to your URL name










@login_required
@user_passes_test(is_requestor)
def requestor_request_history(request):
    return render(request, "requestor/requestor_request_history/requestor_request_history.html")
