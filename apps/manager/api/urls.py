from django.conf.urls import url
from apps.manager.api import api

app_name = 'menu'

urlpatterns = [
    url(r'^api/order/update/$', api.change_order_state),
]
