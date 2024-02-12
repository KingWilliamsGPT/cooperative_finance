from django import forms
from .models import (SavingDeposit,SavingWithdrawal,
        SavingAccount,)
from members.models import Member

class SavingAccountForm(forms.ModelForm):

    class Meta:
        model = SavingAccount
        fields = ('owner','status',)

class  SavingDepositForm(forms.Form):

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


class DepositForm(forms.Form):
    # I'm manually writting this form instead of using a model class, because I don't like stress :)
    mem_number = forms.IntegerField()
    montly_savings = forms.DecimalField(decimal_places=2, max_digits=10, required=False)
    amount_to_shares = forms.DecimalField(decimal_places=2, max_digits=10, required=False)
    
    # cost
    transaction_cost = forms.DecimalField(max_digits=10, decimal_places=2, required=True) 
    members_registration_cost = forms.DecimalField(max_digits=10, decimal_places=2, required=True) 

    def is_valid(self):
        return super().is_valid()
        amount_to_savings = self['montly_savings'].value()
        amount_to_shares = self['amount_to_shares'].value()
        amount_to_loan = self['loan_amount'].value()
        total_amount = self['total_amount'].value()

        actual_total = amount_to_savings + amount_to_shares + amount_to_loan
        if total_amount != ():
            raise forms.ValidationError('Total amount must equal (savings amount + shares amount + loan amount)')


    def clean_mem_number(self):
        mem_number = self.cleaned_data['mem_number']
        try:
            m = Member.objects.get(mem_number=mem_number)
        except Member.DoesNotExist:
            raise forms.ValidationError("member does not exists")

        return mem_number