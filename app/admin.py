from django.contrib import admin
from . import models

# Register your models here.

admin.site.register([models.Client, models.Product, models.Sales, models.Salesman, models.Registered_Users])