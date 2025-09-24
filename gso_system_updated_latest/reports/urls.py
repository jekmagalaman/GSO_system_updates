from django.urls import path
from . import views

urlpatterns = [
    path("accomplishment-report/", views.accomplishment_report, name="accomplishment_report"),


    path("accomplishment-report/ipmt/", views.generate_ipmt, name="generate_ipmt"),
]
