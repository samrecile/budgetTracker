from django.contrib import admin
from main.models import daily, recurring, asset

# Register your models here.
admin.site.register(daily)
admin.site.register(recurring)
admin.site.register(asset)