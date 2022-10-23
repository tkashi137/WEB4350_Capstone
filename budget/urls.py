from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name="index"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('transactions/', views.transactions, name="transactions"),
    path('add-transaction/', views.create_transaction, name="create_transaction"),
    path('update-transaction/<int:id>', views.update_transaction, name="update_transaction"),
    path('delete-transaction/<int:id>', views.delete_transaction, name="delete_transaction"),
    path('budget/', views.budget, name="budget"),
    path('add-category/', views.create_category, name="create_category"),
    path('update-category/<int:id>', views.update_category, name="update_category"),
    path('delete-category/<int:id>', views.delete_category, name="delete_category"),
    path('add-label/', views.create_label, name="create_label"),
    path('update-label/<int:id>', views.update_label, name="update_label"),
    path('delete-label/<int:id>', views.delete_label, name="delete_label"),
    path('reports/', views.reports, name="reports")
]
