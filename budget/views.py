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


# Create your views here.


def index(request):
    template = loader.get_template('budget/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def dashboard(request):
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

    labels = Label.objects.filter(user=user)
    sums = [] # maybe you just need a list of all the sums, depends on what the graph library wants
    sumLabels = []
    for category in Category.objects.filter(user=user):
        cat_sum = labels.filter(category=category).aggregate(Sum('amount_planned'))
        #sums[category.name] = cat_sum
        sums.append(cat_sum)
        sumLabels.append(category.name)
        #put in context, load in, pass to graph

    template = loader.get_template('budget/dashboard.html')
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
       # 'cat_sum': cat_sum,
       # 'sums': sums,
       # 'sumLabels': sumLabels,

    }
    return HttpResponse(template.render(context, request))


@login_required
def transactions(request):
    user = request.user
    #transactions_list = Transaction.objects.all()
    transactions_list = Transaction.objects.filter(user=user) if user.is_authenticated else Transaction.objects.all()
    template = loader.get_template('budget/transactions.html')
    context = {
        'transactions_list': transactions_list,
    }
    return HttpResponse(template.render(context, request))


@login_required
def create_transaction(request):
    form = TransactionForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('/budget/transactions')

    return render(request, 'budget/transaction-form.html', {'form': form})


@login_required
def update_transaction(request, id):
    course = Transaction.objects.get(id=id)
    form = TransactionForm(request.POST or None, instance=course)

    if form.is_valid():
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


@login_required
def create_category(request):
    form = CategoryForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('/budget/budget')

    return render(request, 'budget/category-form.html', {'form': form})


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


@login_required
def create_label(request):
    form = LabelForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('/budget/budget')

    return render(request, 'budget/label-form.html', {'form': form})


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

