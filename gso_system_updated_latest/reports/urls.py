from django.urls import path
from . import views

urlpatterns = [
    path("accomplishment-report/", views.accomplishment_report, name="accomplishment_report"),
]
