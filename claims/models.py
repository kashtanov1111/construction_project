import os
import datetime
import math

from random import randint

from transliterate import translit

from django.db import models
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone

def round_down(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier

class Claim(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(null=True, blank=True, unique=True)
    ammount = models.IntegerField()
    deadline = models.DateTimeField()
    comment = models.TextField(max_length=1000, blank=True, null=True)
    image = models.ImageField(upload_to='images', blank=True, null=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='claims', blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('claims:claim_detail', 
                        kwargs={'slug': self.slug})

    def claim_ends(self):
        delta = self.deadline - timezone.now()
        if delta > datetime.timedelta(seconds=1):
            delta = delta
        else:
            delta = None
        return delta

    def get_delete_url(self):
        return reverse('claims:claim_delete', 
                        kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('claims:claim_update', 
                        kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        russian_slugified_title = translit(self.title, language_code='ru', reversed=True)
        slugified_title = slugify(russian_slugified_title[:40])
        if not self.slug == slugified_title:
            self.slug = slugified_title
            while Claim.objects.filter(slug=self.slug).exists():
                self.slug = self.slug + str(randint(1, 100))
        return super().save(*args, **kwargs)