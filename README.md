📋 Project Overview
The_Tally is a comprehensive Drug Inventory Management System built with Django that helps pharmacies and healthcare facilities manage their drug inventory efficiently. The system provides a modern admin dashboard similar to commercial solutions like DrugTally2.

🚀 Current Status
Version: 1.0.0 (Development)
Last Updated: December 2023
Stage: MVP (Minimum Viable Product) Completed

✨ Features Implemented
✅ Completed Features
1. User Authentication & Authorization
Secure admin login/logout system

Role-based access control (Admin only)

Session management

2. Admin Dashboard
Modern sidebar navigation with all menu items

Statistics cards showing:

Stock Cost Value

Stock Sale Value

Low Stock Drugs

Expiring Soon Drugs

Quick action buttons for common tasks

Fully responsive design

3. Drug Inventory Management
Complete drug model with all required fields:

Generic Name

Brand Name

Dosage Form (Tablet, Spray, Kit, etc.)

Description/Strength

Stock Quantity

Minimum Quantity (reorder level)

Batch Number

Expiry Date

Cost Price

Selling Price (auto-calculated as 1.5× cost price)

Category (Pain killer, Cough and cold, etc.)

Type (Retail/Wholesale)

Supplier information

Manufacturer

Storage location

4. Supplier Management
Supplier information storage

Contact details management

Supplier-drug relationship tracking

5. Category Management
Drug categories (Pain killer, Anti-malarial, etc.)

Category-based filtering and organization

6. Data Visualization
Color-coded stock status (Green/Orange/Red)

Color-coded expiry status

Real-time inventory valuation

Low stock alerts

7. Search & Filtering
Search drugs by name, batch, or description

Filter by drug type (Retail/Wholesale)

Filter by stock status

Filter by expiry status

🔧 Technical Implementation
Backend (Django)
Django 4.2+

SQLite database (production-ready for PostgreSQL/MySQL)

Custom model methods for calculations

Automatic price calculations

Efficient database queries

Frontend
Bootstrap 5 for responsive design

Font Awesome icons

DataTables for enhanced table functionality

Custom CSS with modern gradient designs

Mobile-responsive layout

Admin Interface
Custom Django admin templates

Enhanced form validation

Batch operations

Export capabilities (planned)
📁 Project Structure
Pharm_Tally/
├── Pharm_Tally/           # Project settings
│   ├── settings.py       # Django settings
│   ├── urls.py          # URL configuration
│   └── wsgi.py
├── The_Tally/            # Main app
│   ├── models.py        # Database models
│   ├── views.py         # Business logic
│   ├── admin.py         # Admin configuration
│   ├── apps.py          # App configuration
│   └── migrations/      # Database migrations
├── templates/           # HTML templates
│   ├── admin_dashboard.html  # Main dashboard
│   ├── login.html           # Login page
│   └── admin/               # Custom admin templates
├── static/              # Static files (CSS, JS, images)
└── manage.py           # Django management script
