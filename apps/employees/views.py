import datetime
from sqlite3 import IntegrityError

from django.contrib import messages
from django.db import transaction
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, render, redirect
from django.urls.base import reverse_lazy
from django.utils.html import format_html
from django.views import generic

from apps.manager import helpers as menu_helper
from apps.manager.models import Option
from . import forms
from . import helpers
from . import models


def customize_order(request, option_id, order_id=None):
    """Customize order."""
    template_name = 'employees/custom_order_form.html'
    option = get_object_or_404(Option, id=option_id)
    order = None
    details = None
    now = datetime.datetime.now()

    # comment this part of code for testing
    # time validation
    if now.hour >= 11:
        messages.info(request, 'Exceeded selection time(Until 11 am)')
        return redirect(reverse_lazy('employees:home'))
    # end time validation

    if order_id:
        order = get_object_or_404(models.Order, id=order_id)
        details = helpers.get_details_by_order_id(order_id)
    else:
        order = models.Order()
        order.sale_price = option.sale_price

    employee_form = forms.EmployeeForm(request.POST or None)

    order_detail_formset_factory = inlineformset_factory(
        models.Order,
        models.OrderDetail,
        form=forms.OrderDetailForm,
        can_delete=False,
        extra=len(option.options.all()),
        validate_min=True
    )
    formset = order_detail_formset_factory(
        request.POST or None,
        instance=order,
        prefix='formset_details',
        queryset=details
    )

    index = 0
    for subform in formset.forms:
        dish = option.options.all()[index].dish
        subform.initial = {
            'dish': dish,
            'dish_name': dish.name
        }
        index += 1

    if request.method == 'POST':
        print(request.POST)
        if formset.is_valid() and employee_form.is_valid():
            try:
                with transaction.atomic():
                    employee = employee_form.save(commit=False)
                    defaults = {
                        'name': employee.name,
                        'rut': employee.rut,
                        'email': employee.email
                    }
                    if helpers.exist_employee_order(employee):
                        raise IntegrityError('There is already an order today for this employee')
                    employee = helpers.update_or_create_employee(defaults, employee)
                    order.employee = employee
                    order.created_at = datetime.datetime.now()
                    order.save()
                    # Register options dishes
                    for frm in formset.forms:
                        print(frm.cleaned_data)
                        detail = frm.save(commit=False)
                        detail.order = order
                        detail.save()
            except IntegrityError as error:
                messages.error(request, format_html('An error has occurred: {0}'.format(error)))
            else:
                messages.success(request, "Successful action. Order ID: %s" % order.id)
                return render(request, 'employees/success.html', {'order': order})
        else:
            print(employee_form.errors)
            messages.error(request, 'Invalid forms')

    context = {
        'title': 'Custom you order',
        'formset': formset,
        'order': order,
        'option': option,
        'employee_form': employee_form
    }
    return render(request, template_name, context)


class HomeEmployeesView(generic.TemplateView):
    template_name = 'employees/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeEmployeesView, self).get_context_data(**kwargs)
        context['title'] = 'Home'
        uuid = kwargs.get('uuid')
        context['menu_options'] = menu_helper.get_menu_options_of_day(uuid or None)
        return context


class SearchOrderFormView(generic.FormView):
    form_class = forms.SearchOrderForm
    template_name = 'employees/search_order.html'
    success_url = reverse_lazy('employees:search_order')

    def get_context_data(self, **kwargs):
        context = super(SearchOrderFormView, self).get_context_data(**kwargs)
        context['title'] = 'Search order'
        return context

    def form_valid(self, form):
        data = form.cleaned_data
        rut = data.get('rut')
        order_id = data.get('order_id')
        order = helpers.get_order_by_rut_and_id(rut, order_id)
        if not order:
            messages.info(self.request, format_html('Opss!!! <br> Order not found'))
        context = {
            'order': order,
            'form': self.get_form(),
            'title': 'Search order'
        }
        return render(self.request, 'employees/search_order.html/', context)
