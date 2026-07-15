from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from django.http import HttpResponse
import csv
import datetime
from .models import Expense, Income, Budget, Category
from .forms import ExpenseForm, IncomeForm, BudgetForm, RegisterForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account has been created.")
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'expenses/signup.html', {'form': form})

@login_required
def dashboard_view(request):
    today = timezone.localdate()
    start_of_month = today.replace(day=1)
    
    # Calculate end of month
    if today.month == 12:
        end_of_month = today.replace(year=today.year + 1, month=1, day=1) - datetime.timedelta(days=1)
    else:
        end_of_month = today.replace(month=today.month + 1, day=1) - datetime.timedelta(days=1)

    # 1. Summaries for current month
    total_income = Income.objects.filter(
        user=request.user,
        date__range=[start_of_month, end_of_month]
    ).aggregate(total=Sum('amount'))['total'] or 0

    total_expense = Expense.objects.filter(
        user=request.user,
        date__range=[start_of_month, end_of_month]
    ).aggregate(total=Sum('amount'))['total'] or 0

    net_savings = total_income - total_expense
    abs_net_savings = abs(net_savings)
    savings_rate = int((net_savings / total_income) * 100) if total_income > 0 else 0

    # 2. Budgets checking
    budgets = Budget.objects.filter(user=request.user, month=start_of_month)
    budget_progress = []
    for b in budgets:
        spent = Expense.objects.filter(
            user=request.user,
            category=b.category,
            date__range=[start_of_month, end_of_month]
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        percent = int((spent / b.amount) * 100) if b.amount > 0 else 0
        budget_progress.append({
            'budget': b,
            'spent': spent,
            'percent': min(percent, 100),
            'remaining': b.amount - spent,
            'warning': percent >= 80,
            'exceeded': percent > 100
        })

    # 3. Recent items (combined list of last 5 expenses and incomes)
    recent_expenses = Expense.objects.filter(user=request.user)[:5]
    recent_incomes = Income.objects.filter(user=request.user)[:5]
    recent_transactions = sorted(
        list(recent_expenses) + list(recent_incomes),
        key=lambda x: x.date,
        reverse=True
    )[:5]

    # 4. Chart Data: Expense by Category
    category_data = Expense.objects.filter(
        user=request.user,
        date__range=[start_of_month, end_of_month]
    ).values('category__name', 'category__icon').annotate(total=Sum('amount')).order_by('-total')
    
    cat_labels = [f"{item['category__icon']} {item['category__name']}" for item in category_data]
    cat_values = [float(item['total']) for item in category_data]

    # 5. Chart Data: Daily Spending Trend
    expenses_this_month = Expense.objects.filter(
        user=request.user,
        date__range=[start_of_month, end_of_month]
    )
    daily_totals = {}
    for i in range(1, today.day + 1):
        d = today.replace(day=i)
        daily_totals[d.strftime('%b %d')] = 0

    for exp in expenses_this_month:
        day_str = exp.date.strftime('%b %d')
        if day_str in daily_totals:
            daily_totals[day_str] += float(exp.amount)

    trend_labels = list(daily_totals.keys())
    trend_values = list(daily_totals.values())

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'net_savings': net_savings,
        'abs_net_savings': abs_net_savings,
        'savings_rate': savings_rate,
        'budget_progress': budget_progress,
        'recent_transactions': recent_transactions,
        'cat_labels': cat_labels,
        'cat_values': cat_values,
        'trend_labels': trend_labels,
        'trend_values': trend_values,
        'current_month': today.strftime('%B %Y')
    }
    return render(request, 'expenses/dashboard.html', context)

# --- EXPENSE CRUD ---
@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)
    
    # Filter operations
    category_id = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if category_id:
        expenses = expenses.filter(category_id=category_id)
    if start_date:
        expenses = expenses.filter(date__gte=start_date)
    if end_date:
        expenses = expenses.filter(date__lte=end_date)

    categories = Category.objects.filter(type='EXPENSE')
    return render(request, 'expenses/expense_list.html', {
        'expenses': expenses,
        'categories': categories
    })

@login_required
def expense_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, "Expense added successfully!")
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/expense_form.html', {'form': form, 'title': 'Add Expense'})

@login_required
def expense_update(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, "Expense updated successfully!")
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expenses/expense_form.html', {'form': form, 'title': 'Edit Expense'})

@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, "Expense deleted successfully!")
    return redirect('expense_list')

# --- INCOME CRUD ---
@login_required
def income_list(request):
    incomes = Income.objects.filter(user=request.user)
    category_id = request.GET.get('category')
    if category_id:
        incomes = incomes.filter(category_id=category_id)
        
    categories = Category.objects.filter(type='INCOME')
    return render(request, 'expenses/income_list.html', {
        'incomes': incomes,
        'categories': categories
    })

@login_required
def income_create(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            messages.success(request, "Income source added successfully!")
            return redirect('income_list')
    else:
        form = IncomeForm()
    return render(request, 'expenses/income_form.html', {'form': form, 'title': 'Add Income'})

@login_required
def income_update(request, pk):
    income = get_object_or_404(Income, pk=pk, user=request.user)
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            messages.success(request, "Income source updated successfully!")
            return redirect('income_list')
    else:
        form = IncomeForm(instance=income)
    return render(request, 'expenses/income_form.html', {'form': form, 'title': 'Edit Income'})

@login_required
def income_delete(request, pk):
    income = get_object_or_404(Income, pk=pk, user=request.user)
    if request.method == 'POST':
        income.delete()
        messages.success(request, "Income source deleted successfully!")
    return redirect('income_list')

# --- BUDGET CRUD ---
@login_required
def budget_list(request):
    today = timezone.localdate()
    start_of_month = today.replace(day=1)
    budgets = Budget.objects.filter(user=request.user, month=start_of_month)
    return render(request, 'expenses/budget_list.html', {'budgets': budgets, 'current_month': today.strftime('%B %Y')})

@login_required
def budget_create(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            # Check if budget already exists for this category/month
            existing = Budget.objects.filter(user=request.user, category=budget.category, month=budget.month).first()
            if existing:
                existing.amount = budget.amount
                existing.save()
                messages.success(request, f"Budget for {budget.category.name} updated successfully!")
            else:
                budget.save()
                messages.success(request, f"Budget for {budget.category.name} created successfully!")
            return redirect('budget_list')
    else:
        form = BudgetForm()
    return render(request, 'expenses/budget_form.html', {'form': form, 'title': 'Set Category Budget'})

@login_required
def budget_update(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            messages.success(request, "Budget updated successfully!")
            return redirect('budget_list')
    else:
        form = BudgetForm(instance=budget)
    return render(request, 'expenses/budget_form.html', {'form': form, 'title': 'Edit Budget'})

@login_required
def budget_delete(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        budget.delete()
        messages.success(request, "Budget deleted successfully!")
    return redirect('budget_list')

# --- CSV EXPORT ---
@login_required
def export_expenses_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="expenses_{timezone.localdate().strftime("%Y%m%d")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Date', 'Category', 'Amount', 'Description'])
    
    expenses = Expense.objects.filter(user=request.user)
    for exp in expenses:
        writer.writerow([exp.date, exp.category.name, exp.amount, exp.description])
        
    return response

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')
