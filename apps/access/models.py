from django.contrib.auth.models import User
from django.db import models
from .signals import assign_role

models.signals.post_save.connect(assign_role, sender=User)
