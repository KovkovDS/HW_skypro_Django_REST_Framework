from HW_skypro_Django_REST_Framework import settings
import stripe


stripe.api_key = settings.STRIPE_API_KEY


def create_stripe_product(payment):
    """Функция создания продукта в Stripe."""

    stripe_products_list = stripe.Product.list()
    for product in stripe_products_list:
        if payment.paid_course.title != product.name and payment.paid_lesson is None:
            paid_product = payment.paid_course.title
            stripe_product = stripe.Product.create(name=f"{paid_product}")
        elif payment.paid_lesson.title != product.name and payment.paid_lesson.title is not None:
            paid_product = payment.paid_lesson.title
            stripe_product = stripe.Product.create(name=f"{paid_product}")
        else:
            stripe_product = product
        return stripe_product["id"]


def create_stripe_price(payment, stripe_product_id):
    """Функция создания цены в Stripe."""

    return stripe.Price.create(
        currency="rub",
        unit_amount=int(payment.payment_amount * 100),
        product=stripe_product_id,
    )


def create_stripe_session(price):
    """Функция создания сессии платежа в Stripe."""

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")


def checkout_stripe_session(session_id):
    """Функция проверки статуса сессии платежа в Stripe."""

    checkout_session_id = stripe.checkout.Session.retrieve(session_id)
    if session_id in checkout_session_id.get("url"):
        return True
