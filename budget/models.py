from django.db import models
from django.contrib.auth.models import User

# Create your models here


class Category(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    CATEGORY_TYPE_CHOICES = [
        ("INCOME", "Income"),
        ("EXPENSE", "Expense")
    ]
    type = models.CharField(max_length=8, choices=CATEGORY_TYPE_CHOICES, default="EXPENSE")


class Label(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount_planned = models.DecimalField(decimal_places=2, max_digits=7, blank=True, null=True)
    amount_received = models.DecimalField(decimal_places=2, max_digits=7, blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)


class Transaction(models.Model):
    def __str__(self):
        return "%s %s" % (self.description, self.date)

    description = models.TextField(blank=True, null=True)
    TRANSACTION_TYPE_CHOICES = [
        ("INCOME", "Income"),
        ("EXPENSE", "Expense")
    ]
    type = models.CharField(max_length=8, choices=TRANSACTION_TYPE_CHOICES, default="EXPENSE")
    label = models.ForeignKey(Label, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    date = models.DateTimeField()
