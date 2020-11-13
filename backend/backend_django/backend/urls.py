"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
import covid19.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/allCountries', covid19.views.all_countries),
    path('api/v1/allDate', covid19.views.all_date),
    path('api/v1/dateRange', covid19.views.date_range),
    path('api/v1/covid19', covid19.views.covid19),
    path('api/v1/covid19LatestNumbers', covid19.views.covid19_latest_numbers),
    path('control/update_covid19', covid19.views.update_covid19),
    path('user/login', covid19.views.user_login),
    path('user/info', covid19.views.user_info),
    path('user/logout', covid19.views.user_logout),
]
