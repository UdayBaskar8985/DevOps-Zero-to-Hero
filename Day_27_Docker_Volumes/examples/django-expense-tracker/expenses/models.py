from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    TYPE_CHOICES = [
        ('EXPENSE', 'Expense'),
        ('INCOME', 'Income'),
    ]
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    icon = models.CharField(max_length=10, default='📦')

    class Meta:
        verbose_name_plural = "Categories"
        unique_together = ('name', 'type')

    def __str__(self):
        return f"{self.icon} {self.name}"

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, limit_choices_to={'type': 'EXPENSE'})
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-date', '-id']

    def __str__(self):
        return f"{self.category.name} - ${self.amount} on {self.date}"

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incomes')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, limit_choices_to={'type': 'INCOME'})
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-date', '-id']

    def __str__(self):
        return f"{self.category.name} - ${self.amount} on {self.date}"

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, limit_choices_to={'type': 'EXPENSE'})
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.DateField()  # Store as YYYY-MM-01 to represent a month

    class Meta:
        unique_together = ('user', 'category', 'month')

    def __str__(self):
        return f"{self.category.name} Budget - ${self.amount} for {self.month.strftime('%Y-%m')}"
