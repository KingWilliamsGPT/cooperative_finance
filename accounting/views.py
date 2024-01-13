from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import IncomeForm,ExpenseForm
from .models import Income,Expense


# Create your views here.

def income(request):
    template = 'accounting/form.html'

    transactions = Income.objects.filter(delete_status=False)

    form = IncomeForm(request.POST or None)

    if form.is_valid():
        income = form.save(commit=False)
        income.save()

    context = {
            'form': form,
            'title': 'Income',
            'transactions': transactions,
            }

    return render (request, template, context)

def expense(request):
    template = 'accounting/form.html'
    
    transactions = Expense.objects.filter(delete_status=False)

    form = ExpenseForm(request.POST or None)

    if form.is_valid():
        expense = form.save(commit=False)
        expense.save()

    context = {
            'form': form,
            'title': "Expense",
            'transactions': transactions,
            }
    
    return render (request, template, context)

def accounting(request):
    template = 'accounting/accounting.html'

    return render(request, template)

def income_delete(request, pk):
    template = 'accounting/income_delete.html'

    income = get_object_or_404(Income, pk=pk)

    if request.method == "POST":
        income.delete_status = True
        income.save()
        messages.success(request,
                        'You successfully deleted income_transaction of amount {} and type {} received from{}.'
                        .format(income.amount,income.income_type,income.received_from))
        previous = request.POST.get('previous', None)

        return redirect(previous)

    context = {
        'item': income,
        'type': "Income",
        }

    return render(request, template, context)

def expense_delete(request, pk):
    template = 'accounting/expense_delete.html'

    expense = get_object_or_404(Expense, pk=pk)

    if request.method == "POST":
        expense.delete_status = True
        expense.save()
        messages.success(request,
                        'You successfully deleted expense_transaction of amount {} and type {} payed to{}.'
                        .format(expense.amount,expense.expense_type,expense.payed_to))
        previous = request.POST.get('previous', None)

        return redirect(previous)

    context = {
        'item': expense,
        'type': "Expense",
        }

    return render(request, template, context)
