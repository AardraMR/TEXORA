from django.contrib import admin
from .models import Product, ContactMessage, AboutFeature

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_at')
    readonly_fields = ('name', 'email', 'message', 'submitted_at') # Keeps tickets secure/read-only

@admin.register(AboutFeature)
class AboutFeatureAdmin(admin.ModelAdmin):
    list_display = ('title',)