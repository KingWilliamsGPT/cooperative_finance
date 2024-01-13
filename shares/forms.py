from django import forms
from .models import (ShareAccount,ShareBuy,
        ShareSell,)

class ShareAccountForm(forms.ModelForm):

    class Meta:
        model = ShareAccount
        fields = ('owner','status',)

class ShareBuyForm(forms.ModelForm):

    class Meta:
        model = ShareBuy
        fields = ('__all__')

class ShareSellForm(forms.ModelForm):

    class Meta:
        model = ShareSell
        fields = ('__all__')

class GetShareAccountForm(forms.ModelForm):

    class Meta:
        model = ShareSell
        fields = ('account',)



