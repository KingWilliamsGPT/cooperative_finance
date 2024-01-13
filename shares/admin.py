from django.contrib import admin
from .models import (ShareAccount,ShareBuy,
        ShareSell,)

# Register your models here.

admin.site.register(ShareAccount)
admin.site.register(ShareBuy)
admin.site.register(ShareSell)



