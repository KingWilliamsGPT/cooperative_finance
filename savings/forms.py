from django import forms
from .models import (SavingDeposit,SavingWithdrawal,
        SavingAccount,)

class SavingAccountForm(forms.ModelForm):

    class Meta:
        model = SavingAccount
        fields = ('owner','status',)

class SavingDepositForm(forms.ModelForm):

    class Meta:
        model = SavingDeposit
        fields = ('__all__')

class SavingWithdrawalForm(forms.ModelForm):

    class Meta:
        model = SavingWithdrawal
        fields = ('__all__')

class GetSavingAccountForm(forms.ModelForm):

    class Meta:
        model = SavingDeposit
        fields = ('account',)


