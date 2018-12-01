from django.test import TestCase
# Create your tests here.
from django.urls import reverse

from apps.employees import forms


class HomeEmployeeViewTests(TestCase):
    def testing_home_view(self):
        # Get the client
        response = self.client.get(reverse('employees:home'))
        # Check the status code
        self.assertEqual(response.status_code, 200)
        # Verify that response contains this string
        self.assertContains(response, "MENU")


class SearchOrderFormViewTest(TestCase):
    def testing_view(self):
        response = self.client.get(reverse('employees:search_order'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Check your order")


class SearchOrderFormTest(TestCase):
    # Valid Form Data
    def test_UserForm_valid(self):
        form = forms.SearchOrderForm(data={'rut': "2455122149", 'order_id': 1, })
        self.assertTrue(form.is_valid())

    # Invalid Form Data
    def test_UserForm_invalid(self):
        form = forms.SearchOrderForm(data={'rut': None, 'order_id': None})
        self.assertFalse(form.is_valid())

        form = forms.SearchOrderForm(data={'rut': "2455122149", 'order_id': None})
        self.assertFalse(form.is_valid())

        form = forms.SearchOrderForm(data={'rut': "2455122149", 'order_id': "aaaaaaaaa"})
        self.assertFalse(form.is_valid())

        form = forms.SearchOrderForm(data={'rut': None, 'order_id': "aaaaaaaaa"})
        self.assertFalse(form.is_valid())


class MenuOptionsTest(TestCase):
    valid_uuid = '22f3d678-6ad0-416a-bcc1-4312bdba1eaf'

    def test_view_with_valid_uuid(self):
        response = self.client.get(reverse('employees:home_uuid',
                                           kwargs={'uuid': self.valid_uuid}))
        self.assertEqual(response.status_code, 200)
