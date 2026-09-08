"""
Payment gateway integration (Stripe).

If STRIPE_SECRET_KEY is not configured, the booking flow automatically runs
in DEMO MODE: the booking is created and instantly marked "paid" so the
whole product — including receipts and the admin dashboard — is fully
testable without needing real payment credentials. Once real Stripe keys
are added to the environment, live/test checkout kicks in automatically.
"""
import os


def stripe_enabled():
    return bool(os.getenv("STRIPE_SECRET_KEY", "").strip())


def create_checkout_session(booking, site_name, success_url, cancel_url):
    import stripe
    stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

    description_bits = []
    if booking.qty_indian:
        description_bits.append(f"{booking.qty_indian} Indian")
    if booking.qty_foreign:
        description_bits.append(f"{booking.qty_foreign} Foreign National")
    if booking.qty_student:
        description_bits.append(f"{booking.qty_student} Student")
    if booking.qty_child:
        description_bits.append(f"{booking.qty_child} Child (free)")

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": booking.currency.lower(),
                "product_data": {
                    "name": f"{site_name} — Entry Ticket(s)",
                    "description": f"{', '.join(description_bits)} — Visit date: "
                                    f"{booking.visit_date or 'Flexible'}",
                },
                "unit_amount": int(booking.amount * 100),
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url=success_url + f"?ref={booking.reference}&session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=cancel_url + f"?ref={booking.reference}",
        customer_email=booking.email,
        metadata={"booking_reference": booking.reference},
    )
    return session


def verify_checkout_session(session_id):
    import stripe
    stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
    session = stripe.checkout.Session.retrieve(session_id)
    return session.payment_status == "paid", session.id
