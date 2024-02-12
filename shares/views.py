from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.db.models import Sum
from django import forms
from .forms import (ShareAccountForm,ShareBuyForm,
        ShareSellForm,GetShareAccountForm)

from .models import (ShareBuy,ShareSell,
        ShareAccount,)


from notifications.view_helpers import AdminNotificationViewHelper


# def _share_buy(request):

    

def share_account(request):
    template = 'shares/shares_form.html'

    pk = request.session['ordered_shares_pk']

    ordered_share_ac = get_object_or_404(ShareAccount, pk=pk)

    if request.method == 'POST':
        form = ShareAccountForm(request.POST, instance=ordered_share_ac)
    else:
        form = ShareAccountForm(instance=ordered_share_ac)

    if form.is_valid():
        form.save()

        AdminNotificationViewHelper.de_or_activate(request, form.instance)
        return redirect('shares:share')

    context = {
            'form': form,
            'title': "de|activate",
    }

    return render(request, template, context)

def share_buy(request, **kwargs):
    template = 'shares/shares_form.html'

    if request.method == "POST":
        form = ShareBuyForm(request.POST)
        if form.is_valid(): 
            buy = form.save(commit=False)
            if buy.account.status == "Deactivated":
                messages.warning(request,
                        "This account is not activated yet please activate the account first")
                return redirect("shares:share")
            #adds bought share to current share of shares account
            buy.account.current_share += buy.number
            buy.account.save()
            buy.save()
            
            AdminNotificationViewHelper.shares_buy_or_sell(request, buy)

            messages.success(request,
                    'You have successfully added {} share to account number {}.'
                    .format(buy.number,buy.account.owner.mem_number))

            if 'pk' in kwargs:
                return redirect("shares:buypk", pk=kwargs['pk'])
            return redirect("shares:buy")

    else:
        if 'pk' in kwargs:
            ac = kwargs['pk']
            form = ShareBuyForm()
            form.fields["account"].queryset = ShareAccount.objects.filter(id=ac)
            form.fields["account"].initial = ac
            form.fields["account"].widget = forms.HiddenInput()
        else:
            form = ShareBuyForm()

    context = {
            'form': form,
            'title': "Buy",
    }

    return render(request, template, context)


def share_sell(request, **kwargs):
    template = 'shares/shares_form.html'

    if request.method == "POST":
        form = ShareSellForm(request.POST)
        if form.is_valid():
            sell = form.save(commit=False)
            if sell.account.status == "Deactivated":
                messages.warning(request,
                        "This account is not activated yet please activate the account first")
                return redirect("shares:share")
            #deletes sold share from current share of shares account
            sell.account.current_share -= sell.number
            sell.account.save()
            sell.save()

            AdminNotificationViewHelper.shares_buy_or_sell(request, sell)

            messages.success(request,
                    'You have successfully sold {} share of account number {}.'
                    .format(sell.number,sell.account.owner.mem_number))

            if 'pk' in kwargs:
                return redirect("shares:sellpk", pk=kwargs['pk'])
            return redirect("shares:sell")

    else:
        if 'pk' in kwargs:
            ac = kwargs['pk']
            form = ShareSellForm()
            form.fields["account"].queryset = ShareAccount.objects.filter(id=ac)
            form.fields["account"].initial = ac
            form.fields["account"].widget = forms.HiddenInput()
        else:
            form = ShareSellForm()

    context = {
            'form': form,
            'title': "Sell",
            }

    return render(request, template, context)

def share_buy_transactions(request):
    template = 'shares/shares_transactions.html'

    shares = ShareBuy.objects.filter(delete_status = False)
    shares_sum = shares.aggregate(Sum('number'))['number__sum']

    context = {
            'transactions': shares,
            'transactions_sum': shares_sum,
            'title': "Buys",
            }

    return render(request, template, context)

def share_sell_transactions(request):
    template = 'shares/shares_transactions.html'

    shares = ShareSell.objects.filter(delete_status = False)
    shares_sum = shares.aggregate(Sum('number'))['number__sum']

    context = {
            'transactions': shares,
            'transaxtions_sum': shares_sum,
            'title': "Sells",
            }

    return render(request, template, context)

def get_share_account(request):
    template = 'shares/shares_form.html'

    form = GetShareAccountForm(request.POST or None)

    if form.is_valid():
        shares_account = form.save(commit=False)
        pk = shares_account.account.pk
        request.session['ordered_shares_pk']=pk
        return redirect("shares:de|activate")

    context = {
            'form': form,
            'title': "de|activate",
            }

    return render(request, template, context)

def share_buy_transaction(request):
    template = 'shares/shares_transactions.html'

    form = GetShareAccountForm(request.POST or None)

    if form.is_valid():
        ordered_account = form.save(commit=False)
        shares = ShareBuy.objects.filter(account = ordered_account.account,delete_status = False)
        shares_sum = shares.aggregate(Sum('number'))['number__sum']
        messages.success(request,
                'Buys of share account number {}.'
                .format(ordered_account.account.owner.mem_number))

        context = {
                'transactions': shares,
                'transactions_sum': shares_sum,
                'title': "Buys",
                }

        return render(request, template, context)

    context = {
            'form': form,
            'title': "Buys",
            }

    return render(request, template, context)

def share_sell_transaction(request):
    template = 'shares/shares_transactions.html'

    form = GetShareAccountForm(request.POST or None)

    if form.is_valid():
        ordered_account = form.save(commit=False)
        shares = ShareSell.objects.filter(account = ordered_account.account, delete_status = False)
        shares_sum = shares.aggregate(Sum('number'))['number__sum']
        messages.success(request,
                'Sells of share account number {}.'
                .format(ordered_account.account.owner.mem_number))

        context = {
                'transactions': shares,
                'transactions_sum': shares_sum,
                'title': "Sells",
                }

        return render(request, template, context)

    context = {
            'form': form,
            'title': "Sells",
            }

    return render(request, template, context)

def share(request):
    template = 'shares/shares.html'

    return render(request, template)

def share_buy_delete(request, pk):
    template = 'shares/shares_delete.html'

    buy = get_object_or_404(ShareBuy, pk=pk)

    if request.method == "POST":
        buy.account.current_share -= buy.number
        buy.account.save()
        buy.delete_status = True
        buy.save()
        messages.success(request,
                        'You successfully deleted share_buy of account {} and number {}.'
                        .format(buy.account,buy.number))
        previous = request.POST.get('previous', None)

        return redirect(previous)

    context = {
        'item': buy,
        'type': "Buy",
    }

    return render(request, template, context)

def share_sell_delete(request, pk):
    template = 'shares/shares_delete.html'

    sell = get_object_or_404(ShareSell, pk=pk)

    if request.method == "POST":
        sell.account.current_share += sell.number
        sell.account.save()
        sell.delete_status = True
        sell.save()
        messages.success(request,
                        'You successfully deleted share_sell of account {} and number {}.'
                        .format(sell.account,sell.number))
        previous = request.POST.get('previous', None)

        return redirect(previous)

    context = {
        'item': sell,
        'type': "Sell",
    }

    return render(request, template, context)
