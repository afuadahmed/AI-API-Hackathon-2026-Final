from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("track/", views.track_report, name="track_report"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path(
        "update/<int:report_id>/",
        views.update_status,
        name="update_status",
    ),
]