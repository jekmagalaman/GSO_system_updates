from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import UserEditForm

User = get_user_model()

@login_required
def role_redirect(request):
    user = request.user
    if user.role == 'gso':
        return redirect('gso-dashboard')
    elif user.role == 'unit_head':
        return redirect('unit-head-dashboard')
    elif user.role == 'personnel':
        return redirect('personnel-dashboard')
    elif user.role == 'employee':
        return redirect('employee-dashboard')
    else:
        return redirect('login')


#Account Management Views for GSO Office
@login_required
def account_management(request):
    return render(request, 'gso_office/accounts/account_management.html')


User = get_user_model()

def account_view(request):
    users = User.objects.all()

    # Filtering by status (active/inactive)
    status_filter = request.GET.get('status')
    if status_filter:
        users = users.filter(is_active=(status_filter == 'active'))


    #search functionality
    search_query = request.GET.get('user_status')
    if search_query:
        users = users.filter(
            first_name__icontains=search_query
        ) | users.filter(
            last_name__icontains=search_query
        ) | users.filter(
            username__icontains=search_query
        )


    return render(request, 'gso_office/accounts/account_management.html', {'users': users})


def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('account_management')
    else:
        form = UserEditForm(instance=user)
    
    return render(request, 'gso_office/accounts/account_edit.html', {'form': form, 'user': user})




# Requestor Views
@login_required
def requestor_account(request):
    return render(request, 'requestor/requestor_account/requestor_account.html')