from django import forms
from .models import Income,Expense

class IncomeForm(forms.ModelForm):

    class Meta:
        model = Income
        fields = ('__all__')

class ExpenseForm(forms.ModelForm):

    class Meta:
        model = Expense 
        fields = ('__all__')


