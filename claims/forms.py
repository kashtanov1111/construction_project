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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['deadline'].label = 'Срок Исполнения'
        self.fields['title'].label = 'Название'
        self.fields['ammount'].label = 'Количество'
        self.fields['image'].label = 'Фотография'
        self.fields['comment'].label = 'Комментарий'
    
    class Meta:
        model = Claim
        fields = ('title', 'ammount', 'deadline', 'comment', 'image')
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        },

