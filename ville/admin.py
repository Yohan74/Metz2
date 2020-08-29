from django.contrib import admin

from .models import Noms, Dates

# Register your models here.

# admin.site.register(Noms)
admin.site.register(Dates)

class NomAdmin(admin.ModelAdmin):
    list_display = ('selection', 'nom', 'slug')
    readonly_fields = ["creation" , "updated", ]

admin.site.register(Noms, NomAdmin)