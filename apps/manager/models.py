import datetime
import logging

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import signals

from apps.manager import tasks
from . import helpers


class Chef(models.Model):
    """Chef model."""

    first_name = models.CharField(max_length=250, blank=None, null=True)
    last_name = models.CharField(max_length=250, blank=None, null=True)
    starts = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'chef'
        managed = True

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class Menu(models.Model):
    """Menu model."""

    name = models.CharField(max_length=250, blank=None, null=True)
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)
    effective_date = models.DateField(blank=True, null=True)
    chef = models.ForeignKey(Chef, blank=True, null=True, on_delete=models.DO_NOTHING,
                             related_name='chef_menus')
    active = models.BooleanField(default=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, blank=True,
                             null=True, related_name='user_menus')
    state = models.CharField(max_length=20, default='Draft')
    uuid = models.UUIDField(default=helpers.generate_uuid())

    class Meta:
        db_table = 'menu'
        managed = True
        ordering = ['created_at']

    def __str__(self):
        return self.name


class Option(models.Model):
    """Option model."""

    name = models.CharField(max_length=250, blank=None, null=True)
    code = models.CharField(max_length=15, blank=None, null=True)
    chef_recommendations = models.TextField(blank=True, null=True)
    cost_price = models.DecimalField(max_digits=64, decimal_places=2, default=0)
    sale_price = models.DecimalField(max_digits=64, decimal_places=2, default=0)
    active = models.BooleanField(default=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'option'
        managed = True
        ordering = ['id']

    def __str__(self):
        return self.name


class MenuOption(models.Model):
    """Menu Option model."""

    menu = models.ForeignKey(Menu, on_delete=models.DO_NOTHING)
    option = models.ForeignKey(Option, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'menu_option'
        managed = True
        verbose_name = 'Menu Option'
        verbose_name_plural = 'Menu Options'


class Group(models.Model):
    """Group of dishes, for example: juices, desserts, etc.."""

    name = models.CharField(max_length=250, blank=None, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'groups'
        ordering = ['id']

    def __str__(self):
        return self.name

    def get_str_id(self):
        return self.id


class SequenceOfMeal(models.Model):
    """Desire sequence model."""

    name = models.CharField(max_length=100, blank=True, null=True)
    index = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'sequences_of_meal'
        verbose_name_plural = 'Sequences of meals'

    def __str__(self):
        return self.name

    def get_str_id(self):
        return str(self.id)


class Dish(models.Model):
    """Dish model."""

    name = models.CharField(max_length=250)
    code = models.CharField(max_length=20, blank=True, null=True)
    ingredients = models.TextField(blank=True, null=True)
    order = models.ForeignKey(SequenceOfMeal, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(get_user_model(), blank=True, null=True, related_name='user_dishes',
                             on_delete=models.DO_NOTHING)
    active = models.BooleanField(default=True)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_created=True)

    class Meta:
        db_table = 'dish'
        verbose_name = 'Dish'
        verbose_name_plural = 'Dishes'
        ordering = ['id']

    def __str__(self):
        return '%s -- %s' % (self.name, self.order)


class OptionDish(models.Model):
    """Option dish model."""

    option = models.ForeignKey(Option, on_delete=models.DO_NOTHING,
                               related_name='options')
    dish = models.ForeignKey(Dish, on_delete=models.DO_NOTHING, related_name='dishes')

    class Meta:
        db_table = 'option_dish'


class OptionComment(models.Model):
    """Option comment model."""

    option = models.ForeignKey(Option, on_delete=models.DO_NOTHING,
                               related_name='option_comments')
    comment = models.TextField(blank=True, null=True)
    starts = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_created=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING,
                             blank=True, null=True)

    class Meta:
        db_table = 'option_comment'
        ordering = ['-created_at']
        verbose_name = 'Option Comment'
        verbose_name_plural = 'Option Comments'


def menu_post_save(sender, instance, **kwargs):
    if instance.state == 'Confirm':
        # Send notification email
        start_time = datetime.datetime.now() + datetime.timedelta(minutes=1)
        try:
            tasks.email_notification.apply_async((instance.uuid,), eta=start_time)
        except tasks.email_notification.OperationalError as exc:
            logging.error(exc)

        try:
            tasks.slack_notification.apply_async((instance.uuid,), eta=start_time)
        except tasks.slack_notification.OperationalError as exc:
            logging.error(exc)


signals.post_save.connect(menu_post_save, sender=Menu)
