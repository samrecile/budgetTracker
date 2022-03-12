from django.contrib import admin
from main.models import daily, recurring, asset, liability, Profile

# Register your models here.
admin.site.register(daily)
admin.site.register(recurring)
admin.site.register(liability)
admin.site.register(asset)
admin.site.register(Profile)

class modelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

