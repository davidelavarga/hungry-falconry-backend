import re
import uuid

from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.forms import fields
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

MAC_RE = r'^([0-9a-fA-F]{2}([:-]?|$)){6}$'
mac_re = re.compile(MAC_RE)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class MACAddressFormField(fields.RegexField):
    default_error_messages = {
        'invalid': _(u'Enter a valid MAC address.'),
    }

    def __init__(self, *args, **kwargs):
        super(MACAddressFormField, self).__init__(mac_re, *args, **kwargs)


class MACAddressField(models.Field):
    empty_strings_allowed = False

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 17
        super(MACAddressField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "CharField"

    def formfield(self, **kwargs):
        defaults = {'form_class': MACAddressFormField}
        defaults.update(kwargs)
        return super(MACAddressField, self).formfield(**defaults)


class Feeder(models.Model):
    mac_address = MACAddressField(unique=True, null=False, blank=False)
    name_by_user = models.CharField(max_length=20, null=False, blank=False, unique=False, default="Feeder")
    max_portions = models.IntegerField(null=False, blank=False, editable=True, auto_created=True)
    current_portions = models.IntegerField(null=False, blank=True, editable=True, auto_created=True, default=0)
    created_at = models.DateTimeField(auto_now=timezone.now)
    owner = models.ForeignKey("auth.User", related_name='feeders', on_delete=models.CASCADE, null=False, blank=False)
    slug_feeder = models.SlugField(unique=True, auto_created=True, default=uuid.uuid4().hex, editable=False)

    def __str__(self):
        return self.mac_address


class Schedule(models.Model):
    timestamp = models.DateTimeField(primary_key=True)
    feeder = models.ForeignKey('Feeder', related_name='schedules', on_delete=models.CASCADE, null=False, blank=False)
    done = models.BooleanField(default=False)
    slug_scheduler = models.SlugField(unique=True, auto_created=True, default=uuid.uuid4().hex, editable=False)

    def __str__(self):
        return str(self.timestamp)
