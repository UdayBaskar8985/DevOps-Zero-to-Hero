from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Expense, Income, Budget, Category
import datetime

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'date', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.TextInput(attrs={'placeholder': 'What was this for?'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'glass-input'})
        self.fields['category'].queryset = Category.objects.filter(type='EXPENSE')

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['category', 'amount', 'date', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.TextInput(attrs={'placeholder': 'Source of income'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'glass-input'})
        self.fields['category'].queryset = Category.objects.filter(type='INCOME')

class BudgetForm(forms.ModelForm):
    month_input = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'month', 'class': 'glass-input'}),
        label="Budget Month"
    )

    class Meta:
        model = Budget
        fields = ['category', 'amount']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'glass-input'})
        self.fields['category'].queryset = Category.objects.filter(type='EXPENSE')
        
        if self.instance and self.instance.pk:
            self.fields['month_input'].initial = self.instance.month.strftime('%Y-%m')

    def clean(self):
        cleaned_data = super().clean()
        month_str = cleaned_data.get('month_input')
        if month_str:
            try:
                year, month = map(int, month_str.split('-'))
                cleaned_data['month'] = datetime.date(year, month, 1)
            except ValueError:
                raise forms.ValidationError("Invalid month format. Please use YYYY-MM.")
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.month = self.cleaned_data['month']
        if commit:
            instance.save()
        return instance

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'glass-input', 'placeholder': 'Enter your email'})
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['username', 'email']:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update({
                    'class': 'glass-input',
                    'placeholder': f'Enter your {field_name}'
                })
