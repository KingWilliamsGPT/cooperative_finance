from django.urls import reverse

from . import models
from django.contrib.auth import get_user_model

User = get_user_model()




def send_notifications(users, title, content, redirect_ur=''):
    notifications_list = [
        models.Notification(user=user, content=content, title=title, redirect_url=redirect_ur) for user in users
    ]
    notifications = models.Notification.objects.bulk_create(notifications_list)
    return notifications

def _get_new_status(status):
    # just returns the oposite status
    t=['deactivated', 'activated']
    return t[t.index(status.lower())-1]

def _get_acct_type(model_instance):
    if model_instance.__class__.__name__[-7:] != 'Account':
        raise TypeError(f'wrong model was passed expected SomeKindOfAccount not {model_instance.__class__.__name__}')
    acct_type = model_instance.__class__.__name__[:-7]
    if acct_type in ('Saving', 'Share'):
        acct_type += 's'
    return f'{acct_type} Account'


class AdminNotificationViewHelper:

    @staticmethod
    def create_deposite(request, deposite, url='', users=None):
        title = 'savings deposit'
        content = f'{request.user} approved a deposite of {deposite.amount} into {deposite.account.owner.full_name()}\'s savings account'
        default_url = reverse('members:member_detail', args=[deposite.account.owner.mem_number])
        users = users or User.objects.all()
        send_notifications(users, title, content, url or default_url)

    @staticmethod
    def create_withdraw(request, withdraw, url='', users=None):
        title = 'savings withdrawal'
        content = f'A withdraw of {withdraw.amount} to {withdraw.account.owner.full_name()} account has been approved by {request.user}'
        default_url = reverse('members:member_detail', args=[withdraw.account.owner.mem_number])
        users = users or User.objects.all()
        send_notifications(users, title, content, url or default_url)
    
    @staticmethod
    def de_or_activate(request, account, url='', users=None):
        admin_user = request.user
        owner = account.owner
        users = users or User.objects.all()
        default_url = reverse('members:member_detail', args=[owner.mem_number])

        new_status = account.status
        acct_type = _get_acct_type(account)
        title = f'Account {new_status}'.title()
        content = f'{owner} {acct_type} was {new_status} by {admin_user}'
        send_notifications(users, title, content, url or default_url)

    @staticmethod
    def created_member(request, member, url='', users=None):
        admin_user = request.user
        owner = member
        users = users or User.objects.all()
        default_url = reverse('members:member_detail', args=[owner.mem_number])

        title = "New Member"
        content = f'The new member {owner.full_name()} was added by {admin_user}'
        send_notifications(users, title, content, url or default_url)
    
    @staticmethod
    def shares_buy_or_sell(request, share, url='', users=None):
        admin_user = request.user
        owner = share.account.owner
        users = users or User.objects.all()
        default_url = reverse('members:member_detail', args=[owner.mem_number])
        amount = share.number

        from shares.models import ShareBuy, ShareSell
        if isinstance(share, ShareBuy):
            verb = 'bought'
        else:
            verb = 'sold'
            
        title = f"shares {verb}"
        content = f"{owner.full_name()} just {verb} {amount} shares, approved by {admin_user}"
        send_notifications(users, title, content, url or default_url)

