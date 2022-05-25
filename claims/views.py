import math

import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, Http404, HttpResponseRedirect
from django.views.generic import (
    ListView, DeleteView, UpdateView, CreateView, View)
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone

from offers.models import Offer
from offers.forms import OfferForm

from .models import Claim
from .forms import ClaimForm

from config.utils import PageLinksMixin

class ClaimListView(PageLinksMixin, ListView):
    paginate_by = 10
    context_object_name = 'claim_list'
    model = Claim

    def get_queryset(self):
        return self.model.objects.filter(deadline__gt=timezone.now()).select_related('user').order_by('-created')

class ClaimExpiredListView(PageLinksMixin, ListView):
    paginate_by = 10
    context_object_name = 'claim_list'
    model = Claim
    
    def get_queryset(self):
        return self.model.objects.filter(deadline__lt=timezone.now()).select_related('user').order_by('-created')

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
    model = Claim

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            user=self.request.user
        )

class ClaimCreateView(LoginRequiredMixin, CreateView):
    form_class = ClaimForm
    model = Claim

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class ClaimDetailView(View):
    template_name = 'claims/claim_detail.html'
    model = Claim
    form = OfferForm
    def get(self, request, **kwargs):
        try:
            claim_obj = (self.model.objects
                            .select_related('user')
                            .get(slug=self.kwargs['slug']))
            claim_offers = claim_obj.offers.order_by('price')
            if claim_offers:
                best_offer_price = claim_offers.first().price
                best_offer_unit_price = round(best_offer_price / claim_obj.ammount, 3)
            else:
                best_offer_price = None
                best_offer_unit_price = None
        except ObjectDoesNotExist:
            raise Http404()
        return render(request, self.template_name,
            {'claim': claim_obj, 'claim_offers': claim_offers,
            'form': self.form, 'best_offer_price': best_offer_price,
            'best_offer_unit_price': best_offer_unit_price})

    def post(self, request, **kwargs):
        claim_obj = self.model.objects.get(slug=self.kwargs['slug'])
        bound_form = self.form(request.POST or None)
        if bound_form.is_valid():
            bound_form = bound_form.save(commit=False)
            bound_form.claim = claim_obj
            bound_form.save()
            messages.add_message(request, messages.INFO, 'Ваше предложение принято. Спасибо!')
            return HttpResponseRedirect(reverse('claims:claim_detail', kwargs={'slug': self.kwargs['slug']}))
        else:
            return render(request, self.template_name,
                {'form': bound_form})