from django.contrib import admin
from .models import Category, Label, Transaction

# Register your models here.

admin.site.register(Category)
admin.site.register(Label)
admin.site.register(Transaction)
