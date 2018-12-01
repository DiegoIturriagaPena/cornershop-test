from sqlite3 import IntegrityError

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, render, redirect
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.html import format_html
from django.views import generic

from apps.access.decorators import user_has_permission
from apps.employees import models as employee_models
from apps.manager import forms
from apps.manager import helpers
from apps.manager import models


@method_decorator(user_has_permission, name='dispatch')
class HomeMenuView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'manager/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeMenuView, self).get_context_data(**kwargs)
        context['title'] = 'home'
        return context


@method_decorator(user_has_permission, name='dispatch')
class DishCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'manager/dish_form.html'
    form_class = forms.DishForm
    success_url = reverse_lazy('manager:dishes')

    def get_context_data(self, **kwargs):
        context = super(DishCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Create dish'
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return super(DishCreateView, self).form_valid(form)


@method_decorator(user_has_permission, name='dispatch')
class DishUpdateView(generic.UpdateView):
    template_name = 'manager/dish_form.html'
    form_class = forms.DishForm
    queryset = models.Dish.objects.all()
    success_url = reverse_lazy('manager:dishes')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return super(DishUpdateView, self).form_valid(form)


@method_decorator(user_has_permission, name='dispatch')
class DishListView(LoginRequiredMixin, generic.ListView):
    template_name = 'manager/dish_list.html'
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super(DishListView, self).get_context_data(**kwargs)
        context['title'] = 'Dishes'
        context['groups'] = helpers.get_groups()
        context['orders'] = helpers.get_orders()

        return context

    def get_queryset(self):
        params = self.request.GET
        self.queryset = helpers.get_all_dishes(params)
        return self.queryset


@method_decorator(user_has_permission, name='dispatch')
class OptionListView(LoginRequiredMixin, generic.ListView):
    template_name = 'manager/option_list.html'
    queryset = models.Option.objects.all()
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super(OptionListView, self).get_context_data(**kwargs)
        context['title'] = 'Options'
        return context

    def get_queryset(self):
        params = self.request.GET
        self.queryset = helpers.get_all_options(params)
        return self.queryset


@method_decorator(user_has_permission, name='dispatch')
class MenuListView(LoginRequiredMixin, generic.ListView):
    template_name = 'manager/menu_list.html'
    paginate_by = 25

    def get_queryset(self):
        params = self.request.GET
        return helpers.get_all_menus(params)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MenuListView, self).get_context_data(**kwargs)
        context['title'] = 'Menus'
        return context


@method_decorator(user_has_permission, name='dispatch')
class OrderListView(LoginRequiredMixin, generic.ListView):
    template_name = 'manager/order_list.html'
    paginate_by = 20

    def get_queryset(self):
        params = self.request.GET
        print(params)
        if 'criteria' in params.keys():
            return helpers.get_all_orders(params.get('criteria'))
        return helpers.get_all_orders(None)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        context['title'] = 'Employee orders'
        return context


@method_decorator(user_has_permission, name='dispatch')
class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    model = employee_models.Order
    queryset = employee_models.Order.objects.all()
    template_name = 'manager/order_details.html'

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['title'] = 'Order Details'
        context['details'] = None
        return context


@method_decorator(user_has_permission, name='dispatch')
class EmployeeListView(LoginRequiredMixin, generic.ListView):
    template_name = 'manager/employee_list.html'
    paginate_by = 25

    def get_queryset(self):
        params = self.request.GET
        if 'criteria' in params.keys():
            return helpers.get_all_employees(params.get('criteria'))
        return helpers.get_all_employees(None)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EmployeeListView, self).get_context_data(**kwargs)
        context['title'] = 'Employees'
        return context


@login_required
@user_has_permission
def option_create_edit(request, pk=None):
    template_name = 'manager/option_form.html'
    option = models.Option()
    queryset_option_dish = None
    if pk:
        option = get_object_or_404(models.Option, pk=pk)
        queryset_option_dish = helpers.get_option_dishes(option)
    form = forms.OptionForm(request.POST or None, instance=option)

    formset_option_dish = forms.OptionDishFormsetFactory(
        request.POST or None,
        instance=option,
        queryset=queryset_option_dish,
        prefix='frm_option_dish'
    )
    if request.method == 'POST':
        if form.is_valid() and formset_option_dish.is_valid():
            try:
                with transaction.atomic():
                    option = form.save(commit=False)
                    option.user = request.user
                    option.save()
                    # Register options dishes
                    for frm in formset_option_dish.forms:
                        if frm.cleaned_data.get('DELETE') and frm.instance.pk:
                            frm.instance.delete()
                        else:
                            option_dish = frm.save(commit=False)
                            option_dish.option = option
                            option_dish.save()
            except IntegrityError as error:
                messages.error(request, format_html('An error has occurred {0}'.format(error)))
            else:
                messages.success(request, "Successful action")
                return redirect('manager:option_list')
        else:
            print(form.errors)
            print(formset_option_dish.errors)
            messages.error(request, 'Invalid forms')

    context = {
        'form': form,
        'formset': formset_option_dish
    }
    return render(request, template_name, context)


@login_required
@user_has_permission
def menu_option_create_edit(request, pk=None):
    template_name = 'manager/menu_option_form.html'
    menu = models.Menu()
    queryset_menu_option = None
    if pk:
        menu = get_object_or_404(models.Menu, pk=pk)
        queryset_menu_option = helpers.get_all_menu_option(menu)
    form = forms.MenuForm(request.POST or None, instance=menu)

    formset_menu_option = forms.MenuOptionFormsetFactory(
        request.POST or None,
        instance=menu,
        queryset=queryset_menu_option,
        prefix='frm_menu_option'
    )
    if request.method == 'POST':
        if form.is_valid() and formset_menu_option.is_valid():
            try:
                with transaction.atomic():
                    menu = form.save(commit=False)
                    menu.user = request.user
                    menu.save()
                    # Register menu options dishes
                    for frm in formset_menu_option.forms:
                        if frm.cleaned_data.get('DELETE') and frm.instance.pk:
                            frm.instance.delete()
                        else:
                            menu_option = frm.save(commit=False)
                            menu_option.menu = menu
                            menu_option.save()
                    if 'btn_confirm' in request.POST:
                        menu.state = 'Confirm'
                        menu.save()

            except IntegrityError as error:
                messages.error(request, format_html('An error has occurred {0}'.format(error)))
            else:
                messages.success(request, "Successful action")
                return redirect('manager:menu_list')
        else:
            messages.error(request, 'Invalid forms')
    context = {
        'form': form,
        'formset': formset_menu_option,
        'menu': menu
    }
    return render(request, template_name, context)
