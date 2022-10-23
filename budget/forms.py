from django import forms
from .models import Category, Label, Transaction
from django.forms import ModelForm


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type']


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name', 'category', 'amount_planned', 'amount_received', 'due_date', 'notes']


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['description', 'type', 'label', 'amount', 'date']
