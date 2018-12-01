import datetime

from apps.employees import models


def get_employee_emails():
    """Returns active employees with email."""
    employees = models.Employee.objects.filter(
        active=True,
        email__isnull=False
    )
    return [employee.email for employee in employees]


def get_details_by_order_id(order_id):
    """
    Returns all order details given an order id.
    :param order_id:
    :return:
    """
    return models.OrderDetail.objects.filter(
        order__id=order_id
    )


def update_or_create_employee(defaults, employee):
    """
    Return
    :param defaults:
    :param employee:
    :return:
    """
    obj, created = models.Employee.objects.update_or_create(
        rut=employee.rut,
        defaults=defaults
    )
    return obj


def exist_employee_order(employee):
    """
    Return order given a rut employee.
    :param employee:
    :return:
    """
    today = datetime.datetime.now()
    return models.Order.objects.filter(
        employee__rut=employee.rut,
        created_at__day=today.day,
        created_at__year=today.year,
        created_at__month=today.month
    ).first()


def get_order_by_rut_and_id(rut, order_id):
    """
    Return order given a rut and an id.
    :param rut:
    :param order_id:
    :return:
    """
    return models.Order.objects.filter(
        employee__rut=rut,
        id=order_id
    ).first()
