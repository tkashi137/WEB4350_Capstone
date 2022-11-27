import traceback

from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

# Create your models here


# added default categories for users
class Category(models.Model):
    def __str__(self):
        return self.name
    CATEGORY_INCOME = "INCOME"
    CATEGORY_EXPENSE = "EXPENSE"
    DEFAULT_CATEGORIES = [
        {"name": 'Housing', "type": CATEGORY_EXPENSE},
        {"name": 'Food', "type": CATEGORY_EXPENSE},
        {"name": 'Transportation', "type": CATEGORY_EXPENSE},
        {"name": 'Health/Medical', "type": CATEGORY_EXPENSE},
        {"name": 'Personal', "type": CATEGORY_EXPENSE},
        {"name": 'Entertainment', "type": CATEGORY_EXPENSE},
        {"name": 'Gifts', "type": CATEGORY_EXPENSE},
        {"name": 'Other Expense', "type": CATEGORY_EXPENSE},
        {"name": 'Utilities', "type": CATEGORY_EXPENSE},
        {"name": 'Debt', "type": CATEGORY_EXPENSE},
        {"name": 'Savings', "type": CATEGORY_EXPENSE},
        {"name": 'Paycheck', "type": CATEGORY_INCOME},
        {"name": 'Bonus', "type": CATEGORY_INCOME},
        {"name": 'Interest', "type": CATEGORY_INCOME},
        {"name": 'Other Income', "type": CATEGORY_INCOME},
    ]

    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    CATEGORY_TYPE_CHOICES = [
        (CATEGORY_INCOME, "Income"),
        (CATEGORY_EXPENSE, "Expense")
    ]

    type = models.CharField(max_length=8, choices=CATEGORY_TYPE_CHOICES, default=CATEGORY_EXPENSE)

    @staticmethod
    def create_default_categories(user):
        for category in Category.DEFAULT_CATEGORIES:
            Category.objects.create(user=user, **category)


# Label model
class Label(models.Model):
    DEFAULT_LABELS = [
        {"name": 'Mortage Payment', "category": 'Housing', "amount_planned": Decimal("0.0"),
        "amount_received": Decimal("0.0"), "due_date": None, "notes": 'enter notes here'},
        {"name": 'Rent', "category": 'Housing', "amount_planned": Decimal("0.0"),
        "amount_received": Decimal("0.0"), "due_date": None, "notes": 'enter notes here'},
        {"name": 'Eating Out', "category": 'Food', "amount_planned": Decimal("0.0"),
        "amount_received": Decimal("0.0"), "due_date": None, "notes": 'enter notes here'},
        {"name": 'Grocery', "category": 'Food', "amount_planned": Decimal("0.0"),
        "amount_received": Decimal("0.0"), "due_date": None, "notes": 'enter notes here'},
        {"name": 'Fuel/Gas', "category": 'Transportation', "amount_planned": Decimal("0.0"),
        "amount_received": Decimal("0.0"), "due_date": None, "notes": 'enter notes here'},
        {"name": 'Auto Insurance', "category": 'Transportation', "amount_planned": Decimal("0.0"),
        "amount_received": Decimal("0.0"), "due_date": None, "notes": 'enter notes here'},
        {"name": 'Dr. Visits', "category": 'Health/Medical', "amount_planned": Decimal("0.0"),
        "amount_received": Decimal("0.0"), "due_date": None, "notes": 'enter notes here'},
        {"name": 'Gym Membership', "category": 'Health/Medical', "amount_planned": Decimal("0.0"),
        "amount_received": Decimal("0.0"), "due_date": None, "notes": 'enter notes here'},
        {"name": 'Personal', "category": 'Personal', "amount_planned": Decimal("0.0"),
        "amount_received": Decimal("0.0"), "due_date": None, "notes": 'enter notes here'},
        {"name": 'Movies', "category": 'Entertainment', "amount_planned": Decimal("0.0"),
        "amount_received": Decimal("0.0"), "due_date": None, "notes": 'enter notes here'},
        {"name": 'Road Trips', "category": 'Entertainment', "amount_planned": Decimal("0.0"),
        "amount_received": Decimal("0.0"), "due_date": None, "notes": 'enter notes here'},
        {"name": 'Holiday', "category": 'Gifts', "amount_planned": Decimal("0.0"),
        "amount_received": Decimal("0.0"), "due_date": None, "notes": 'enter notes here'},
        {"name": 'Birthday', "category": 'Gifts', "amount_planned": Decimal("0.0"),
        "amount_received": Decimal("0.0"), "due_date": None, "notes": 'enter notes here'},
        {"name": 'OtherExp', "category": 'Other Expense', "amount_planned": Decimal("0.0"),
        "amount_received": Decimal("0.0"), "due_date": None, "notes": 'enter notes here'},
        {"name": 'Gas', "category": 'Utilities', "amount_planned": Decimal("0.0"),
        "amount_received": Decimal("0.0"), "due_date": None, "notes": 'enter notes here'},
        {"name": 'Electric', "category": 'Utilities', "amount_planned": Decimal("0.0"),
        "amount_received": Decimal("0.0"), "due_date": None, "notes": 'enter notes here'},
        {"name": 'Internet', "category": 'Utilities', "amount_planned": Decimal("0.0"),
        "amount_received": Decimal("0.0"), "due_date": None, "notes": 'enter notes here'},
        {"name": 'Auto Paymnet', "category": 'Debt', "amount_planned": Decimal("0.0"),
        "amount_received": Decimal("0.0"), "due_date": None, "notes": 'enter notes here'},
        {"name": 'Credit Card', "category": 'Debt', "amount_planned": Decimal("0.0"),
        "amount_received": Decimal("0.0"), "due_date": None, "notes": 'enter notes here'},
        {"name": 'Vacation', "category": 'Savings', "amount_planned": Decimal("0.0"),
        "amount_received": Decimal("0.0"), "due_date": None, "notes": 'enter notes here'},
        {"name": 'Emergency Fund', "category": 'Savings', "amount_planned": Decimal("0.0"),
        "amount_received": Decimal("0.0"), "due_date": None, "notes": 'enter notes here'},
        {"name": 'Full Time Job', "category": 'Paycheck', "amount_planned": Decimal("0.0"),
        "amount_received": Decimal("0.0"), "due_date": None, "notes": 'enter notes here'},
        {"name": 'Side Gig', "category": 'Paycheck', "amount_planned": Decimal("0.0"),
        "amount_received": Decimal("0.0"), "due_date": None, "notes": 'enter notes here'},
        {"name": 'Bonus', "category": 'Bonus', "amount_Interestplanned": Decimal("0.0"),
        "amount_received": Decimal("0.0"), "due_date": None, "notes": 'enter notes here'},
        {"name": 'Interest', "category": 'Interest', "amount_planned": Decimal("0.0"),
        "amount_received": Decimal("0.0"), "due_date": None, "notes": 'enter notes here'},
        {"name": 'OtherInc', "category": 'Other Income', "amount_planned": Decimal("0.0"),
        "amount_received": Decimal("0.0"), "due_date": None, "notes": 'enter notes here'},
    ]

    def __str__(self):
        return self.name

    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(Category, related_name='labels', on_delete=models.CASCADE)
    amount_planned = models.DecimalField(decimal_places=2, max_digits=7, blank=True, null=True)
    amount_received = models.DecimalField(decimal_places=2, max_digits=7, blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    @staticmethod
    def create_default_labels(user):
        for label in Label.DEFAULT_LABELS:
            category_name = label.pop("category")
            try:
                category = Category.objects.get(name=category_name, user=user)
                Label.objects.create(user=user, **label, category=category)

            except Exception as e:
                print(f'Label creation failed for {user} & {category_name}')
                traceback.print_exc()


class Transaction(models.Model):
    def __str__(self):
        return "%s %s" % (self.description, self.date)

    description = models.TextField(blank=True, null=True)
    TRANSACTION_TYPE_CHOICES = [
        ("INCOME", "Income"),
        ("EXPENSE", "Expense")
    ]
    type = models.CharField(max_length=8, choices=TRANSACTION_TYPE_CHOICES, default="EXPENSE")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    label = models.ForeignKey(Label, related_name='transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    date = models.DateTimeField()
