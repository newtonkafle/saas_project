from django.db import models
from django.contrib.auth.models import Group, Permission
from django.conf import settings
from django.db.models import signals

User = settings.AUTH_USER_MODEL
ALLOW_CUSTOM_GROUPS = True

SUBSCRIPTIONS_PERMISSION = [
    ("advanced", "Advanced Perm"),  # subscriptions.advanced
    ("pro", "Pro Perm"),  # subscriptions.pro
    ("basic", "Basic Perm"),  # subscriptions.basic
]


# Create your models here.
class Subscriptions(models.Model):
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

    class Meta:
        permissions = SUBSCRIPTIONS_PERMISSION

    def __str__(self):
        return f"{self.name}"


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
        if subscription is not None:
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
