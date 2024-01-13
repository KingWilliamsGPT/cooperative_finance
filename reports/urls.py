from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import report,income,expense,loan,capital,monthly,yearly
app_name = 'reports'
urlpatterns = [
    path('', login_required(report), name='reports'),
    path('income', login_required(income), name='income'),
    path('expense', login_required(expense), name='expense'),
    path('loans', login_required(loan), name='loan'),
    path('capital', login_required(capital), name='capital'),
    path('monthly', login_required(monthly), name='monthly'),
    path('yearly', login_required(yearly), name='yearly'),
]
