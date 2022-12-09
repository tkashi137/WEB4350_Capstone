from django import forms
from .models import Category, Label, Transaction
from django.forms import ModelForm


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': "form-control",
                'id': 'name'
            }),
            'type': forms.Select(attrs={
                'class': "form-control",
                'id': 'type'
            })
        }


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name', 'category', 'amount_planned', 'amount_received', 'due_date', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': "form-control",
                'id': 'name'
            }),
            'category': forms.Select(attrs={
                'class': "form-control",
                'id': 'category'
            }),
            'amount_planned': forms.NumberInput(attrs={
                'class': "form-control",
                'id': 'planned'
            }),
            'amount_received': forms.NumberInput(attrs={
                'class': "form-control",
                'id': 'received'
            }),
            'due_date': forms.NumberInput(attrs={
                'class': "form-control",
                'type': 'date',
                'id': 'date'
            }),
            'notes': forms.Textarea(attrs={
                'class': "form-control",
                'id': 'notes',
                'rows': 3
            })
        }


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['description', 'type', 'label', 'amount', 'date']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': "form-control",
                'id': "desc",
                'rows': 3
            }),
            'type': forms.Select(attrs={
                'class': "form-control",
                'id': "type"
            }),
            'label': forms.Select(attrs={
                'class': "form-control",
                'id': 'label'
            }),
            'amount': forms.NumberInput(attrs={
                'class': "form-control",
                'placeholder': "$00.00",
                'id': 'amount'
            }),
            'date': forms.NumberInput(attrs={
                'class': "form-control",
                'type': 'date',
                'id': 'date'
            }),
        }
