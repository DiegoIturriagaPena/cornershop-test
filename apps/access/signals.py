from django.contrib.auth.models import Group


def assign_role(sender, instance, created, **kwargs):
    """Assign role of "clients" when a client registers."""
    if created:
        try:
            group = Group.objects.filter(name__iexact='clients').first()
            instance.groups.add(group)
            instance.save()
        except Exception as exc:
            print(exc)
