def create_default_categories(sender, **kwargs):
    from .models import Category

    default_categories = [
        # Expenses
        ('Food', 'EXPENSE', '🍔'),
        ('Utilities', 'EXPENSE', '💡'),
        ('Travel', 'EXPENSE', '🚗'),
        ('Entertainment', 'EXPENSE', '🎬'),
        ('Rent', 'EXPENSE', '🏠'),
        ('Shopping', 'EXPENSE', '🛍️'),
        ('Healthcare', 'EXPENSE', '🏥'),
        ('Other Expense', 'EXPENSE', '📦'),
        
        # Income
        ('Salary', 'INCOME', '💰'),
        ('Freelance', 'INCOME', '💻'),
        ('Investments', 'INCOME', '📈'),
        ('Gifts', 'INCOME', '🎁'),
        ('Other Income', 'INCOME', '💸'),
    ]

    for name, cat_type, icon in default_categories:
        Category.objects.get_or_create(
            name=name,
            type=cat_type,
            defaults={'icon': icon}
        )
