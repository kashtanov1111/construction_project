from xmlrpc.client import DateTime
from django import forms 
from django.contrib.admin import widgets
from django.core.exceptions import ValidationError
from django.utils import timezone

from bootstrap_datepicker_plus.widgets import DateTimePickerInput

from .models import Claim

class TitleCleanMixin:

    def clean_title(self):
        title = self.cleaned_data['title']
        if title == 'среате':
            raise ValidationError(
                'Такое название заявки недопустимо!'
            )
        return title

class DeadlineCleanMixin:

    def clean_deadline(self):
        deadline = self.cleaned_data['deadline']
        if deadline < timezone.now():
            raise ValidationError(
                'Срок исполнения не может находиться в прошлом!'
            )
        return deadline

class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'
    input_formats = '%Y-%m-%dT%H:%M'

class ClaimForm(DeadlineCleanMixin, TitleCleanMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['deadline'].label = 'Истекает'
        self.fields['title'].label = 'Название'
        self.fields['ammount'].label = 'Количество'
        self.fields['image'].label = 'Фотография'
        self.fields['comment'].label = 'Комментарий'
    
    deadline = forms.DateTimeField(localize=True, widget=forms.DateTimeInput(format='%Y-%m-%dT%H:%M', attrs={'type': 'datetime-local'}))

    class Meta:
        model = Claim
        fields = ('title', 'ammount', 'deadline', 'comment', 'image')
        widgets = {
            # 'deadline': forms.DateTimeInput(format='%Y-%m-%dT%H:%M', attrs={'type': 'datetime-local'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

