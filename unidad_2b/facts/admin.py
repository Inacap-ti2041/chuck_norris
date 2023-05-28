from django.contrib import admin

from .models import Fact


class FactAdmin(admin.ModelAdmin):
    list_display = ('fact', 'created_at', 'updated_at')


admin.site.register(Fact, FactAdmin)
