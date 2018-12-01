from django.conf.urls import url
from . import views

app_name = 'employees'

urlpatterns = [
    url(r'^$', views.HomeEmployeesView.as_view(), name='home'),
    url(r'menu/(?P<uuid>[-\w]+)/$', views.HomeEmployeesView.as_view(), name='home_uuid'),
    url(r'^menu/option/(?P<option_id>\d+)/customize/$', views.customize_order, name='custom_order'),
    url(r'^search-order/$', views.SearchOrderFormView.as_view(), name='search_order'),
]
