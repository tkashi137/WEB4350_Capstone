from rest_framework import serializers
from .models import Category, Transaction, Label


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'user', 'type']


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'name', 'category', 'amount_planned', 'amount_received', 'due_date', 'notes']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'description', 'type', 'label', 'amount', 'date']
