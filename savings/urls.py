from django.urls import path
from django.contrib.auth.decorators import login_required


from .views import (saving_deposit,saving_withdrawal,
        saving_deposit_transactions,saving_withdrawal_transactions,
        saving_deposit_transaction,saving_withdrawal_transaction,
        saving_account,saving,
        saving_deposit_delete,saving_withdrawal_delete,
        get_saving_account)

app_name = 'savings'
urlpatterns = [
    path('', login_required(saving), name='saving'),
    path('get', login_required(get_saving_account), name='get_savings_account'),
    path('de|activate/', login_required(saving_account), name='de|activate'),
    path('deposit/', login_required(saving_deposit), name='deposit'),
    path('deposit/<int:pk>/', login_required(saving_deposit), name='depositpk'),
    path('deposit/<int:pk>/delete/', login_required(saving_deposit_delete), name='deposit_delete'),
    path('withdraw/', login_required(saving_withdrawal), name='withdraw'),
    path('withdraw/<int:pk>/', login_required(saving_withdrawal), name='withdrawpk'),
    path('withdraw/<int:pk>/delete/', login_required(saving_withdrawal_delete), name='withdraw_delete'),
    path('deposit/transactions/', login_required(saving_deposit_transactions), name='transactions'),
    path('withdraw/transactions/', login_required(saving_withdrawal_transactions), name='withdraw_transactions'),
    path('deposit/transaction/', login_required(saving_deposit_transaction), name='transaction'),
    path('withdraw/transaction/', login_required(saving_withdrawal_transaction), name='withdraw_transaction'),
]
