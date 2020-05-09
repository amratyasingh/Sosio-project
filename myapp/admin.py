from django.contrib import admin

# Register your models here.
from myapp.models import Invoice

admin.site.register(Invoice)
