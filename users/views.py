from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
from .forms import RegistrationForm, UserForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.apps import apps
from django.contrib.auth import authenticate, login


from budget import models as budget_models # jami - for default categories


# Create your views here.


@login_required
def profilepage(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your funds have been successfully updated!')
        else:
            messages.error(request, 'Unable to complete request')
        return redirect('profile')
    form = ProfileForm(instance=request.user.profile)
    return render(request=request, template_name="users/profile.html", context={"user": request.user, "form": form})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save() # add user to form.save - jami
            new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, new_user)
            #To create default categories for user when registering - Jami
            budget_models.Category.create_default_categories(new_user)
            budget_models.Label.create_default_labels(new_user)
            budget_models.Transaction.create_default_transactions(new_user)
            name = form.cleaned_data.get('username')
            messages.success(request, f'Welcome {name}! You are logged in.')
            return redirect('dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})

# @login_required
# def profilepage(request):
#     return render(request, 'users/profile.html')
