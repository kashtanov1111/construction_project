import datetime

from django import forms 
from django.core.exceptions import ValidationError

from .models import Claim

class DeadlineCleanMixin:

    def clean_deadline(self):
        deadline = self.cleaned_data['deadline']
        if deadline < datetime.datetime.now():
            raise ValidationError(
                'Срок исполнения не может находиться в прошлом!'
            )
        return deadline

class ClaimForm(forms.ModelForm):
    
    class Meta:
        model = Claim
        fields = ('title', 'ammount', 'deadline', 'comment', 'image')
