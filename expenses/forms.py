from django import forms
from .models import Category, Expense

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'color']
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color', 'class': 'input input-bordered w-full h-12 p-1'}),
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'transaction_type', 'category', 'date', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'transaction_type': forms.Select(attrs={'class': 'select select-bordered w-full'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)

class ExpenseCommonForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'input input-bordered w-full'}))

class ExpenseLineItemForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['transaction_type', 'amount', 'category', 'description']
        widgets = {
            'transaction_type': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'amount': forms.NumberInput(attrs={'class': 'input input-bordered w-full amount-input', 'placeholder': 'Amount', 'step': '0.01'}),
            'category': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'description': forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full', 'rows': 1, 'placeholder': 'Description'}),
        }

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)
