from django import forms 
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Claim

class DeadlineCleanMixin:

    def clean_deadline(self):
        deadline = self.cleaned_data['deadline']
        if deadline < timezone.now():
            raise ValidationError(
                'Срок исполнения не может находиться в прошлом!'
            )
        return deadline

class ClaimForm(DeadlineCleanMixin, forms.ModelForm):
    
    class Meta:
        model = Claim
        fields = ('title', 'ammount', 'deadline', 'comment', 'image')
        widgets = {
            'deadline': forms.DateTimeInput(format='%d/%m/%Y %H:%M', attrs={'type': 'datetime-local', 'class':'form-control'}),
        }
