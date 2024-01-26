"""cooperative_finance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path,include
from django.contrib.auth.decorators import login_required

import static_pages.views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_required(static_pages.views.home), name="home"),
    path('about/', static_pages.views.about, name="about"),
    path('contact/', static_pages.views.contact, name="contact"),
    path('tutorial/', static_pages.views.tutorial, name="tutorial"),
    path('savings/', include('savings.urls')),
    path('loans/', include('loans.urls')),
    path('shares/', include('shares.urls')),
    path('members/', include('members.urls')),
    path('reports/', include('reports.urls')),
    path('accounting/', include('accounting.urls')),
    path('search/', include('search.urls')),
    # notifications
    path('notifications/', include('notifications.urls')),
    # path('OneSignalSDK.js', TemplateView.as_view(template_name='OneSignalSDKWorker.js', content_type='application/javascript')),
]
