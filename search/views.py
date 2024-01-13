from django.shortcuts import render
from members.models import Member
from loans.models import LoanIssue
from django.db.models import Q
# Create your views here.

def search(request):
    template='search/search.html'

    return render(request, template)

def member_result(request):
    template='search/search.html'

    query = request.GET.get('mq')

    results = Member.objects.filter(Q(mem_number__iexact=query) | Q(first_name__icontains=query) |
            Q(last_name__icontains=query) | Q(address__iexact=query) | Q(contact__iexact=query))

    context = {
        'results': results,
        'title': 'members',
    }

    return render(request, template, context)

def loan_result(request):
    template='search/search.html'

    query = request.GET.get('lq')

    results = LoanIssue.objects.filter(Q(loan_num__iexact=query) | Q(principal__iexact=query))

    context = {
        'results': results,
        'title': 'loans',
    }

    return render(request, template, context)
