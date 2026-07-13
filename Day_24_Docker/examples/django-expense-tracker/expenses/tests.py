from django.template.context import BaseContext

# Monkey-patch BaseContext.__copy__ for Python 3.14 compatibility
def patched_copy(self):
    cls = self.__class__
    duplicate = cls.__new__(cls)
    for k, v in self.__dict__.items():
        if k != 'dicts':
            setattr(duplicate, k, v)
    duplicate.dicts = self.dicts[:]
    return duplicate

BaseContext.__copy__ = patched_copy

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Category, Expense, Income, Budget
import datetime

class ExpenseTrackerTests(TestCase):

    def setUp(self):
        self.client = Client(raise_request_exception=True)
        self.user = User.objects.create_user(username='testuser', password='password123')
        
        # Categories are seeded automatically via signals, but let's ensure we fetch or mock them
        self.food_category = Category.objects.get_or_create(name='Food', type='EXPENSE', defaults={'icon': '🍔'})[0]
        self.salary_category = Category.objects.get_or_create(name='Salary', type='INCOME', defaults={'icon': '💰'})[0]

    def test_category_seeding(self):
        """Verify default categories are successfully seeded."""
        categories = Category.objects.all()
        self.assertGreater(categories.count(), 0)
        self.assertTrue(categories.filter(name='Food', type='EXPENSE').exists())
        self.assertTrue(categories.filter(name='Salary', type='INCOME').exists())

    def test_auth_required_for_dashboard(self):
        """Verify redirect to login when accessing dashboard unauthenticated."""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_dashboard_calculations(self):
        """Verify total income, expense, net savings, and savings rate calculations."""
        self.client.login(username='testuser', password='password123')
        
        today = timezone.localdate()
        
        # Add income log
        Income.objects.create(
            user=self.user,
            category=self.salary_category,
            amount=5000.00,
            date=today,
            description="Monthly salary deposit"
        )
        
        # Add expense logs
        Expense.objects.create(
            user=self.user,
            category=self.food_category,
            amount=1000.00,
            date=today,
            description="Grocery run"
        )
        Expense.objects.create(
            user=self.user,
            category=self.food_category,
            amount=500.00,
            date=today,
            description="Dinner out"
        )

        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(response.context['total_income'], 5000.00)
        self.assertEqual(response.context['total_expense'], 1500.00)
        self.assertEqual(response.context['net_savings'], 3500.00)
        self.assertEqual(response.context['savings_rate'], 70)  # (3500 / 5000) * 100 = 70%

    def test_budget_warnings(self):
        """Verify budget warning indicators (warning at 80% capacity)."""
        self.client.login(username='testuser', password='password123')
        
        today = timezone.localdate()
        start_of_month = today.replace(day=1)
        
        # Create a budget of $1000
        budget = Budget.objects.create(
            user=self.user,
            category=self.food_category,
            amount=1000.00,
            month=start_of_month
        )
        
        # Spent $850 (85% - should trigger warning, but not exceeded)
        Expense.objects.create(
            user=self.user,
            category=self.food_category,
            amount=850.00,
            date=today,
            description="Weekly shopping"
        )

        response = self.client.get(reverse('dashboard'))
        budget_info = response.context['budget_progress'][0]
        
        self.assertEqual(budget_info['spent'], 850.00)
        self.assertEqual(budget_info['percent'], 85)
        self.assertTrue(budget_info['warning'])
        self.assertFalse(budget_info['exceeded'])

        # Spent another $200 (Total $1050 - should trigger exceeded)
        Expense.objects.create(
            user=self.user,
            category=self.food_category,
            amount=200.00,
            date=today,
            description="Luxury dining"
        )

        response = self.client.get(reverse('dashboard'))
        budget_info = response.context['budget_progress'][0]
        self.assertEqual(budget_info['spent'], 1050.00)
        self.assertTrue(budget_info['exceeded'])
