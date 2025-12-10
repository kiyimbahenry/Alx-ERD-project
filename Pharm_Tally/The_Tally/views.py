from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Q
from datetime import date, timedelta
from .models import Drug

def is_admin(user):
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Admin dashboard view with statistics and drug listing"""
    
    # Get all active drugs
    drugs = Drug.objects.filter(is_active=True).select_related('category', 'supplier')
    
    # Calculate statistics
    total_drugs = drugs.count()
    
    # Calculate total inventory value
    total_inventory_cost = 0
    total_inventory_sale = 0
    
    for drug in drugs:
        total_inventory_cost += float(drug.stock_qty) * float(drug.cost_price)
        total_inventory_sale += float(drug.stock_qty) * float(drug.selling_price)
    
    # Low stock count
    low_stock_count = drugs.filter(
        stock_qty__gt=0,
        stock_qty__lte=models.F('min_qty')
    ).count()
    
    # Expiring soon count (within 30 days)
    today = date.today()
    thirty_days_later = today + timedelta(days=30)
    expiring_soon_count = drugs.filter(
        expiry__range=[today, thirty_days_later]
    ).count()
    
    # Count by status
    active_drugs = drugs.filter(is_active=True).count()
    inactive_drugs = Drug.objects.filter(is_active=False).count()
    
    context = {
        'drugs': drugs,
        'total_drugs': total_drugs,
        'total_cost_value': total_inventory_cost,
        'total_sale_value': total_inventory_sale,
        'low_stock_count': low_stock_count,
        'expiring_soon_count': expiring_soon_count,
        'active_drugs': active_drugs,
        'inactive_drugs': inactive_drugs,
    }
    
    return render(request, 'admin_dashboard.html', context)

# Add missing import at the top
from django.db import models
