from django.shortcuts import (render, redirect,
        get_object_or_404)
from django.contrib import messages
from django.db.models import Sum
from django import forms

from .forms import (LoanIssueForm,LoanPaymentForm,
       GetLoanNumForm,LoanAccountForm,GetLoanAccountForm)

from .models import (LoanAccount,LoanIssue,
    LoanPayment,LoansIssue)

from accounting.models import Income,IncomeType

# Create your views here.

# for charging loan fee by default look at loan_approve function
LOAN_FEE_PK = 1
LOAN_FEE_PERCENT = 2
INCOME_FROM_LOAN_TAX = 'INCOME_FROM_LOAN_TAX'

def loan_account(request):
    template = 'loans/loans_form.html'

    pk = request.session['ordered_loans_pk']
    print(pk)
    print("*************")

    ordered_loan_ac = get_object_or_404(LoanAccount, pk=pk)

    if request.method == 'POST':
        form = LoanAccountForm(request.POST, instance=ordered_loan_ac)
    else:
        form = LoanAccountForm(instance=ordered_loan_ac)

    if form.is_valid():
        form.save()
        return redirect('loans:loan')

    context = {
            'form': form,
            'title': "de|activate",
            }

    return render(request, template, context)


def loan_issue(request, **kwargs):
    template = 'loans/loans_form.html'

    if request.method == "POST":
        form = LoanIssueForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            if issue.account.status == 'Deactivated':
                messages.warning(request,
                        "This account is not yet activated please activate the account first")
                return redirect("loans:loan")

            if issue.status == 'Approved':
            #adds issued principal to the users account total principal
                issue.account.total_principal += issue.principal
                issue.account.save()
            issue.save()
            messages.success(request,
                        'You have successfully issued ₦{} only loan to the account number {}.'
                        .format(issue.principal,issue.account.owner.mem_number))
            if 'pk' in kwargs:
                return redirect("loans:issuepk", pk=kwargs['pk'])
            return redirect("loans:issue")
    else:
        if 'pk' in kwargs:
            ac = kwargs['pk']
            form = LoanIssueForm()
            form.fields["account"].queryset = LoanAccount.objects.filter(id=ac)
            form.fields["account"].initial = ac
            form.fields["account"].widget = forms.HiddenInput()
        else:
            form = LoanIssueForm()

    context = {
        'form': form,
        'title': "Issue",
    }

    return render(request, template, context)

def loan_payment(request, **kwargs):
    template = 'loans/loans_form.html'

    if request.method == "POST":
        form = LoanPaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            if payment.loan_num.account.status == 'Deactivated':
                messages.warning(request,
                        "This account is not yet activated please activate the account first")
                return redirect("loans:loan")

            if not payment.loan_num.status == 'Approved':
                messages.success(request,
                        'This loan with loan no. {} is not approved yet.'
                        .format(payment.loan_num.loan_num,))
                return redirect("loans:pay")
        #deducts payment principal from the selected loan issue and total principal
            payment.loan_num.principal -= payment.principal
            payment.loan_num.account.total_principal -= payment.principal
            payment.loan_num.account.save()
            payment.loan_num.save()
            payment.save()
            messages.success(request,
                            'you have successfully paid ₦ {} only loan to the account number {}.'
                            .format(payment.principal,payment.loan_num.account.owner.mem_number))

            if 'pk' in kwargs:
                return redirect("loans:paypk", pk=kwargs['pk'])
            return redirect("loans:pay")

    else:
        if 'pk' in kwargs:
            loan_ac = kwargs['pk']
            form = LoanPaymentForm()
            form.fields["loan_num"].queryset = LoanIssue.objects.filter(account=loan_ac, status="Approved")
        else:
            form = LoanPaymentForm()

    context = {
        'form': form,
        'title': "Pay",
    }

    return render(request, template, context)

def loan_issue_transactions(request):
    template = 'loans/loans_transactions.html'

    loans = LoanIssue.objects.filter(status='Approved',delete_status = False)
    loans_sum = loans.aggregate(Sum('principal'))['principal__sum']

    context = {
        'transactions': loans,
        'transactions_sum': loans_sum,
        'title': "Issue",
    }

    return render(request, template, context)

def loan_payment_transactions(request):
    template = 'loans/loans_transactions.html'

    loans = LoanPayment.objects.filter(delete_status = False)
    loans_sum = loans.aggregate(Sum('principal'))['principal__sum']

    context = {
        'transactions': loans,
        'transactions_sum': loans_sum,
        'title': "Payment",
    }

    return render(request, template, context)

def get_loan_account(request):
    template = 'loans/loans_form.html'

    form = GetLoanAccountForm(request.POST or None)

    if form.is_valid():
        loans_account = form.save(commit=False)
        pk = loans_account.account.pk
        request.session['ordered_loans_pk']=pk
        return redirect("loans:de|activate")

    context = {
        'form': form,
        'title': 'de|activate',
        }

    return render(request, template, context)

def loan_issue_transaction(request):
    template = 'loans/loans_transactions.html'

    form = GetLoanNumForm(request.POST or None)

    if form.is_valid():
        ordered_loan = form.save(commit=False)
        loans = LoanIssue.objects.filter(loan_num = ordered_loan.loan_num.loan_num, delete_status = False)
        loans_sum = loans.aggregate(Sum('principal'))['principal__sum']
        messages.success(request,
                        'Loan Issue loans of loan number {}.'
                        .format(ordered_loan.loan_num))

        context = {
            'transactions': loans,
            'transactions_sum': loans_sum,
            'title': 'Issued',
        }
        return render(request, template, context)
    context = {
        'form':form,
        'title':"Issued",
    }

    return render(request, template, context)

def loan_payment_transaction(request):
    template = 'loans/loans_transactions.html'

    form = GetLoanNumForm(request.POST or None)

    if form.is_valid():
        ordered_loan = form.save(commit=False)
        loans = LoanPayment.objects.filter(loan_num = ordered_loan.loan_num, delete_status = False)
        loans_sum = loans.aggregate(Sum('principal'))['principal__sum']
        messages.success(request,
                         'Loan Payment loans of loan number {}.'
                         .format(ordered_loan.loan_num))

        context = {
            'transactions': loans,
            'transactions_sum': loans_sum,
            'title': "Payment",
        }

        return render(request, template, context)

    context = {
        'form': form,
        'title': "Payment",
    }

    return render(request, template, context)

def get_loan(request, **kwargs):
    template = 'loans/loans_form.html'

    if 'pk' in kwargs:
        loan_ac = kwargs['pk']
        form = GetLoanNumForm(request.POST or None)
        form.fields["loan_num"].queryset = LoanIssue.objects.filter(account=loan_ac, status="Pending")
    else:
        form = GetLoanNumForm(request.POST or None)
        form.fields["loan_num"].queryset = LoanIssue.objects.filter(status="Pending")

    if form.is_valid():
        loan = form.save(commit=False)
        if loan.loan_num.status == 'Approved':
            messages.success(
                request,
                'This loan is already approved')
            if 'pk' in kwargs:
                return redirect("loans:get_loanpk", pk=kwargs['pk'])
            else:
                return redirect("loans:get_loan")

        loan_num = loan.loan_num.loan_num
        request.session['loan_num']=loan_num
        return redirect("loans:approveloan_num", loan_num=int(loan_num))

    context = {
        'form': form,
        'title': "approve",
    }
    return render(request, template, context)

def loan_approve(request, **kwargs):
    template = 'loans/loans_form.html'

    if 'loan_num' in kwargs:
        loan_num = str(kwargs['loan_num'])
    else:
        loan_num = str(request.session['loan_num'])
    
    import loans.models
    ordered_loan = get_object_or_404(loans.models.LoanIssue, loan_num = loan_num)

    if request.method == "POST":
        form = LoanIssueForm(request.POST, instance=ordered_loan)
    else:
        form = LoanIssueForm(instance=ordered_loan)

    if form.is_valid():
        issue = form.save(commit=False)
        if issue.account.status == 'Deactivated':
            messages.warning(request,
                        "This account is not yet activated please activate the account first")
            return redirect("loans:loan")
        #adds issued principal to the users total_principal of loan ac
        try:
            income_type = IncomeType.objects.get(code=INCOME_FROM_LOAN_TAX)
        except IncomeType.DoesNotExist:
            income_type = IncomeType.objects.create(
                name=INCOME_FROM_LOAN_TAX,
                code=INCOME_FROM_LOAN_TAX,
            )

        Income.objects.create(amount=LOAN_FEE_PERCENT/100*issue.principal, received_from=issue.account.owner, loan_num=issue, income_type=income_type)
        issue.account.total_principal += issue.principal
        issue.account.save()
        issue.save()
        if issue.status == 'Approved':
            LoansIssue.objects.create(account = issue.account, loan_num = issue.loan_num, principal = issue.principal)
            messages.success(
                    request,
                    'You have issued')
        else:
            messages.warning(
                    request,
                    'Loan is not yet approved')
        #if request.session:
            #del request.session['loan_num']
        if 'loan_num' in kwargs:
            issue_instance=get_object_or_404(LoanIssue, loan_num=kwargs['loan_num'])
            mem_number=issue_instance.account.owner.mem_number
            return redirect("members:member_detail", mem_number=mem_number)
        return redirect("loans:get_loan")

    context = {
        'form': form,
        'title': "confirm",
    }

    return render(request, template, context)

def loan(request):
    template = 'loans/loans.html'

    return render(request, template)

def loan_issue_delete(request, pk):
    template = 'loans/loans_delete.html'

    issue = get_object_or_404(LoanIssue, pk=pk)

    if request.method == "POST":
        issue.account.total_principal -= issue.principal
        issue.account.save()
        issue.delete_status = True
        issue.save()
        messages.success(request,
                        'You successfully deleted loans_issue of account {}, principal {} and loan no. {}.'
                        .format(issue.account,issue.principal,issue.loan_num))
        previous = request.POST.get('previous', None)

        return redirect(previous)

    context = {
        'item': issue,
        'type': "issue",
    }

    return render(request, template, context)

def loan_payment_delete(request, pk):
    template = 'loans/loans_delete.html'

    payment = get_object_or_404(LoanPayment, pk=pk)

    if request.method == "POST":
        payment.loan_num.account.total_principal += payment.principal
        payment.loan_num.account.save()
        issue.delete_status = True
        payment.save()
        messages.success(request,
                        'You successfully deleted loans_payment of principal {} and loan no. {}.'
                        .format(payment.principal,payment.loan_num))
        previous = request.POST.get('previous', None)

        return redirect(previous)

    context = {
        'item': payment,
        'type': "payment",
    }

    return render(request, template, context)


