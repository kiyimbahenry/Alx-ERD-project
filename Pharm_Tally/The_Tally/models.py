from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
from datetime import date

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def drug_count(self):
        return self.drug_set.count()

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def drug_count(self):
        return self.drug_set.count()

class Drug(models.Model):
    TYPE_CHOICES = [
        ('retail', 'Retail'),
        ('wholesale', 'Wholesale'),
    ]
    
    DOSAGE_CHOICES = [
        ('tab', 'Tablet'),
        ('spr', 'Spray'),
        ('kit', 'Kit'),
        ('cap', 'Capsule'),
        ('syr', 'Syrup'),
        ('inj', 'Injection'),
        ('cre', 'Cream'),
        ('oin', 'Ointment'),
        ('oth', 'Other'),
    ]
    
    # Basic Information
    generic_name = models.CharField(max_length=500, verbose_name="Generic Name")
    brand_name = models.CharField(max_length=200, verbose_name="Brand Name")
    dosage = models.CharField(max_length=10, choices=DOSAGE_CHOICES, default='tab', verbose_name="Dosage Form")
    description = models.TextField(blank=True, verbose_name="Description/Strength")
    
    # Stock Information
    stock_qty = models.IntegerField(default=0, verbose_name="Stock Quantity")
    min_qty = models.IntegerField(default=10, verbose_name="Minimum Quantity")
    
    # Batch and Expiry
    batch = models.CharField(max_length=100, verbose_name="Batch Number")
    expiry = models.DateField(verbose_name="Expiry Date")
    
    # Pricing
    cost_price = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        verbose_name="Cost Price",
        default=0.00
    )
    selling_price = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        verbose_name="Selling Price",
        default=0.00
    )
    
    # Relationships
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Category")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Supplier")
    drug_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='retail', verbose_name="Type")
    
    # Additional Information
    manufacturer = models.CharField(max_length=200, blank=True, verbose_name="Manufacturer")
    location = models.CharField(max_length=100, blank=True, verbose_name="Storage Location")
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name="Active")
    is_dead_stock = models.BooleanField(default=False, verbose_name="Dead Stock")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        ordering = ['generic_name', 'brand_name']
        verbose_name = "Drug"
        verbose_name_plural = "Drugs"
    
    def __str__(self):
        return f"{self.brand_name} - {self.generic_name[:30]}"
    
    def save(self, *args, **kwargs):
        # Auto-calculate selling price if not set (1.5x cost price)
        if self.selling_price == 0 and self.cost_price > 0:
            self.selling_price = self.cost_price * Decimal('1.5')
        super().save(*args, **kwargs)
    
    @property
    def stock_status(self):
        if self.stock_qty <= 0:
            return "Out of Stock"
        elif self.stock_qty <= self.min_qty:
            return "Low Stock"
        else:
            return "In Stock"
    
    @property
    def stock_status_color(self):
        if self.stock_qty <= 0:
            return "danger"
        elif self.stock_qty <= self.min_qty:
            return "warning"
        else:
            return "success"
    
    @property
    def expiry_status(self):
        if not self.expiry:
            return "No Expiry"
        
        today = date.today()
        days_to_expiry = (self.expiry - today).days
        
        if days_to_expiry < 0:
            return "Expired"
        elif days_to_expiry <= 30:
            return "Expiring Soon"
        elif days_to_expiry <= 90:
            return "Near Expiry"
        else:
            return "Valid"
    
    @property
    def expiry_status_color(self):
        if not self.expiry:
            return "secondary"
        
        today = date.today()
        days_to_expiry = (self.expiry - today).days
        
        if days_to_expiry < 0:
            return "danger"
        elif days_to_expiry <= 30:
            return "warning"
        elif days_to_expiry <= 90:
            return "info"
        else:
            return "success"
