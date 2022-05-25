from random import randint

from transliterate import translit

from django.db import models
from django.template.defaultfilters import slugify

from claims.models import Claim

class Offer(models.Model):
    price = models.DecimalField(max_digits=20, decimal_places=2)
    slug = models.SlugField(null=True, blank=True, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200)
    phone_number = models.BigIntegerField()
    email = models.EmailField(null=True, blank=True)
    comment = models.TextField(max_length=2000, blank=True, null=True)
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE, related_name='offers')

    def __str__(self):
        return self.name + str(self.price)

    def unit_price(self):
        return self.price / self.claim.ammount

    def save(self, *args, **kwargs):
        russian_slugified_title = translit(self.name + str(self.price), language_code='ru', reversed=True)
        slugified_title = slugify(russian_slugified_title[:40])
        if not self.slug == slugified_title:
            self.slug = slugified_title
            while Claim.objects.filter(slug=self.slug).exists():
                self.slug = self.slug + str(randint(1, 100))
        return super().save(*args, **kwargs)