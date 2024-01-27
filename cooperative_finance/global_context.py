# This is module is for context prepocessors
from django.conf import settings



def site_data(request):
    return {
        'APPLICATION_NAME': settings.APPLICATION_NAME,
    }