from django.db import models

class Product(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    # ⚡ TWO-TIER ARCHITECTURE
    category = models.CharField(max_length=100)      # e.g., "Women Wear"
    subcategory = models.CharField(max_length=100)   # e.g., "Saree"
    
    def __str__(self):
        return self.name

    @property
    def inventory_value(self):
        return self.price * self.quantity

# 📨 NEW: For capturing client tickets sent through contact.html
class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.email}"

# 🏷️ NEW: For making your about.html page feature grids completely dynamic
class AboutFeature(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title