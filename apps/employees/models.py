from django.db import models
from apps.manager import models as menu_models


class Employee(models.Model):
    name = models.CharField(max_length=250)
    rut = models.CharField(max_length=10)
    email = models.EmailField(blank=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'employee'
        managed = True

    def __str__(self):
        return self.name


class Order(models.Model):
    """Order model."""
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING,
                                 related_name='orders', blank=True, null=True)
    created_at = models.DateTimeField(auto_created=True)
    state = models.CharField(max_length=25, default='Pending')
    active = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=64, decimal_places=2, default=0)

    class Meta:
        db_table = 'order'
        managed = True

    def __str__(self):
        return str(self.id)


class Version(models.Model):
    """Version model"""
    name = models.CharField(max_length=50)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'version'

    def __str__(self):
        return self.name


class OrderDetail(models.Model):
    """Order Detail model."""
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING,
                              blank=True, null=True, related_name='details')
    version = models.ForeignKey(Version, on_delete=models.DO_NOTHING, default=1)
    specification = models.TextField(blank=True, null=True)
    dish = models.ForeignKey(menu_models.Dish, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'order_detail'
        verbose_name = 'Order Details'
        verbose_name_plural = 'Orders Details'
