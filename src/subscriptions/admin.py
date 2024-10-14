from django.contrib import admin

# Register your models here.
from .models import Subscriptions, UserSubscription, SubscriptionsPrice


class SubscriptionPrice(admin.StackedInline):
    """tabular inline data with associated model -> SubscriptionAdmin"""

    model = SubscriptionsPrice
    extra = 0
    readonly_fields = ["stripe_id"]
    can_delete = False


class SubscriptionAdmin(admin.ModelAdmin):
    inlines = [SubscriptionPrice]
    list_display = ["name", "active"]
    readonly_fields = ["stripe_id"]

    fields = ["stripe_id", "name", "groups", "permissions", "active", "order"]


admin.site.register(Subscriptions, SubscriptionAdmin)
admin.site.register(UserSubscription)
admin.site.register(SubscriptionsPrice)
