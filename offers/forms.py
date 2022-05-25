from django import forms

from .models import Offer

class OfferForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['price'].label = 'Общая Цена'
        self.fields['name'].label = 'Ваше Имя'
        self.fields['phone_number'].label = 'Мобильный телефон'
        self.fields['comment'].label = 'Комментарий'

    class Meta:
        model = Offer
        fields = ('price', 'name', 'phone_number', 'email', 'comment')