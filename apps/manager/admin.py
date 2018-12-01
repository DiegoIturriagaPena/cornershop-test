from django.contrib import admin
from apps.manager import models


class OrderDishModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'index', 'active')

class GroupModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')

class MenuModelAdmin(admin.ModelAdmin):
    list_display = ('name', )

class ChefModelAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'starts',)

admin.site.register(models.SequenceOfMeal, OrderDishModelAdmin)
admin.site.register(models.Group, GroupModelAdmin)
admin.site.register(models.Menu, MenuModelAdmin)
admin.site.register(models.Chef, ChefModelAdmin)