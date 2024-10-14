from django.db import models
from django.contrib.auth.models import Group, Permission
from django.conf import settings
from django.db.models import signals
from helpers import billing

User = settings.AUTH_USER_MODEL
ALLOW_CUSTOM_GROUPS = True

SUBSCRIPTIONS_PERMISSION = [
    ("advanced", "Advanced Perm"),  # subscriptions.advanced
    ("pro", "Pro Perm"),  # subscriptions.pro
    ("basic", "Basic Perm"),  # subscriptions.basic
]


# Create your models here.
class Subscriptions(models.Model):
    """Subscription = Stripe prodcut"""

    name = models.CharField(max_length=120)
    groups = models.ManyToManyField(Group)
    active = models.BooleanField(default=True)
    permissions = models.ManyToManyField(
        Permission,
        limit_choices_to={
            "content_type__app_label": "subscriptions",
            "codename__in": [perm[0] for perm in SUBSCRIPTIONS_PERMISSION],
        },
    )
    stripe_id = models.CharField(max_length=120, null=True, blank=True)
    order = models.IntegerField(default=-1, help_text="Ordering on django pricing page")
    featured = models.BooleanField(
        default=True, help_text="featured on Django pricing page"
    )
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.stripe_id:
            stripe_res_id = billing.create_product(
                name=self.name,
                metadata={"subscription_plan_id": self.id},
            )
            self.stripe_id = stripe_res_id
        super().save(*args, **kwargs)

    class Meta:
        permissions = SUBSCRIPTIONS_PERMISSION
        ordering = ["order", "featured", "-updated"]

    def __str__(self):
        return f"{self.name}"


class SubscriptionsPrice(models.Model):
    """
    Subscription Price => Stripe Product Price
    """

    class IntervalChoices(models.TextChoices):
        MONTHLY = ("month", "MONTHLY")
        YEARLY = ("year", "YEARLY")

    subscription = models.ForeignKey(
        Subscriptions, on_delete=models.SET_NULL, null=True
    )
    stripe_id = models.CharField(max_length=120, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=99.99)
    interval = models.CharField(
        max_length=120, default=IntervalChoices.MONTHLY, choices=IntervalChoices.choices
    )
    order = models.IntegerField(default=-1, help_text="Ordering on django pricing page")
    featured = models.BooleanField(
        default=True, help_text="featured on Django pricing page"
    )
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "featured", "-updated"]

    @property
    def product_stripe_id(self):
        if not self.subscription:
            return None
        return self.subscription.stripe_id

    @property
    def stripe_price(self):
        """remove decimal places"""
        return int(self.price * 100)

    @property
    def stripe_currency(self):
        return "usd"

    def save(self, *args, **kwargs):
        if not self.stripe_id and self.product_stripe_id is not None:
            stripe_id = billing.create_price(
                currency=self.stripe_currency,
                unit_amount=self.stripe_price,
                recurring={"interval": self.interval},
                product=self.product_stripe_id,
                metadata={"subscription_plan_price_id": self.id},
            )
            self.stripe_id = stripe_id
        super().save(*args, **kwargs)
        if self.featured and self.subscription:
            qs = SubscriptionsPrice.objects.filter(
                subscription=self.subscription, interval=self.interval
            ).exclude(id=self.id)

            qs.update(featured=False)


class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(
        Subscriptions, on_delete=models.SET_NULL, null=True, blank=True
    )
    active = models.BooleanField(default=True)


def user_sub_post_save(sender, instance, *args, **kwargs):
    """add user to the group designated by subscriptions models."""
    user_sub_instance = instance
    user = user_sub_instance.user
    subscription = user_sub_instance.subscription
    groups_ids = []
    if subscription is not None:
        groups = subscription.groups.all()
        groups_ids = groups.values_list("id", flat=True)

        if not ALLOW_CUSTOM_GROUPS:
            user.groups.set(groups)
        else:
            # get all usual subscriptions group ids as set
            subs_qs = Subscriptions.objects.filter(active=True)
            subs_qs.exclude(id=subscription.id)
            subs_groups = subs_qs.values_list("groups__id", flat=True)
            subs_groups_set = set(subs_groups)

            # creating set of currnet groups ids that you want user to be in.
            groups_ids_set = set(groups_ids)

            # set of groups ids user currently in.
            current_groups = user.groups.all().values_list("id", flat=True)
            current_groups_ids_set = set(current_groups)

            # filtering usual groups ids to keep custom groups ids.
            custom_groups_ids_set = current_groups_ids_set - subs_groups_set

            # setting groups with custom groups and the new subs group.
            final_groups_ids_set = list(groups_ids_set | custom_groups_ids_set)

            user.groups.set(final_groups_ids_set)


signals.post_save.connect(user_sub_post_save, sender=UserSubscription)
