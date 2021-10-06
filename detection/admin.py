from django.contrib import admin
from .models import Detection


# Register your models here.

class DateAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

admin.site.register(Detection, DateAdmin)
