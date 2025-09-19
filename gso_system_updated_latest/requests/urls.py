# requests/urls.py
from django.urls import path
from . import views

urlpatterns = [
    #GSO Office URLs
    path('gso/', views.request_management, name='gso-dashboard'),
    path('gso/request-management', views.request_management, name='request_management'),

    path("requests/<int:pk>/approve/", views.approve_request, name="approve_request"),


    # Unit Head URLs
    path('unit-head/', views.unit_head_request_management, name='unit-head-dashboard'),
    path('unit-head/unit-head-request-management/', views.unit_head_request_management, name='unit_head_request_management'),
    path('unit-head/unit-head-request_history/', views.unit_head_request_history, name='unit_head_request_history'),

    # Updated detail URL (use the new merged view)
    path("unit-head/requests/<int:pk>/", views.unit_head_request_detail, name="unit_head_request_detail"),





    #Personnel URLs
    path('personnel/', views.personnel_task_management, name='personnel-dashboard'),
    path('personnel/personnel-task-management/', views.personnel_task_management, name='personnel_task_management'),
    path("tasks/<int:pk>/", views.personnel_task_detail, name="personnel_task_detail"),
    path('personnel/personnel-history/', views.personnel_history, name='personnel_history'),



    #Requestor URLs
    path('requestor/', views.requestor_request_management, name='requestor-dashboard'),
    path('requestor/requestor-request-management/', views.requestor_request_management, name='requestor_request_management'),
    path('requestor/requestor-request-history/', views.requestor_request_history, name='requestor_request_history'),

    path("requests/add/", views.add_request, name="add_request"),
    path("requests/<int:pk>/cancel/", views.cancel_request, name="cancel_request"),

]
