import datetime
import uuid

import pandas as pd
import pytz
from django.conf import settings
from django.db.models import Q

from apps.manager import models
from apps.employees import models as employee_models


def get_all_dishes(params):
    """Returns all active dishes."""

    group = params.get('select_group')
    group = group if group != 'none' else None

    order = params.get('select_order')
    order = order if order != 'none' else None

    criteria = params.get('criteria') or None
    queryset = models.Dish.objects.all()
    if group:
        queryset = queryset.filter(group__name__icontains=group)
    if order:
        queryset = queryset.filter(order__name__icontains=order)
    if criteria:
        queryset = queryset.filter(
            Q(name__icontains=criteria) |
            Q(ingredients__icontains=criteria)
        )
    return queryset


def get_orders():
    """Returns all orders."""
    return models.SequenceOfMeal.objects.filter(active=True).order_by('index')


def get_groups():
    """Returns all groups."""
    return models.Group.objects.filter(active=True).order_by('id')


def get_option_dishes(option):
    """Returns all menu options dishes given a option."""
    return models.OptionDish.objects.filter(
        option=option
    ).order_by('dish__order__index')


def get_all_menu_option(menu):
    """Returns all menu options given a menu."""
    return models.MenuOption.objects.filter(menu=menu)


def get_all_options(params):
    """Return all options."""
    criteria = params.get('criteria') or None
    queryset = models.Option.objects.all()
    if criteria:
        queryset = queryset.filter(
            Q(name__icontains=criteria) |
            Q(chef_recommendations__icontains=criteria) |
            Q(code__icontains=criteria)
        )
    return queryset


def get_all_menus(params):
    """Return all menu."""
    criteria = params.get('criteria') or None
    queryset = models.Menu.objects.all()
    if criteria:
        queryset = queryset.filter(
            name__icontains=criteria
        )
    return queryset


def get_menu_options_of_day(uuid=None):
    """Menu of day."""
    today = datetime.datetime.now()
    menu_options = None
    if uuid:
        menu_options = models.MenuOption.objects.filter(
            menu__uuid=uuid
        )
    else:
        menu_options = models.MenuOption.objects.filter(
            menu__created_at__year=today.year,
            menu__created_at__month=today.month,
            menu__state='Confirm',
            menu__active=True,
            menu__created_at__day=today.day
        )
    return menu_options


def get_date_range(menu):
    """Returns date range given menu created at."""
    freq = '{0}min'.format(settings.PERIODICITY)
    end_date = datetime.datetime.now() + datetime.timedelta(minutes=5)
    dates = pd.date_range(
        start=menu.created_at,
        end=end_date, freq=freq
    )
    return dates


def convert_to_utc(date_time, timezone='America/Santiago'):
    utc = pytz.utc
    time_zone = pytz.timezone(timezone)
    dt = time_zone.localize(date_time)
    return dt.astimezone(utc)


def generate_uuid():
    """Return uuid"""
    return uuid.uuid4().hex


def get_menu_by_uuid(uuid):
    """Return a menu given a uuid."""
    return models.Menu.objects.filter(uuid__exact=uuid).first()


def get_all_orders(criteria):
    """Returns all orders"""
    if criteria:
        return employee_models.Order.objects.filter(
            employee__name__icontains=criteria
        ).order_by('-created_at')
    return employee_models.Order.objects.all().order_by('-created_at')


def get_all_employees(criteria):
    """
    Returns all employees.
    :param criteria:
    :return:
    """
    print(criteria)
    queryset = employee_models.Employee.objects.filter().order_by('id')
    if criteria:
        queryset = queryset.filter(
            Q(name__icontains=criteria) |
            Q(rut__icontains=criteria) |
            Q(email__icontains=criteria)
        )
    return queryset

