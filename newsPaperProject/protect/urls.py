from django.urls import path
from .views import ProtectView

app_name = 'protect'

urlpatterns = [
    path('', ProtectView.as_view()),
]