from django.contrib import admin
from .models import Flag

class FlagAdmin(admin.ModelAdmin):
    list_display = ('name','image' )

admin.site.register(Flag, FlagAdmin)