from django.views.generic import TemplateView

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

def home_view(request):
    return HttpResponseRedirect(reverse('claims:claim_list'))
