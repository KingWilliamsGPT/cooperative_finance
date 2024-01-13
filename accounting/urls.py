from django.urls import path
from django.contrib.auth.decorators import login_required


from .views import (income,expense,
                    accounting,income_delete,
                    expense_delete,
                    )

app_name = 'accounting'
urlpatterns = [
        path('', login_required(accounting), name="accounting"),
        path('income/', login_required(income), name="income"),
        path('expense/', login_required(expense), name="expense"),
        path('income/<int:pk>/delete/', login_required(income_delete), name="income_delete"),
        path('expense/<int:pk>/delete/', login_required(expense_delete), name="expense_delete"),
]
