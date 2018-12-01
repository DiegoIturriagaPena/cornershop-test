from django.contrib.auth import views as auth_views
from django.urls.base import reverse_lazy
from django.views import generic

from . import forms


class LoginTemplateView(auth_views.LoginView):
    """Login View."""
    template_name = 'login.html'
    redirect_field_name = 'next'

    def get_success_url(self):
        if self.request.user.groups.filter(name__iexact='admin').exists() \
                or self.request.user.is_superuser:
            return reverse_lazy('manager:menu_list')
        elif self.request.user.groups.filter(name__iexact='clients').exists():
            return reverse_lazy('employees:home')


class RegisterView(generic.CreateView):
    """Signup view."""
    form_class = forms.RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('access:login')
