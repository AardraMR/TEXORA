from django.shortcuts import render, redirect
from django.db.models import Count  
from django.contrib import messages  
from .models import Product, ContactMessage, AboutFeature  

def home(request):
    all_products = Product.objects.all()
    
    # Standard Core Metrics
    total_items = sum(p.quantity for p in all_products)
    low_stock_count = all_products.filter(quantity__lt=10).count()
    total_value = sum(p.inventory_value for p in all_products)
    
    # 📊 Category Chart Aggregation
    category_data = Product.objects.values('category').annotate(total_stock=Count('id'))
    chart_labels = [str(item['category']) for item in category_data]
    chart_counts = [int(item['total_stock']) for item in category_data]

    # 💎 UNIQUE FEATURE 1: Dead Stock Radar
    # Flags any textile line with more than 20 units sitting stagnant
    dead_stock_items = all_products.filter(quantity__gte=20)
    for item in dead_stock_items:
        # Dynamically calculates a 15% clearance sale markdown price
        item.clearance_price = round(float(item.price) * 0.85, 2)

    # 📈 NEW UNIQUE FEATURE 2: Seasonal Style Trend Indicator
    # Detects which category is in high demand based on lower remaining stock distribution
    fast_moving_category = "None"
    demand_status = "Stable"
    
    if all_products.exists():
        # Group products by category and collect their stock quantities
        category_stock_averages = {}
        for p in all_products:
            category_stock_averages[p.category] = category_stock_averages.get(p.category, []) + [p.quantity]
        
        # Find the category with the lowest average stock left (selling out the fastest)
        avg_stock_per_cat = {cat: sum(quantities)/len(quantities) for cat, quantities in category_stock_averages.items()}
        if avg_stock_per_cat:
            fast_moving_category = min(avg_stock_per_cat, key=avg_stock_per_cat.get)
            
            # Set a dynamic alert label based on how low the stock is getting
            if avg_stock_per_cat[fast_moving_category] < 10:
                demand_status = "🔥 Critical High Demand"
            else:
                demand_status = "⚡ Rising Trend"

    context = {
        'total_items': total_items,
        'low_stock_count': low_stock_count,
        'total_value': total_value,
        'chart_labels': chart_labels,   
        'chart_counts': chart_counts,
        'dead_stock_items': dead_stock_items,
        # Clean retail trend context fields passed down to home.html
        'fast_moving_category': fast_moving_category,
        'demand_status': demand_status,
    }
    return render(request, 'home.html', context)

def about(request):
    features = AboutFeature.objects.all()
    return render(request, 'about.html', {'features': features})

def products(request):
    all_products = Product.objects.all()
    return render(request, 'products.html', {'products': all_products})

def addproduct(request):
    if request.method == "POST":
        sku_code = request.POST.get('sku', '').strip()
        product_name = request.POST.get('name', '').strip()
        category_group = request.POST.get('category', 'Uncategorized').strip()
        subcategory_group = request.POST.get('subcategory', 'General').strip() 
        unit_price = request.POST.get('price') or '0.00'
        stock_quantity = request.POST.get('quantity') or '0'
        img_url = request.POST.get('image_url', '').strip() 

        # Form Validations
        if not sku_code:
            messages.error(request, "🔴 Submission Rejected: SKU Code field cannot be left empty.")
            return render(request, 'addproduct.html')
            
        if not product_name:
            messages.error(request, "🔴 Submission Rejected: Product Description Name cannot be left empty.")
            return render(request, 'addproduct.html')

        if Product.objects.filter(sku=sku_code).exists():
            messages.error(request, f"🔴 SKU Code '{sku_code}' already exists. Please assign a unique asset token.")
            return render(request, 'addproduct.html')

        if not img_url:
            img_url = "/static/images/multicolour.jpg"

        # Save to database row
        Product.objects.create(
            sku=sku_code,
            name=product_name,
            category=category_group,
            subcategory=subcategory_group,
            price=unit_price,
            quantity=stock_quantity,
            image=img_url
        )
        
        messages.success(request, f"🟢 Asset '{product_name}' successfully registered to inventory ledger!")
        return redirect('products')
        
    return render(request, 'addproduct.html')

def contact(request):
    if request.method == "POST":
        client_name = request.POST.get('name')
        client_email = request.POST.get('email')
        client_msg = request.POST.get('message')

        ContactMessage.objects.create(
            name=client_name,
            email=client_email,
            message=client_msg
        )
        messages.success(request, "📩 Message sent successfully! Our team will contact you shortly.")
        return redirect('contact')

    return render(request, 'contact.html')

def deleteproduct(request, sku_code):
    product_to_remove = Product.objects.filter(sku=sku_code).first()
    
    if product_to_remove:
        item_name = product_to_remove.name
        product_to_remove.delete() 
        messages.success(request, f"🗑️ Asset '{item_name}' has been safely purged from the registry.")
    else:
        messages.error(request, "🔴 Delete Failed: Target asset could not be found in current records.")
        
    return redirect('products')