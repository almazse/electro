from django.contrib import admin
from .models import Category, Brand, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class CategoryBrand(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Brand, CategoryBrand)


class CategoryProduct(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'old_price', 'rait', 'stock', 'available', 'created', 'updated']
    list_filter = ['rait', 'available', 'created', 'updated']
    list_editable = ['price', 'old_price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Product, CategoryProduct)
