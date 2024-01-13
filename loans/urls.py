from django.urls import path
from django.contrib.auth.decorators import login_required


from .views import (loan_issue,loan_payment,
                    loan_issue_transactions,loan_payment_transactions,
                    loan_issue_transaction,loan_payment_transaction,
                    loan_approve,loan_account,loan,
                    get_loan,loan_issue_delete,
                    loan_payment_delete,get_loan_account)

app_name = 'loans'

urlpatterns = [
    path('', login_required(loan), name='loan'),
    path('get', login_required(get_loan_account), name='get_loan_account'),
    path('de|activate/', login_required(loan_account), name='de|activate'),
    path('pay/', login_required(loan_payment), name='pay'),
    path('pay/<int:pk>/', login_required(loan_payment), name='paypk'),
    path('pay/<int:pk>/delete', login_required(loan_payment_delete), name='payment_delete'),
    path('issue/', login_required(loan_issue), name='issue'),
    path('issue/<int:pk>/', login_required(loan_issue), name='issuepk'),
    path('issue/<int:pk>/delete', login_required(loan_issue_delete), name='issue_delete'),
    path('issue/get/', login_required(get_loan), name='get_loan'),
    path('issue/get/<int:pk>/', login_required(get_loan), name='get_loanpk'),
    path('issue/approve/', login_required(loan_approve), name='approve'),
    path('issue/approve/<int:loan_num>/', login_required(loan_approve), name='approveloan_num'),
    path('pay/transactions/', login_required(loan_payment_transactions), name='transactions'),
    path('issue/transactions/', login_required(loan_issue_transactions), name='issue_transactions'),
    path('pay/transaction/', login_required(loan_payment_transaction), name='transaction'),
    path('issue/transaction/', login_required(loan_issue_transaction), name='issue_transaction'),
]
