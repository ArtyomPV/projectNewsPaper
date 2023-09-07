from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class ProtectView(LoginRequiredMixin, View):
    template_name = 'protect/index.html'
