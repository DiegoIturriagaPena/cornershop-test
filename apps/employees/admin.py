from django.contrib import admin

from apps.employees import models


class EmployeeModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'rut', 'active')


class VersionModelAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(models.Employee, EmployeeModelAdmin)
admin.site.register(models.Version, VersionModelAdmin)
