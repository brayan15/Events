from __future__ import unicode_literals

import uuid
from django.db import models
from django.utils import timezone
from events.events.models import Event
from events.users.models import User


# Create your models here.

class Transaction(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4,
                            editable=False,
                            unique=True)
    event = models.ForeignKey(Event)
    user = models.ForeignKey(User)
    paid = models.BooleanField(default=False)
    value = models.PositiveIntegerField(default=0)
    valid = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    applied_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    def success(self):
        user = self.user
        user.refresh_from_db()
        user.save()
        self.applied = True
        self.applied_at = timezone.now()
        self.valid = True
        self.save()

    def set_invalid(self):
        self.applied = True
        self.applied_at = timezone.now()
        self.valid = False
        self.save()

    def __unicode__(self):
        return "{}| Value:{}| {}".format(
            self.user,
            self.value,
            "Paid" if self.paid else "Not Paid")

