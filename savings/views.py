from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum
from django import forms

from .forms import (SavingDepositForm,SavingWithdrawalForm,
        GetSavingAccountForm,SavingAccountForm,)
                    
from .models import (SavingDeposit,SavingWithdrawal,
                    SavingAccount,)
from notifications.view_helpers import AdminNotificationViewHelper

from user.models import User


def saving_account(request):
    template = 'savings/savings_form.html'

    pk = request.session['ordered_savings_pk']

    ordered_saving_ac = get_object_or_404(SavingAccount, pk=pk)

    if request.method == 'POST':
        form = SavingAccountForm(request.POST, instance=ordered_saving_ac)
    else:
        form = SavingAccountForm(instance=ordered_saving_ac)

    if form.is_valid():
        instance = ordered_saving_ac
        if form['status'] and form['status'] != instance.status:
            AdminNotificationViewHelper.de_or_activate(request, instance)
        form.save()
        return redirect("savings:saving")

    context = {
            'form':form,
            'title': "de|activate",
            }

    return render(request, template, context)


def saving_deposit(request, **kwargs):
    template = 'savings/savings_form.html'

    if request.method == 'POST':
        form = SavingDepositForm(request.POST)
        if form.is_valid():
            deposit = form.save(commit=False)
            if deposit.account.status == 'Deactivated':
                messages.warning(request,
                        "This account is not yet activated please activate the account first")
                return redirect("savings:saving")
            # adds deposit to the users saving account current balance
            deposit.account.current_balance += deposit.amount
            deposit.account.save()
            deposit.save()
            
            # notify users
            AdminNotificationViewHelper.create_deposite(request, deposit)
            
            messages.success(request,
                         'You Have successfully Deposited ₦ {} only to the account number {}.'
                         .format(deposit.amount,deposit.account.owner.mem_number))
            if 'pk' in kwargs:
                return redirect("savings:depositpk", pk=kwargs['pk'])
            return redirect("savings:deposit")
    else:
        if 'pk' in kwargs:
            ac=kwargs['pk']
            form = SavingDepositForm()
            form.fields["account"].queryset = SavingAccount.objects.filter(id=ac)
            form.fields["account"].initial = ac
            form.fields["account"].widget = forms.HiddenInput() 
        else:
             form = SavingDepositForm()
    context = {
            'form': form,
            'title': "Deposit"
    }

    return render(request, template, context)

def saving_withdrawal(request, **kwargs):
    template = 'savings/savings_form.html'

    if request.method == "POST":
        form = SavingWithdrawalForm(request.POST)
        if form.is_valid():
            withdraw = form.save(commit=False)
            if withdraw.account.status == 'Deactivated':
                messages.warning(request,
                        "This account is not yet activated please activate the account first")
                return redirect("savings:saving")
            # checks if withdrawal amount is valid
            if(withdraw.account.current_balance >= withdraw.amount and
                    withdraw.amount >= 10):
                withdraw.account.current_balance -= withdraw.amount
                withdraw.account.save()
                withdraw.save()

                AdminNotificationViewHelper.create_withdraw(request, withdraw)

                messages.success(
                    request,
                    'You Have Withdrawn ₦ {} only from the account number {}.'
                    .format(withdraw.amount,withdraw.account.owner.mem_number))

                if 'pk' in kwargs:
                    return redirect("savings:withdrawpk", pk=kwargs['pk'])
                return redirect("savings:withdraw")
            else:
                messages.error(
                    request,
                    "Either you are trying to withdraw less than ₦10 or your current balance is not sufficient"
                )
    else:
        if 'pk' in kwargs:
            ac = kwargs['pk']
            form = SavingWithdrawalForm()
            form.fields["account"].queryset = SavingAccount.objects.filter(id=ac)
            form.fields["account"].initial = ac
            form.fields["account"].widget = forms.HiddenInput() 
        else:
            form = SavingWithdrawalForm()

    context = {
        'form': form,
        'title': "Withdraw"
    }

    return render(request, template, context)

def saving_deposit_transactions(request):
    template = 'savings/savings_transactions.html'

    savings = SavingDeposit.objects.filter(delete_status=False)
    savings_sum = savings.aggregate(Sum('amount'))['amount__sum']

    context = {
        'transactions': savings,
        'transactions_sum': savings_sum,
        'title': "Deposit",
    }

    return render(request, template, context)

def saving_withdrawal_transactions(request):
    template = 'savings/savings_transactions.html'

    savings = SavingWithdrawal.objects.filter(delete_status=False)
    savings_sum = savings.aggregate(Sum('amount'))['amount__sum']

    context = {
        'transactions': savings,
        'transactions_sum': savings_sum,
        'title': "Withdrawal",
    }

    return render(request, template, context)

def get_saving_account(request):
    template = 'savings/savings_form.html'

    form = GetSavingAccountForm(request.POST or None)

    if form.is_valid():
        savings_account = form.save(commit=False)
        pk = savings_account.account.pk
        request.session['ordered_savings_pk']=pk
        return redirect("savings:de|activate")

    context = {
        'form': form,
        'title': "de|activate",
    }

    return render(request, template, context)


def saving_deposit_transaction(request):
    template = 'savings/savings_transactions.html'

    form = GetSavingAccountForm(request.POST or None)

    if form.is_valid():
        ordered_account = form.save(commit=False)
        savings = SavingDeposit.objects.filter(account = ordered_account.account, delete_status=False)
        savings_sum = savings.aggregate(Sum('amount'))['amount__sum']
        messages.success(request,
                         'Deposit savings of savings account number {}.'
                         .format(ordered_account.account.owner.mem_number))
        context = {
            'transactions': savings,
            'transactions_sum': savings_sum,
            'title': "Deposit",
        }

        return render(request, template, context)

    context = {
        'form': form,
        'title': "Deposit",
    }

    return render(request, template, context)

def saving_withdrawal_transaction(request):
    template = 'savings/savings_transactions.html'

    form = GetSavingAccountForm(request.POST or None)

    if form.is_valid():
        ordered_account = form.save(commit=False)
        savings = SavingWithdrawal.objects.filter(account = ordered_account.account, delete_status=False)
        savings_sum = savings.aggregate(Sum('amount'))['amount__sum']
        messages.success(request,
                         'Withdrawal ransactions of savings account number {}.'
                         .format(ordered_account.account.owner.mem_number))

        context = {
            'transactions':savings,
            'transactions_sum':savings_sum,
            'title': "Withdrawal",
        }

        return render(request, template, context)
    context = {
        'form':form,
        'title': "Withdrawal",
    }

    return render(request, template, context)

def saving(request):
    template = 'savings/savings.html'

    return render(request, template)

def saving_deposit_delete(request, pk):
    template = 'savings/savings_delete.html'

    deposit = get_object_or_404(SavingDeposit, pk=pk)

    if request.method == "POST":
        deposit.account.current_balance -= deposit.amount
        deposit.account.save()
        deposit.delete_status = True
        deposit.save()
        messages.success(request,
                        'You successfully deleted saving_deposit of account {} and amount {}.'
                        .format(deposit.account,deposit.amount))
        previous = request.POST.get('previous', None)

        return redirect(previous)

    context = {
        'item': deposit,
        'type': "deposit",
    }

    return render(request, template, context)

def saving_withdrawal_delete(request, pk):
    template = 'savings/savings_delete.html'

    withdrawal = get_object_or_404(SavingWithdrawal, pk=pk)

    if request.method == "POST":
        withdrawal.account.current_balance += withdrawal.amount
        withdrawal.account.save()
        withdrawal.delete_status = True
        withdrawal.save()
        messages.success(request,
                        'You successfully deleted saving_withdrawal of account {} and amount {}.'
                        .format(withdrawal.account,withdrawal.amount))
        previous = request.POST.get('previous', None)

        return redirect(previous)

    context = {
        'item': withdrawal,
        'type': "withdrawal",
    }

    return render(request, template, context)
