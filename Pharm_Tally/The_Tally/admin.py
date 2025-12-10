from django.contrib import admin
from django.utils.html import format_html
from .models import Drug, Category, Supplier

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'phone', 'email')
    search_fields = ('name', 'contact_person')

@admin.register(Drug)
class DrugAdmin(admin.ModelAdmin):
    list_display = (
        'brand_name',
        'generic_name_short',
        'batch',
        'stock_qty',
        'min_qty',
        'expiry',
        'selling_price_display',
        'is_active'
    )
    
    list_filter = ('is_active', 'drug_type', 'category')
    search_fields = ('brand_name', 'generic_name', 'batch')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('generic_name', 'brand_name', 'description')
        }),
        ('Stock Information', {
            'fields': ('stock_qty', 'min_qty', 'dosage')
        }),
        ('Pricing', {
            'fields': ('cost_price', 'selling_price')
        }),
        ('Batch Information', {
            'fields': ('batch', 'expiry', 'manufacturer')
        }),
        ('Categorization', {
            'fields': ('category', 'supplier', 'drug_type')
        }),
        ('Status', {
            'fields': ('is_active', 'is_dead_stock', 'location')
        }),
    )
    
    def generic_name_short(self, obj):
        return obj.generic_name[:50] + '...' if len(obj.generic_name) > 50 else obj.generic_name
    generic_name_short.short_description = 'Generic Name'
    
    def selling_price_display(self, obj):
        return format_html(
            '<span style="color: green; font-weight: bold;">Ksh {:.2f}</span>',
            obj.selling_price
        )
    selling_price_display.short_description = 'Selling Price'
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

# Customize admin site
admin.site.site_header = "The_Tally - Drug Inventory"
admin.site.site_title = "The_Tally Admin"
admin.site.index_title = "Dashboard"
