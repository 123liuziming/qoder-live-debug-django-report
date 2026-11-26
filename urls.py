from django.urls import path

from ledger.views import report, report_page

urlpatterns = [path("", report_page), path("reports/branch", report)]
