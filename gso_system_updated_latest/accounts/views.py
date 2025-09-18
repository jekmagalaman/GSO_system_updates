from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import UserEditForm, RequestorProfileUpdate, UserForm
from django.contrib.auth.hashers import make_password



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
    elif user.role == 'requestor':
        return redirect('requestor-dashboard')
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




def add_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data["password"])  # hash password
            user.save()
            return redirect("account_management")  # go back to the list
    else:
        form = UserForm()
    return render(request, "gso_office/accounts/add_user.html", {"form": form})























# Requestor Views
@login_required
def requestor_account(request):
    return render(request, 'requestor/requestor_account/requestor_account.html')

@login_required
def profile(request):
    if request.method == "POST":
        form = RequestorProfileUpdate(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("requestor_account")  # reload page with updated info
    else:
        form = RequestorProfileUpdate(instance=request.user)

    return render(request, "requestor/account.html", {"form": form})