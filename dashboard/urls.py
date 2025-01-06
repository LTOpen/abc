from django.urls import re_path, path

from . import views

urlpatterns = [
    re_path(r"^$", views.index, name="index"),
    path("accounts/", views.all_accounts, name="accounts"),
    path(
        "date_between/<str:start_date_str>/<str:end_date_str>/",
        views.main,
        name="date_between",
    ),
    path("yearview/", views.yearview, name="yearview"),
]
