from collections import OrderedDict

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.db.models import Sum 
from datetime import date

# from rest_framework import viewsets
# from .serializers import CategorySerializer, LabelSerializer, TransactionSerializer
from .models import Category, Label, Transaction
from django.contrib.auth.decorators import login_required
from .forms import CategoryForm, LabelForm, TransactionForm
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy


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
      
   
    print(sumLabels)
    print(sums)
    print(receivedSums)
   

    
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

# @login_required
# def create_transaction(request):
#     form = TransactionForm(request.POST or None)

#     if form.is_valid():
#         form.save()
#         return redirect('/budget/transactions')

#     return render(request, 'budget/transaction-form.html', {'form': form})

#class based form
class CreateTransaction(CreateView):
    model = Transaction
    fields = ['description', 'type', 'label', 'amount', 'date']
    template_name = 'budget/transaction-form.html'
    success_url = reverse_lazy("transactions")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@login_required
def update_transaction(request, id):
    course = Transaction.objects.get(id=id)
    form = TransactionForm(request.POST or None, instance=course)

    if form.is_valid():
        user = request.user 
        form.save()
        return redirect('/budget/transactions')

    return render(request, 'budget/transaction-form.html', {'form': form})


@login_required
def delete_transaction(request, id):
    transaction = Transaction.objects.get(id=id)

    if request.method == 'POST':
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


# @login_required
# def create_category(request):
#     form = CategoryForm(request.POST or None)

#     if form.is_valid():
#         form.save()
#         return redirect('/budget/budget')

#     return render(request, 'budget/category-form.html', {'form': form})

#classed based create category view
class CreateCategory(CreateView):
    model = Category
    fields = ['name', 'type']
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
    model = Label
    fields = ['name', 'category', 'amount_planned', 'amount_received', 'due_date', 'notes']
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
    category_types = list(categories_list.values_list('type', flat=True))
    labels_list = Label.objects.filter(user=user) if user.is_authenticated else Label.objects.all()
    label_names = list(labels_list.values_list('name', flat=True))
    label_category = list(labels_list.values_list('category', flat=True))
    label_amountRec = list(labels_list.values_list('amount_received', flat=True))
    label_amountPlanned = list(labels_list.values_list('amount_planned', flat=True))
    transactions_list = Transaction.objects.filter(user=user) if user.is_authenticated else Label.objects.all()
    transaction_description = list(transactions_list.values_list('description', flat=True))
    transaction_type = list(transactions_list.values_list('type', flat=True))
    transaction_label = list(transactions_list.values_list('label', flat=True))
    transaction_amount = list(transactions_list.values_list('amount', flat=True))
    transaction_date = list(transactions_list.values_list('date', flat=True))
    template = loader.get_template('budget/reports.html')
    context = {
        'categories_list': categories_list,
        'category_names': category_names,
        'category_types': category_types,
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
    }
    return HttpResponse(template.render(context, request))

