from django.shortcuts import render
from accounting.models import Income,Expense
from loans.models import LoanPayment,LoanIssue,LoansIssue
from shares.models import ShareBuy,ShareSell
from savings.models import SavingDeposit,SavingWithdrawal
from django.db.models import Sum
from datetime import datetime

# helper functions

def total_capital(keys, pre_context):
        for item in keys:
            if pre_context.get(item) != None:
                items_sum = 0
                items_sum = items_sum + pre_context[item]
                return items_sum

# Create your views here.

def report(request):
    template = 'reports/reports.html'

    return render(request, template)

def _income(year=datetime.now().year, month=datetime.now().month, yearly=False):
    if yearly == True:
        incomes = Income.objects.filter(delete_status = False, date_created__year = year)
    else:
        incomes = Income.objects.filter(delete_status = False, date_created__year = year,
                date_created__month = month)
    return incomes

def income(request):
    template = 'reports/income.html'

    # Implement date picker or something else that is less error prone
    if request.method == 'POST':
        month = request.POST.get('month')
        year = request.POST.get('year')
        incomes = _income(year=year,month=month)
    else:
        incomes = _income()

    context = {
        'items_income': incomes,
        'title_income': 'Income',
        'total_income': incomes.aggregate(Sum('amount'))['amount__sum']
        }

    return render(request, template, context)

def _expense(year=datetime.now().year, month=datetime.now().month, yearly=False):
    if yearly == True:
        expenses = Expense.objects.filter(delete_status = False, date_created__year = year)
    else:
        expenses = Expense.objects.filter(delete_status = False, date_created__year = year,
                date_created__month = month)
    return expenses

def expense(request):
    template = 'reports/expense.html'

    if request.method == 'POST':
        month = request.POST.get('month')
        year = request.POST.get('year')
        expenses = _expense(year=year,month=month)
    else:
        expenses = _expense()

    context = {
            'items_expenses': _expense(),
            'title_expenses': "Expense",
            'total_expense': expenses.aggregate(Sum('amount'))['amount__sum']
            }

    return render(request, template, context)

def _loan(year=datetime.now().year, month=datetime.now().month, yearly=False):
    if yearly == True:
        loans_rec = LoanPayment.objects.filter(delete_status = False, date_created__year = year)
        loans_issued = LoansIssue.objects.filter(delete_status = False, date_created__year = year)
    else:
        loans_rec = LoanPayment.objects.filter(delete_status = False, date_created__year = year,
                date_created__month = month)
        loans_issued = LoansIssue.objects.filter(delete_status = False, date_created__year = year,
                date_created__month = month)
    return {'loans_rec': loans_rec, 'loans_issued': loans_issued}

def loan(request):
    template = 'reports/loans.html'

    if request.method == 'POST':
        month = request.POST.get('month')
        year = request.POST.get('year')
        loan = _loan(year=year,month=month)
    else:
        loan = _loan()



    context = {
            'items_loans': loan.get("loans_rec","none"),
            'issued_items_loans': loan.get("loans_issued","none"),
            'title_loans': 'Loans',
            }

    return render(request, template, context)

def _capital(year=datetime.now().year, month=datetime.now().month,yearly=False):

    if yearly == True:
        shares_buy = ShareBuy.objects.filter(delete_status = False, date_created__year = year)
        shares_sell = ShareSell.objects.filter(delete_status = False, date_created__year = year)

        savings_deposit = SavingDeposit.objects.filter(delete_status = False, date_created__year = year)
        savings_withdrawal = SavingWithdrawal.objects.filter(delete_status = False, date_created__year = year)

        loan_payment = LoanPayment.objects.filter(delete_status = False, date_created__year = year)
        loans_issued = LoansIssue.objects.filter(delete_status = False, date_created__year = year)
    else:
        shares_buy = ShareBuy.objects.filter(delete_status = False, date_created__year = year,
                date_created__month = month)
        shares_sell = ShareSell.objects.filter(delete_status = False, date_created__year = year,
                date_created__month = month)

        savings_deposit = SavingDeposit.objects.filter(delete_status = False, date_created__year = year,
                date_created__month = month)
        savings_withdrawal = SavingWithdrawal.objects.filter(delete_status = False, date_created__year = year,
                date_created__month = month)

        loan_payment = LoanPayment.objects.filter(delete_status = False, date_created__year = year,
                date_created__month = month)
        loans_issued = LoansIssue.objects.filter(delete_status = False, date_created__year = year,
                date_created__month = month)

    shares_buy_sum = shares_buy.aggregate(Sum('number'))['number__sum']
    shares_sell_sum = shares_sell.aggregate(Sum('number'))['number__sum']

    savings_deposit_sum = savings_deposit.aggregate(Sum('amount'))['amount__sum']
    savings_withdrawal_sum= savings_withdrawal.aggregate(Sum('amount'))['amount__sum']

    loan_payment_sum= loan_payment.aggregate(Sum('principal'))['principal__sum']
    loans_issued_sum = loans_issued.aggregate(Sum('principal'))['principal__sum']

    return {'shares_buy_sum': shares_buy_sum, 'shares_sell_sum': shares_sell_sum,
	'savings_deposit_sum': savings_deposit_sum, 'savings_withdrawal_sum':savings_withdrawal_sum,
	'loan_payment_sum': loan_payment_sum,'loans_issued_sum': loans_issued_sum,
  	 }



def capital(request):
    template = 'reports/capital.html'

    if request.method == 'POST':
        month = request.POST.get('month')
        year = request.POST.get('year')
        capital = _capital(year=year,month=month)
    else:
        capital = _capital()

    pre_context = {
                0: capital.get('shares_buy_sum'),
                1: capital.get('savings_deposit_sum'),
                2: capital.get('loan_payment_sum'),
                3: capital.get('shares_sell_sum'),
                4: capital.get('savings_withdrawal_sum'),
                5: capital.get('loans_issued_sum'),
                }

    context = {
            'shares_buy_sum_capital': pre_context[0],
            'savings_deposit_sum_capital': pre_context[1],
            'loan_payment_sum_capital': pre_context[2],
            'shares_sell_sum_capital': pre_context[3],
            'savings_withdrawal_sum_capital': pre_context[4],
            'loans_issued_sum_capital': pre_context[5],
            'total_capital_additions': total_capital([0,1,2], pre_context),
            'total_capital_deductions': total_capital([3,4,5], pre_context),
            'title_capital': 'Capital',
            }

    return render (request, template, context)

def monthly(request):
    template = 'reports/monthly.html'

    if request.method == 'POST':
        month = request.POST.get('month')
        year = request.POST.get('year')
        loan = _loan(year=year,month=month)
        capital = _capital(year=year,month=month)
        incomes = _income(year=year,month=month)
        expenses = _expense(year=year,month=month)
    else:
        loan = _loan()
        capital = _capital()
        incomes = _income()
        expenses = _expense()

    pre_context = {
            0: capital.get('shares_buy_sum'),
            1: capital.get('savings_deposit_sum'),
            2: capital.get('loan_payment_sum'),
            3: capital.get('shares_sell_sum'),
            4: capital.get('savings_withdrawal_sum'),
            5: capital.get('loans_issued_sum'),
            6: incomes,
            7: incomes.aggregate(Sum('amount'))['amount__sum'],
            8: expenses,
            9: expenses.aggregate(Sum('amount'))['amount__sum'],
            10: loan.get('loans_rec'),
            11: loan.get('loans_issued'),
        }

    context = {
        'shares_buy_sum_capital': pre_context[0],
        'savings_deposit_sum_capital': pre_context[1],
        'loan_payment_sum_capital': pre_context[2],
        'shares_sell_sum_capital': pre_context[3],
        'savings_withdrawal_sum_capital': pre_context[4],
        'loans_issued_sum_capital': pre_context[5],
        'total_capital_additions': total_capital([0,1,2], pre_context),
        'total_capital_deductions': total_capital([3,4,5], pre_context),
        'items_income': pre_context[6],
        'total_income': pre_context[7],
        'items_expenses': pre_context[8],
        'total_expense': pre_context[9],
        'items_loans': pre_context[10],
        'issued_items_loans': pre_context[11],
        'title_yearly': 'Monthly',
        'title_income': 'Income',
        'title_expenses': 'Expense',
        'title_loans': 'Loans',
        'title_capital': 'Capital',
        }

    return render(request, template, context)

def yearly(request):
    template = 'reports/yearly.html'

    if request.method == 'POST':
        year = request.POST.get('year')
        loan = _loan(year=year,yearly=True)
        capital = _capital(year=year,yearly=True)
        incomes = _income(year=year,yearly=True)
        expenses = _expense(year=year,yearly=True)
    else:
        loan = _loan(yearly=True)
        capital = _capital(yearly=True)
        incomes = _income(yearly=True)
        expenses = _expense(yearly=True)

    pre_context = {
            0: capital.get('shares_buy_sum'),
            1: capital.get('savings_deposit_sum'),
            2: capital.get('loan_payment_sum'),
            3: capital.get('shares_sell_sum'),
            4: capital.get('savings_withdrawal_sum'),
            5: capital.get('loans_issued_sum'),
            6: incomes,
            7: incomes.aggregate(Sum('amount'))['amount__sum'],
            8: expenses,
            9: expenses.aggregate(Sum('amount'))['amount__sum'],
            10: loan.get('loans_rec'),
            11: loan.get('loans_issued'),
        }

    context = {
        'shares_buy_sum_capital': pre_context[0],
        'savings_deposit_sum_capital': pre_context[1],
        'loan_payment_sum_capital': pre_context[2],
        'shares_sell_sum_capital': pre_context[3],
        'savings_withdrawal_sum_capital': pre_context[4],
        'loans_issued_sum_capital': pre_context[5],
        'total_capital_additions': total_capital([0,1,2], pre_context),
        'total_capital_deductions': total_capital([3,4,5], pre_context),
        'items_income': pre_context[6],
        'total_income': pre_context[7],
        'items_expenses': pre_context[8],
        'total_expense': pre_context[9],
        'items_loans': pre_context[10],
        'issued_items_loans': pre_context[11],
        'title_yearly': 'Monthly',
        'title_income': 'Income',
        'title_expenses': 'Expense',
        'title_loans': 'Loans',
        'title_capital': 'Capital',
        }

    return render(request, template, context)
