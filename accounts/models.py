from __future__ import unicode_literals

import os

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.urlresolvers import reverse
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _


class AccountManager(BaseUserManager):

    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        account = self.model(email=email, username=email)
        account.set_password(password)
        account.save()
        return account

    def create_superuser(self, email, password, **kwargs):
        account = self.create_user(email, password, **kwargs)
        account.is_admin = True
        account.is_staff = True
        account.is_active = True
        account.is_superuser = True
        account.save()
        return account


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=225, unique=True)
    username = models.CharField(max_length=225, blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    about_me = models.TextField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    contact_number = models.CharField(max_length=13, blank=True)
    profile_pic = models.ImageField(
        'Profile picture', upload_to='profiles',)
    hourly_rate = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)

    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(_('active'), default=False,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    objects = AccountManager()
    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_short_name(self):
        return "{}".format(self.first_name)


class AccountLog(models.Model):
    INVALID = 'invalid'
    VALID = 'valid'
    STATUSES = (
        (INVALID, 'Invalid'),
        (VALID, 'Valid'),
    )

    account = models.ForeignKey(Account)
    ip = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=150, choices=STATUSES, default=INVALID)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.account.email)


class Payroll(models.Model):
    date = models.DateTimeField()
    employee = models.ForeignKey(Account)
    amount_before_deductions = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    description = models.TextField()
    paid = models.BooleanField(default=False)
    date_paid = models.DateTimeField(blank=True, null=True)
    invoice_file = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "{} to {}".format(self.description, self.employee)