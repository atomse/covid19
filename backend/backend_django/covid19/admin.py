from django.contrib import admin
from .models import Covid19, Covid19Country, Covid19Latest, Covid19Date
# Register your models here.
admin.site.register(Covid19)
admin.site.register(Covid19Country)
admin.site.register(Covid19Latest)
admin.site.register(Covid19Date)