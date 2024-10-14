# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
import stripe
from decouple import config

DJANGO_DEBUG = config("DJANGO_DEBUG", default=False, cast=bool)
STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY", default="", cast=str)


if "sk_test" in STRIPE_SECRET_KEY and not DJANGO_DEBUG:
    raise ValueError("Invalid stripe key for prod")

stripe.api_key = STRIPE_SECRET_KEY


def create_customer(name, email, metadata, raw=False):
    """Create a custumer in stripe and return customer id"""
    res = stripe.Customer.create(name=name, email=email, metadata=metadata)
    if raw:
        return res

    stripe_id = res.id
    return stripe_id


def create_product(name="", metadata={}, raw=False):
    """create a product and return the id / raw data."""
    res = stripe.Product.create(name=name, metadata=metadata)

    if raw:
        return res

    return res.id


def create_price(currency, unit_amount, recurring, product, metadata, raw=False):
    res = stripe.Price.create(
        currency=currency,
        unit_amount=unit_amount,
        recurring=recurring,
        metadata=metadata,
        product=product,
    )

    if raw:
        return res

    return res.id
