# urls.py
from django.urls import path
from .views import DemandReportCreateView

urlpatterns = [
    path('demand', DemandReportCreateView.as_view(), name='demand'),
]
