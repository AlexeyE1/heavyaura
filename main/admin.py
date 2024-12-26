from django.contrib import admin
from .models import Product, Category, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class ProductImageInLine(admin.TabularInline):
    model = ProductImage
    extra = 5



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'price', 'available',
                    'created', 'updated', 'discount')
    list_filter = ('available', 'created', 'updated')
    list_editable = ('price', 'available', 'discount')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInLine]
    