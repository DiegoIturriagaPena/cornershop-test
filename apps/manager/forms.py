from django import forms
from django.forms import inlineformset_factory

from apps.commons.forms import BootstrapForm
from apps.manager import models


class DishForm(forms.ModelForm, BootstrapForm):
    class Meta:
        model = models.Dish
        exclude = ('user',)


class OptionForm(forms.ModelForm, BootstrapForm):
    class Meta:
        model = models.Option
        exclude = ('user',)


class OptionDishForm(forms.ModelForm, BootstrapForm):
    class Meta:
        model = models.OptionDish
        exclude = ("option",)


class MenuForm(forms.ModelForm, BootstrapForm):
    class Meta:
        model = models.Menu
        exclude = ('user', 'state', 'effective_date', 'uuid')


class MenuOptionForm(forms.ModelForm, BootstrapForm):
    class Meta:
        model = models.MenuOption
        exclude = ('menu',)


OptionDishFormsetFactory = inlineformset_factory(
    models.Option,
    models.OptionDish,
    form=OptionDishForm,
    can_delete=True,
    extra=0,
    min_num=1,
    validate_min=True
)

MenuOptionFormsetFactory = inlineformset_factory(
    models.Menu,
    models.MenuOption,
    form=MenuOptionForm,
    can_delete=True,
    extra=0,
    min_num=1,
    validate_min=True
)
