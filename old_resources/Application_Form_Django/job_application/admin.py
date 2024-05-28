from django.contrib import admin
from .models import Form


class FormAdmin(admin.ModelAdmin):
    list_display = ("first_name","last_name","email")
    search_fields = ("first_name", "last_name")
    list_filter = ("date","occupation")
    ordering = ("first_name", )
    # alphabetical ordering based on first name , for reverse write -first_name

    readonly_fields = ("occupation",)# admin cant change these



admin.site.register(Form,FormAdmin)