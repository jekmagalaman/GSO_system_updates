from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from .models import ServiceRequest

#GSO Office Views
def is_gso(user):
    return user.is_authenticated and user.role == 'gso'

@login_required
@user_passes_test(is_gso)

def request_management(request):
    requests = ServiceRequest.objects.select_related("requestor").all().order_by("-created_at")

    context = {
        "user_role": request.user.role,
        "requests": requests,
    }
    return render(request, "gso_office/request_management/request_management.html", context)







#Unit Head Views
@login_required
def unit_head_request_management(request):
    return render(request, "unit_heads/unit_head_request_management/unit_head_request_management.html")

@login_required
def unit_head_request_history(request):
    return render(request, 'unit_heads/unit_head_request_history/unit_head_request_history.html')



#Personnel Views
@login_required
def personnel_task_management(request):
    return render(request, 'personnel/personnel_task_management/personnel_task_management.html')

@login_required
def personnel_history(request):
    return render(request, 'personnel/personnel_history/personnel_history.html')



#Requestor Views
@login_required
def requestor_request_management(request):
    return render(request, 'requestor/requestor_request_management/requestor_request_management.html')

@login_required
def requestor_request_history(request):
    return render(request, 'requestor/requestor_request_history/requestor_request_history.html')