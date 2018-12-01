from django import forms
from django.forms import inlineformset_factory

from apps.employees import models
from apps.commons.forms import BootstrapForm


class OrderDetailForm(forms.ModelForm, BootstrapForm):
    dish_name = forms.CharField()

    class Meta:
        model = models.OrderDetail
        fields = '__all__'
        widgets = {'dish': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(OrderDetailForm, self).__init__(*args, **kwargs)
        self.empty_permitted = False
        self.fields['specification'].widget.attrs['rows'] = 2
        self.fields['dish_name'].widget.attrs['readonly'] = 'true'
        self.fields['specification'].label = 'Customizations'
        self.fields['specification'].widget.attrs['placeholder'] = 'Specify customizations'

        instance = kwargs.get('instance', None)
        if instance:
            self.initial['dish_name'] = instance.dish.name


class EmployeeForm(forms.ModelForm, BootstrapForm):
    class Meta:
        model = models.Employee
        exclude = ('active',)

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['email'].help_text = 'Enter your email to receive ' \
                                         'notifications from our menus'


class SearchOrderForm(forms.Form):
    rut = forms.CharField(required=True, max_length=10, label='RUT')
    order_id = forms.IntegerField(required=True)

    def __init__(self, *args, **kwargs):
        super(SearchOrderForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
