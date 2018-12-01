from django.conf.urls import url
from . import views

app_name = 'manager'

urlpatterns = [
    # url(r'^$', views.HomeMenuView.as_view(),name='home'),
    url(r'^$', views.MenuListView.as_view(), name='menu_list'),
    url(r'^dishes/$', views.DishListView.as_view(),name='dishes'),
    url(r'^dish/create/$', views.DishCreateView.as_view(),name='dish_create'),
    url(r'^dish/(?P<pk>\d+)/update/$', views.DishUpdateView.as_view(),name='dish_update'),
    url(r'^options/$', views.OptionListView.as_view(), name='option_list'),
    url(r'^option/create/$', views.option_create_edit, name='option_create'),
    url(r'^option/(?P<pk>\d+)/update$', views.option_create_edit, name='option_update'),
    url(r'^create/$', views.menu_option_create_edit, name='menu_create'),
    url(r'^orders/$', views.OrderListView.as_view(),name='order_list'),
    url(r'^order/(?P<pk>\d+)/details$', views.OrderDetailView.as_view(),name='order_details'),
    url(r'^(?P<pk>\d+)/update/$', views.menu_option_create_edit, name='menu_update'),
    url(r'^employees/$', views.EmployeeListView.as_view(),name='employee_list'),
]
