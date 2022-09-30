
from django.contrib import admin
from .models import Products, Variation

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'catagory', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    
    
class Variationadmin(admin.ModelAdmin):
    list_display = ('product', 'variation_catagory', 'variation_value' , 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_catagory', 'variation_value')

admin.site.register(Products, ProductAdmin)
admin.site.register(Variation, Variationadmin)