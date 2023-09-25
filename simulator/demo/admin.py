from django.contrib import admin
from .models import Client


class ClientDisplay(admin.ModelAdmin):
    list_display = ("name", "company", "email")


admin.site.register(Client, ClientDisplay)

# Register your models here.
