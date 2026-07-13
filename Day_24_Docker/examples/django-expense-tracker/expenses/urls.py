from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Dashboard and Auth
    path('', views.dashboard_view, name='dashboard'),
    path('signup/', views.register_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='expenses/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Expenses CRUD
    path('expenses/', views.expense_list, name='expense_list'),
    path('expenses/new/', views.expense_create, name='expense_create'),
    path('expenses/<int:pk>/edit/', views.expense_update, name='expense_update'),
    path('expenses/<int:pk>/delete/', views.expense_delete, name='expense_delete'),

    # Income CRUD
    path('income/', views.income_list, name='income_list'),
    path('income/new/', views.income_create, name='income_create'),
    path('income/<int:pk>/edit/', views.income_update, name='income_update'),
    path('income/<int:pk>/delete/', views.income_delete, name='income_delete'),

    # Budgets CRUD
    path('budgets/', views.budget_list, name='budget_list'),
    path('budgets/new/', views.budget_create, name='budget_create'),
    path('budgets/<int:pk>/edit/', views.budget_update, name='budget_update'),
    path('budgets/<int:pk>/delete/', views.budget_delete, name='budget_delete'),

    # Export
    path('export/expenses/', views.export_expenses_csv, name='export_expenses_csv'),
]
