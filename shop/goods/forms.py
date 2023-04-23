from django import forms

from goods.models import CartItem


class ItemsCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, )


class ConfirmForm(forms.Form):
    confirm = forms.BooleanField(label='Уверены, что хотите очистить корзину?', required=True)
