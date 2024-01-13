from django import forms
from .models import (LoanIssue,LoanPayment,LoanAccount)

class LoanAccountForm(forms.ModelForm):
    class Meta:
        model = LoanAccount
        fields = ('owner','status',)

class LoanIssueForm(forms.ModelForm):
    class Meta:
        model = LoanIssue
        fields = ('__all__')

class LoanPaymentForm(forms.ModelForm):
    class Meta:
        model = LoanPayment
        fields = ('__all__')

class GetLoanNumForm(forms.ModelForm):
    class Meta:
        model = LoanPayment
        fields = ('loan_num',)

class GetLoanAccountForm(forms.ModelForm):
    class Meta:
        model = LoanIssue
        fields = ('account',)
