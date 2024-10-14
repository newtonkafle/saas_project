from django.db import models
from django.conf import settings
from helpers import billing
from allauth.account.signals import (
    email_confirmed as allauth_email_confirmed,
    user_signed_up as allauth_user_signed_up,
)

User = settings.AUTH_USER_MODEL
# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=120, blank=True, null=True)
    init_email = models.EmailField(blank=True, null=True)
    init_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}"

    def save(self, *args, **kwargs):
        if not self.stripe_id:
            if self.init_email_verified:
                stripe_res_id = billing.create_customer(
                    name=self.user.username,
                    email=self.init_email,
                    metadata={"user_id": self.user_id, "username": self.username},
                )
                self.stripe_id = stripe_res_id
        super().save(*args, **kwargs)


def allauth_user_register_handler(request, user, *args, **kwargs):
    """add a customer into django customer models when user signed up with email(all_auth)"""
    email = user.email
    Customer.objects.create(user=user, init_email=email, init_email_verified=False)


def allauth_email_confirmed_handler(request, email_address, *args, **kwargs):
    """change init_email_confirmed to be true on customer model when email is verified by user."""
    try:
        cust_obj = Customer.objects.get(init_email=email_address)
    except:
        print("Email not found")
    else:
        cust_obj.init_email_verified = True
        cust_obj.save()


allauth_user_signed_up.connect(allauth_user_register_handler)
allauth_email_confirmed.connect(allauth_email_confirmed_handler)
