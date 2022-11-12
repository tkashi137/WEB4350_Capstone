from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
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
    transactions_list = Transaction.objects.all()
    categories_list = Category.objects.all()
    labels_list = Label.objects.all()
    template = loader.get_template('budget/dashboard.html')
    context = {
        'transactions_list': transactions_list,
        'categories_list': categories_list,
        'labels_list': labels_list
    }
    return HttpResponse(template.render(context, request))


def transactions(request):
    transactions_list = Transaction.objects.all()
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
    categories_list = Category.objects.all()
    labels_list = Label.objects.all()
    template = loader.get_template('budget/budget.html')
    context = {
        'categories_list': categories_list,
        'labels_list': labels_list
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
    transactions_list = Transaction.objects.all()
    categories_list = Category.objects.all()
    labels_list = Label.objects.all()
    template = loader.get_template('budget/reports.html')
    context = {
        'transactions_list': transactions_list,
        'categories_list': categories_list,
        'labels_list': labels_list
    }
    return HttpResponse(template.render(context, request))



# JUST FOR TESTING!
# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer


# JUST FOR TESTING!
# class CatExpenseViewSet(viewsets.ModelViewSet):
#     queryset = Category.objects.filter(type='EXPENSE')
#     serializer_class = CategorySerializer


