from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DeleteView, UpdateView
from django.shortcuts import render
from django.urls import reverse_lazy

from .models import Claim
from .forms import ClaimForm

from config.utils import PageLinksMixin

class ClaimListView(PageLinksMixin, ListView):
    paginate_by = 10
    context_object_name = 'claim_list'
    queryset = Claim.objects.all()
    ordering = '-created'

class ClaimDeleteView(LoginRequiredMixin, DeleteView):
    queryset = Claim.objects.all()
    success_url = reverse_lazy('claims:claim_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next')
        return context

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            user=self.request.user
        )

class ClaimUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ClaimForm
    success_url = reverse_lazy('claims:claim_list')
    model = Claim