from django.core.exceptions import PermissionDenied


def user_has_permission(function):
    def wrap(request, *args, **kwargs):
        if request.user.groups.filter(name__iexact='admin').exists() \
                or request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
