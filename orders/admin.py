from django.contrib import admin

from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "customer", "quantity", "size", "created_at", "order_status"]


admin.site.register(Order, OrderAdmin)
