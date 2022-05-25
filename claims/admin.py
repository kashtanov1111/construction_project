from django.contrib import admin

from .models import Claim
from offers.models import Offer

class OfferInline(admin.StackedInline):
    model = Offer
    extra = 1

class ClaimAdmin(admin.ModelAdmin):
    model = Claim
    inlines = [OfferInline,]

admin.site.register(Claim, ClaimAdmin)