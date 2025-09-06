from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('redirect/', views.role_redirect, name='role-redirect'),


    #GSO Office URLs
    path('account-management/', views.account_management, name='account_management'),
    path('accounts/', views.account_view, name='account_management'),
    path('edit/<int:user_id>/', views.edit_user, name='edit_user'),


    #Requestor URLs
    path('requestor-account/', views.requestor_account, name='requestor_account'),
]
