from collections import OrderedDict
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.db.models import Sum 
from datetime import date
from decimal import Decimal

# from rest_framework import viewsets
# from .serializers import CategorySerializer, LabelSerializer, TransactionSerializer
from .models import Category, Label, Transaction
from users.models import Profile, User
from django.contrib.auth.decorators import login_required
from .forms import CategoryForm, LabelForm, TransactionForm
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
import calendar
import datetime


# Create your views here.


def index(request):
    template = loader.get_template('budget/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def dashboard(request):
    user = request.user
    categories_list = Category.objects.filter(user=user) if user.is_authenticated else Label.objects.all()
    category_names = list(categories_list.values_list('name', flat=True))
    category_types = [x[0] for x in Category.CATEGORY_TYPE_CHOICES]
    # list(categories_list.values_list('type', flat=True))
    labels_list = Label.objects.filter(user=user) if user.is_authenticated else Label.objects.all()
    label_names = list(labels_list.values_list('name', flat=True))
    label_category = list(labels_list.values_list('category', flat=True))
    label_amountRec = list(labels_list.values_list('amount_received', flat=True))
    label_amountPlanned = list(labels_list.values_list('amount_planned', flat=True))
    transactions_list = Transaction.objects.filter(user=user) if user.is_authenticated else Label.objects.all()
    transaction_description = list(transactions_list.values_list('description', flat=True))
    transaction_type = list(transactions_list.values_list('type', flat=True))
    transaction_label = list(transactions_list.values_list('label', flat=True))
    transaction_amount = list (transactions_list.values_list('amount', flat=True))
    transaction_date = list(transactions_list.values_list('date', flat=True))

    # daily spending limit
    now = datetime.datetime.now()
    month_days = calendar.monthrange(now.year, now.month)[1]
    days_left = month_days - now.day
    funds_list = Profile.objects.filter(user=user).values('funds').get()
    funds = list(funds_list.values())[0]
    spending_limit = funds / days_left

    #amount planned, received, remaining by category
    labels = Label.objects.filter(user=user)
    sums = [] 
    sumLabels = []
    receivedSums = []
    for category in Category.objects.filter(user=user):
        cat_sum = labels.filter(category=category).aggregate(Sum('amount_planned'))
        # sums[category.name] = cat_sum
        sums.append(cat_sum)
        sumLabels.append(category.name)
     
    for category in Category.objects.filter(user=user):
        cat_Receivedsum = labels.filter(category=category).aggregate(Sum('amount_received'))
        # sums[category.name] = cat_sum
        receivedSums.append(cat_Receivedsum)

    # categories type chart
    categories = Category.objects.filter(user=user)
    category_type_sum = OrderedDict()
    for category in categories:
        if category.type not in category_type_sum:
            category_type_sum[category.type] = 0
        category_type_sum[category.type] += 1

    # transaction chart
    transactions = Transaction.objects.filter(user=user)
    transaction_amount_sum = OrderedDict()
    for transaction in transactions:
        if transaction.type not in transaction_amount_sum:
            transaction_amount_sum[transaction.type] = 0
        transaction_amount_sum[transaction.type] += transaction.amount

    template = loader.get_template('budget/dashboard.html')
    context = {
        'categories_list': categories_list,
        'category_names': category_names,
        'category_types': list(category_type_sum.keys()),
        'labels_list': labels_list,
        'label_names': label_names,
        'label_category': label_category,
        'label_amountRec': label_amountRec,
        'label_amountPlanned': label_amountPlanned,
        'transactions_list': transactions_list,
        'transaction_description': transaction_description,
        'transaction_type': transaction_type,
        'transaction_label': transaction_label,
        'transaction_amount': transaction_amount,
        'transaction_date': transaction_date,
        'categoryTypeSum': list(category_type_sum.values()),
        'transactionAmountSum': list(transaction_amount_sum.values()),
        'sums': sums,
        'sumLabels': sumLabels,
        'receivedSums': receivedSums,
        'now': now,
        'days_left': days_left,
        'spending_limit': spending_limit
    }
    return HttpResponse(template.render(context, request))


@login_required
def transactions(request):
    user = request.user
    transactions_list = Transaction.objects.filter(user=user) if user.is_authenticated else Transaction.objects.all()
    template = loader.get_template('budget/transactions.html')
    context = {
        'transactions_list': transactions_list,
    }
    return HttpResponse(template.render(context, request))


# class based form
class CreateTransaction(CreateView):
    form_class = TransactionForm
    template_name = 'budget/transaction-form.html'
    success_url = reverse_lazy("transactions")

    def form_valid(self, form):
        transaction_type = form.cleaned_data['type']
        if transaction_type == 'EXPENSE':
            user = self.request.user
            label_name = form.cleaned_data['label']
            received = Label.objects.filter(user=user, name=label_name).values('amount_received').get()
            amount_received = list(received.values())[0]
            form_amount = form.cleaned_data['amount']
            amount = form_amount + amount_received
            Label.objects.filter(user=user, name=label_name).update(amount_received=amount)
            funds_list = Profile.objects.filter(user=user).values('funds').get()
            funds = list(funds_list.values())[0]
            balance = funds - form_amount
            Profile.objects.filter(user=user).update(funds=balance)
            form.instance.user = self.request.user
            return super().form_valid(form)
        elif transaction_type == 'INCOME':
            user = self.request.user
            label_name = form.cleaned_data['label']
            received = Label.objects.filter(user=user, name=label_name).values('amount_received').get()
            amount_received = list(received.values())[0]
            form_amount = form.cleaned_data['amount']
            amount = form_amount + amount_received
            Label.objects.filter(user=user, name=label_name).update(amount_received=amount)
            funds_list = Profile.objects.filter(user=user).values('funds').get()
            funds = list(funds_list.values())[0]
            balance = funds + form_amount
            Profile.objects.filter(user=user).update(funds=balance)
            form.instance.user = self.request.user
            return super().form_valid(form)


@login_required
def update_transaction(request, id):
    transaction = Transaction.objects.get(id=id)
    form = TransactionForm(request.POST or None, instance=transaction)
    og_amount = transaction.amount

    if form.is_valid():
        transaction_type = form.cleaned_data['type']
        if transaction_type == 'EXPENSE':
            user = request.user
            label_name = form.cleaned_data['label']
            received1 = Label.objects.filter(user=user, name=label_name).values('amount_received').get()
            amount_received1 = list(received1.values())[0]
            refund_amount = amount_received1 + og_amount
            Label.objects.filter(user=user, name=label_name).update(amount_received=refund_amount)
            funds_list1 = Profile.objects.filter(user=user).values('funds').get()
            funds = list(funds_list1.values())[0]
            refund_balance = funds + og_amount
            Profile.objects.filter(user=user).update(funds=refund_balance)
            received = Label.objects.filter(user=user, name=label_name).values('amount_received').get()
            amount_received = list(received.values())[0]
            form_amount = form.cleaned_data['amount']
            amount = form_amount + amount_received
            Label.objects.filter(user=user, name=label_name).update(amount_received=amount)
            funds_list = Profile.objects.filter(user=user).values('funds').get()
            funds = list(funds_list.values())[0]
            balance = funds - form_amount
            Profile.objects.filter(user=user).update(funds=balance)
            form.save()
            return redirect('/budget/transactions')
        elif transaction_type == 'INCOME':
            user = request.user
            label_name = form.cleaned_data['label']
            received1 = Label.objects.filter(user=user, name=label_name).values('amount_received').get()
            amount_received1 = list(received1.values())[0]
            refund_amount = amount_received1 - og_amount
            Label.objects.filter(user=user, name=label_name).update(amount_received=refund_amount)
            funds_list1 = Profile.objects.filter(user=user).values('funds').get()
            funds = list(funds_list1.values())[0]
            refund_balance = funds - og_amount
            Profile.objects.filter(user=user).update(funds=refund_balance)
            received = Label.objects.filter(user=user, name=label_name).values('amount_received').get()
            amount_received = list(received.values())[0]
            form_amount = form.cleaned_data['amount']
            amount = form_amount + amount_received
            Label.objects.filter(user=user, name=label_name).update(amount_received=amount)
            funds_list = Profile.objects.filter(user=user).values('funds').get()
            funds = list(funds_list.values())[0]
            balance = funds + form_amount
            Profile.objects.filter(user=user).update(funds=balance)
            form.save()
            return redirect('/budget/transactions')

    return render(request, 'budget/transaction-form.html', {'form': form})


@login_required
def delete_transaction(request, id):
    transaction = Transaction.objects.get(id=id)

    if request.method == 'POST':
        transaction_type = transaction.type
        if transaction_type == 'INCOME':
            user = request.user
            label_name = transaction.label
            received = Label.objects.filter(user=user, name=label_name).values('amount_received').get()
            amount_received = list(received.values())[0]
            delete_amount = transaction.amount
            amount = amount_received - delete_amount
            Label.objects.filter(user=user, name=label_name).update(amount_received=amount)
            funds_list = Profile.objects.filter(user=user).values('funds').get()
            funds = list(funds_list.values())[0]
            balance = funds - delete_amount
            Profile.objects.filter(user=user).update(funds=balance)
            transaction.delete()
            return redirect('/budget/transactions')
        elif transaction_type == 'EXPENSE':
            user = request.user
            label_name = transaction.label
            received = Label.objects.filter(user=user, name=label_name).values('amount_received').get()
            amount_received = list(received.values())[0]
            delete_amount = transaction.amount
            amount = amount_received + delete_amount
            Label.objects.filter(user=user, name=label_name).update(amount_received=amount)
            funds_list = Profile.objects.filter(user=user).values('funds').get()
            funds = list(funds_list.values())[0]
            balance = funds + delete_amount
            Profile.objects.filter(user=user).update(funds=balance)
            transaction.delete()
            return redirect('/budget/transactions')

    return render(request, 'budget/transaction-delete.html', {'transaction': transaction})


def budget(request):
    user = request.user
    current_time = date
    categories_list = Category.objects.filter(user=user) if user.is_authenticated else Category.objects.all()
    labels_list = Label.objects.filter(user=user) if user.is_authenticated else Label.objects.all()
    template = loader.get_template('budget/budget.html')
    context = {
        'categories_list': categories_list,
        'labels_list': labels_list,
        'current_time': current_time
    }
    return HttpResponse(template.render(context, request))


# class based create category view
class CreateCategory(CreateView):
    form_class = CategoryForm
    template_name = 'budget/category-form.html'
    success_url = reverse_lazy("budget")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



@login_required
def update_category(request, id):
    category = Category.objects.get(id=id)
    form = CategoryForm(request.POST or None, instance=category)

    if form.is_valid():
        form.save()
        return redirect('/budget/budget')

    return render(request, 'budget/category-form.html', {'form': form})


@login_required
def delete_category(request, id):
    category = Category.objects.get(id=id)

    if request.method == 'POST':
        category.delete()
        return redirect('/budget/budget')

    return render(request, 'budget/category-delete.html', {'category': category})


# @login_required
# def create_label(request):
#     form = LabelForm(request.POST or None)

#     if form.is_valid():
#         form.save()
#         return redirect('/budget/budget')

#     return render(request, 'budget/label-form.html', {'form': form})

class CreateLabel(CreateView):
    form_class = LabelForm
    template_name = "budget/label-form.html"
    success_url = reverse_lazy("budget")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@login_required
def update_label(request, id):
    label = Label.objects.get(id=id)
    form = LabelForm(request.POST or None, instance=label)

    if form.is_valid():
        form.save()
        return redirect('/budget/budget')

    return render(request, 'budget/label-form.html', {'form': form})


@login_required
def delete_label(request, id):
    label = Label.objects.get(id=id)

    if request.method == 'POST':
        label.delete()
        return redirect('/budget/budget')

    return render(request, 'budget/label-delete.html', {'label': label})


def reports(request):
    user = request.user
    categories_list = Category.objects.filter(user=user) if user.is_authenticated else Label.objects.all()
    category_names = list(categories_list.values_list('name', flat=True))
    category_types = [x[0] for x in Category.CATEGORY_TYPE_CHOICES]
    # list(categories_list.values_list('type', flat=True))
    labels_list = Label.objects.filter(user=user) if user.is_authenticated else Label.objects.all()
    label_names = list(labels_list.values_list('name', flat=True))
    label_category = list(labels_list.values_list('category', flat=True))
    label_amountRec = list(labels_list.values_list('amount_received', flat=True))
    label_amountPlanned = list(labels_list.values_list('amount_planned', flat=True))
    transactions_list = Transaction.objects.filter(user=user) if user.is_authenticated else Label.objects.all()
    transaction_description = list(transactions_list.values_list('description', flat=True))
    transaction_type = list(transactions_list.values_list('type', flat=True))
    transaction_label = list(transactions_list.values_list('label', flat=True))
    transaction_amount = list (transactions_list.values_list('amount', flat=True))
    transaction_date = list(transactions_list.values_list('date', flat=True))

    #amount planned, received, remaining by category
    labels = Label.objects.filter(user=user)
    sums = [] 
    sumLabels = []
    receivedSums = []
    for category in Category.objects.filter(user=user):
        cat_sum = labels.filter(category=category).aggregate(Sum('amount_planned'))
        #sums[category.name] = cat_sum
        sums.append(cat_sum)
        sumLabels.append(category.name)
     
    for category in Category.objects.filter(user=user):
        cat_Receivedsum = labels.filter(category=category).aggregate(Sum('amount_received'))
        #sums[category.name] = cat_sum
        receivedSums.append(cat_Receivedsum)
      
    
    #categories type chart
    categories = Category.objects.filter(user=user)
    category_type_sum = OrderedDict()
    for category in categories:
        if category.type not in category_type_sum:
            category_type_sum[category.type] = 0
        category_type_sum[category.type] += 1

    #transaction chart
    transactions = Transaction.objects.filter(user=user)
    transaction_amount_sum = OrderedDict()
    for transaction in transactions:
        if transaction.type not in transaction_amount_sum:
            transaction_amount_sum[transaction.type] = 0
        transaction_amount_sum[transaction.type] += transaction.amount




    template = loader.get_template('budget/reports.html')
    context = {
        'categories_list': categories_list,
        'category_names': category_names,
        'category_types': list(category_type_sum.keys()),
        'labels_list': labels_list,
        'label_names': label_names,
        'label_category': label_category,
        'label_amountRec': label_amountRec,
        'label_amountPlanned': label_amountPlanned,
        'transactions_list': transactions_list,
        'transaction_description': transaction_description,
        'transaction_type': transaction_type,
        'transaction_label': transaction_label,
        'transaction_amount': transaction_amount,
        'transaction_date': transaction_date,
        'categoryTypeSum': list(category_type_sum.values()),
        'transactionAmountSum': list(transaction_amount_sum.values()),
        'sums': sums,
        'sumLabels': sumLabels,
        'receivedSums': receivedSums,


    
    }
    return HttpResponse(template.render(context, request))

