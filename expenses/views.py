from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from .models import Category, Expense
from .forms import CategoryForm, ExpenseForm, ExpenseCommonForm, ExpenseLineItemForm
from django.forms import formset_factory
from django.shortcuts import redirect
import csv
from django.http import HttpResponse, JsonResponse

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'expenses/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        today = timezone.now().date()
        
        # Totals
        total_income = Expense.objects.filter(user=user, transaction_type='INCOME').aggregate(Sum('amount'))['amount__sum'] or 0
        total_expenses = Expense.objects.filter(user=user, transaction_type='EXPENSE').aggregate(Sum('amount'))['amount__sum'] or 0
        
        context['total_income'] = total_income
        context['total_expenses'] = total_expenses
        context['balance'] = total_income - total_expenses
        
        context['monthly_expenses'] = Expense.objects.filter(user=user, transaction_type='EXPENSE', date__month=today.month, date__year=today.year).aggregate(Sum('amount'))['amount__sum'] or 0
        context['daily_expenses'] = Expense.objects.filter(user=user, transaction_type='EXPENSE', date=today).aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Recent Expenses
        context['recent_expenses'] = Expense.objects.filter(user=user).order_by('-date', '-created_at')[:5]
        
        # Chart Data (Last 7 days) - Net Spending
        labels = []
        data = []
        for i in range(6, -1, -1):
            date = today - timedelta(days=i)
            labels.append(date.strftime('%a'))
            daily_expense = Expense.objects.filter(user=user, transaction_type='EXPENSE', date=date).aggregate(Sum('amount'))['amount__sum'] or 0
            data.append(float(daily_expense))
            
        context['chart_labels'] = labels
        context['chart_data'] = data
        
        return context

# Category Views
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'expenses/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'expenses/category_form.html'
    success_url = reverse_lazy('category_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'expenses/category_form.html'
    success_url = reverse_lazy('category_list')

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'expenses/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

# Expense Views
class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    template_name = 'expenses/expense_list.html'
    context_object_name = 'expenses'
    paginate_by = 10

    def get_queryset(self):
        queryset = Expense.objects.filter(user=self.request.user)
        category = self.request.GET.get('category')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')

        if category:
            queryset = queryset.filter(category__id=category)
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(user=self.request.user)
        return context

class ExpenseCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'expenses/expense_form.html'
    success_url = reverse_lazy('expense_list')

    def get(self, request, *args, **kwargs):
        common_form = ExpenseCommonForm(initial={'date': timezone.now().date()})
        ExpenseFormSet = formset_factory(ExpenseLineItemForm, extra=1)
        formset = ExpenseFormSet(form_kwargs={'user': request.user})
        return render(request, self.template_name, {'common_form': common_form, 'formset': formset})

    def post(self, request, *args, **kwargs):
        common_form = ExpenseCommonForm(request.POST)
        ExpenseFormSet = formset_factory(ExpenseLineItemForm)
        formset = ExpenseFormSet(request.POST, form_kwargs={'user': request.user})

        if common_form.is_valid() and formset.is_valid():
            date = common_form.cleaned_data['date']
            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    expense = form.save(commit=False)
                    expense.user = request.user
                    expense.date = date
                    # Auto-generate title from category or default
                    if expense.category:
                        expense.title = expense.category.name
                    else:
                        expense.title = "Uncategorized Expense"
                    expense.save()
            return redirect(self.success_url)
        
        return render(request, self.template_name, {'common_form': common_form, 'formset': formset})

class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expenses/expense_form.html'
    success_url = reverse_lazy('expense_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    model = Expense
    template_name = 'expenses/expense_confirm_delete.html'
    success_url = reverse_lazy('expense_list')

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

class ExportExpensesView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="expenses.csv"'

        writer = csv.writer(response)
        writer.writerow(['Date', 'Title', 'Category', 'Amount', 'Description'])

        expenses = Expense.objects.filter(user=request.user).order_by('-date')
        for expense in expenses:
            category_name = expense.category.name if expense.category else 'Uncategorized'
            writer.writerow([expense.date, expense.title, category_name, expense.amount, expense.description])

        return response

class ChartDataView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        days = int(request.GET.get('days', 7))
        transaction_type = request.GET.get('type', 'EXPENSE')
        today = timezone.now().date()
        labels = []
        data = []
        
        for i in range(days - 1, -1, -1):
            date = today - timedelta(days=i)
            labels.append(date.strftime('%b %d'))
            amount = Expense.objects.filter(user=request.user, transaction_type=transaction_type, date=date).aggregate(Sum('amount'))['amount__sum'] or 0
            data.append(float(amount))
            
        return JsonResponse({'labels': labels, 'data': data})
