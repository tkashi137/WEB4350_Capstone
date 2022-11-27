from django import forms
from .models import Category, Label, Transaction
from django.forms import ModelForm


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': "form-control"
            }),
            'type': forms.Select(attrs={
                'class': "form-control"
            })
        }


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name', 'category', 'amount_planned', 'amount_received', 'due_date', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': "form-control"
            }),
            'category': forms.Select(attrs={
                'class': "form-control"
            }),
            'amount_planned': forms.NumberInput(attrs={
                'class': "form-control"
            }),
            'amount_received': forms.NumberInput(attrs={
                'class': "form-control"
            }),
            'due_date': forms.NumberInput(attrs={
                'class': "form-control",
                'type': 'date'
            }),
            'notes': forms.Textarea(attrs={
                'class': "form-control",
                'rows': 3
            })
        }


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['description', 'type', 'label', 'amount', 'date']
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 3,
                'class': "form-control"
            }),
            'type': forms.Select(attrs={
                'class': "form-control"
            }),
            'label': forms.Select(attrs={
                'class': "form-control"
            }),
            'amount': forms.NumberInput(attrs={
                'class': "form-control",
                'placeholder': "$00.00"
            }),
            'date': forms.NumberInput(attrs={
                'class': "form-control",
                'type': 'date'
            }),
        }
