from django.contrib import admin
from .models import *
from .forms import *
from django.utils.html import format_html
from django.urls import reverse

# Register your models here.

# nếu đưa dữ liệu ở cách 1 sẽ không hiện chi tiết như cách 2
# nên đưa dữ liệu lên trang admin bằng cách 2 sẽ chi tiết hơn cách 1


# admin.site.register(Customer)
@admin.register(Customer)
class CusatomerModelAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "name", "address", "state"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


# admin.site.register(Product)
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    # form = ProductForm
    list_display = [
        "id",
        "title",
        "selling_price",
        "discounted_price",
        "description",
        "brand",
        "category",
        "product_image",
    ]


# admin.site.register(Cart)
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "product", "quantity"]


# admin.site.register(OderPlaced)
@admin.register(OderPlaced)
class OderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "customer", "customer_info", "product", "quantity", "ordered_date", "status"]

    def customer_info(self, obj):
        link = reverse("admin:app_customer_change", args=[obj.customer.pk])
        return format_html('<a> href="{}">{}<a>', link, obj.customer.name)
    
    def product_info(self, obj):
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a> href="{}">{}<a>', link, obj.product.name)