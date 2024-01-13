from django.shortcuts import render
from django.db.models import Sum

import savings.models
import loans.models
import shares.models
import members.models

def home(request):
    template = 'static_pages/home.html'
    
    savings_deposit = savings.models.SavingDeposit.objects.filter(delete_status=False)
    savings_dep_sum = savings_deposit.aggregate(Sum('amount'))['amount__sum']
    savings_withdrawal = savings.models.SavingWithdrawal.objects.filter(delete_status=False)
    savings_withdrawal_sum = savings_withdrawal.aggregate(Sum('amount'))['amount__sum']
    
    loan_issue = loans.models.LoanIssue.objects.filter(status='Approved', delete_status=False)
    loan_issue_sum = loan_issue.aggregate(Sum('principal'))['principal__sum']
    loan_issue_pending = loans.models.LoanIssue.objects.filter(status='Pending', delete_status=False)
    loan_issue_pending_sum = loan_issue_pending.aggregate(Sum('principal'))['principal__sum']
    loan_payment = loans.models.LoanPayment.objects.filter(delete_status=False)
    loan_payment_sum = loan_payment.aggregate(Sum('principal'))['principal__sum']

    shares_buy = shares.models.ShareBuy.objects.filter(delete_status = False)
    shares_buy_sum = shares_buy.aggregate(Sum('number'))['number__sum']
    shares_sell = shares.models.ShareSell.objects.filter(delete_status = False)
    shares_sell_sum = shares_sell.aggregate(Sum('number'))['number__sum']

    members_ = members.models.Member.objects.all()

    context = {
        'savings_deposit': savings_deposit,
        'savings_deposit_sum': savings_dep_sum,
        'savings_withdrawal': savings_withdrawal,
        'savings_withdrawal_sum': savings_withdrawal_sum,
        'loan_issue': loan_issue,
        'loan_issue_sum': loan_issue_sum,
        'loan_issue_pending': loan_issue_pending,
        'loan_issue_pending_sum': loan_issue_pending_sum,
        'loan_payment': loan_payment,
        'loan_payment_sum': loan_payment_sum,
        'shares_buy': shares_buy,
        'shares_buy_sum': shares_buy_sum,
        'shares_sell': shares_sell,
        'shares_sell_sum': shares_sell_sum,
        'members': members_,
    }
    return render(request, template, context)

def about(request):
    template = 'static_pages/about.html'

    return render(request, template)

def contact(request):
    template = 'static_pages/contact.html'

    return render(request, template)

def tutorial(request):
    template = 'static_pages/tutorial.html'

    return render(request, template)

