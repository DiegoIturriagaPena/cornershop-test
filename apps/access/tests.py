from django.test import TestCase
from django.urls.base import reverse


class LoginTestCase(TestCase):
    def test_login(self):
        response = self.client.get(reverse('manager:menu_list'))
        self.assertEquals(response.status_code, 403)

        response = self.client.get(reverse('manager:dishes'))
        self.assertEquals(response.status_code, 403)

        response = self.client.get(reverse('manager:dish_create'))
        self.assertEquals(response.status_code, 403)

        response = self.client.get(reverse('manager:dish_update', kwargs={'pk': 1}))
        self.assertEquals(response.status_code, 403)

        response = self.client.get(reverse('manager:option_list'))
        self.assertEquals(response.status_code, 403)

        response = self.client.get(reverse('manager:order_list'))
        self.assertEquals(response.status_code, 403)

        response = self.client.get(reverse('manager:order_details', kwargs={'pk': 1}))
        self.assertEquals(response.status_code, 403)

        response = self.client.get(reverse('manager:employee_list'))
        self.assertEquals(response.status_code, 403)
