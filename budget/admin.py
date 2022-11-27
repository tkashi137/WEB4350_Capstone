from django.contrib import admin
from .models import Category, Label, Transaction

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'user']
    list_filter = ['name', 'user']

@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ['name', 'user']
    list_filter = ['name', 'user']

@admin.register(Transaction)
class LabelAdmin(admin.ModelAdmin):
    list_display = ['description', 'user']
    list_filter = ['description', 'user']


