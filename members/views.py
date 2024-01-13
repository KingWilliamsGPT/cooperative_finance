from django.shortcuts import render, get_object_or_404, redirect
from .forms import MemberCreateForm
from .models import Member
from savings.models import (SavingAccount, SavingDeposit,
        SavingWithdrawal,)
from loans.models import (LoanAccount,LoanIssue,
        LoanPayment,)
from shares.models import (ShareAccount,ShareSell,
        ShareBuy,)

# Create your views here.

def member_create(request):
    template = 'members/form.html'

    form = MemberCreateForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('members:member')

    context = {
            'form': form,
            'title': "Create",
            }

    return render(request, template, context)


def member(request):
    template = 'members/members.html'

    members = Member.objects.order_by("mem_number")

    context = {
            'members': members,
            }

    return render(request, template, context)

def member_detail(request, mem_number):
    template = 'members/member_details.html'

    member = get_object_or_404(Member, mem_number=mem_number)
    saving_ac = get_object_or_404(SavingAccount, owner=member)
    deposit_transactions = SavingDeposit.objects.filter(account=saving_ac, delete_status = False)
    withdrawal_transactions = SavingWithdrawal.objects.filter(account=saving_ac, delete_status = False)
    loan_ac = get_object_or_404(LoanAccount, owner=member)
    pending_loan = LoanIssue.objects.filter(account=loan_ac, status="Pending", delete_status = False)
    approved_loan = LoanIssue.objects.filter(account=loan_ac, status="Approved", delete_status = False)
    issue_transactions = LoanIssue.objects.filter(account=loan_ac, delete_status = False)
    payment_transactions = LoanPayment.objects.filter(loan_num__account=loan_ac, delete_status = False)
    share_ac = get_object_or_404(ShareAccount, owner=member)
    sell_transactions = ShareSell.objects.filter(account=share_ac, delete_status = False)
    buy_transactions = ShareBuy.objects.filter(account=share_ac, delete_status = False)

    context = {
            'member': member,
            'saving_ac': saving_ac,
            'loan_ac': loan_ac,
            'share_ac': share_ac,
            'pending_loan': pending_loan,
            'approved_loan': approved_loan,
            'deposit_transactions': deposit_transactions,
            'withdrawal_transactions': withdrawal_transactions,
            'issue_transactions': issue_transactions,
            'payment_transactions': payment_transactions,
            'sell_transactions': sell_transactions,
            'buy_transactions': buy_transactions,
    }

    return render(request, template, context)

