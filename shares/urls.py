from django.urls import path
from django.contrib.auth.decorators import login_required


from .views import (share_account,share_buy,
        share_sell,share_buy_transactions,
        share_sell_transactions,share_buy_transaction,
        share_sell_transaction,share,
        share_buy_delete,share_sell_delete,
        get_share_account,)

app_name = 'shares'
urlpatterns = [
    path('', login_required(share), name='share'),
    path('get/', login_required(get_share_account), name='get_shares_account'),
    path('de|activate/', login_required(share_account), name='de|activate'),

    path('buy/', login_required(share_buy), name='buy'),
    path('buy/<int:pk>/', login_required(share_buy), name='buypk'),
    path('buy/<int:pk>/delete/', login_required(share_buy_delete), name='buy_delete'),

    path('sell/', login_required(share_sell), name='sell'),
    path('sell/<int:pk>/', login_required(share_sell), name='sellpk'),
    path('sell/<int:pk>/delete', login_required(share_sell_delete), name='sell_delete'),
    
    path('buy/transactions/', login_required(share_buy_transactions), name='transactions'),
    path('sell/transactions/', login_required(share_sell_transactions), name='sell_transactions'),
    path('buy/transaction/', login_required(share_buy_transaction), name='transaction'),
    path('sell/transaction/', login_required(share_sell_transaction), name='sell_transaction'),
]
