from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, abort

from . import models
from . import payments

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def home():
    settings = models.get_settings()
    galleries = models.get_galleries(active_only=True)
    notices = models.get_active_notices()
    total_visitors = sum(g.current_occupancy for g in galleries)
    stats = {
        "galleries": len(galleries),
        "visitors_today": total_visitors,
        "artifacts": settings["total_artifacts"],
        "established": settings["established_year"],
    }
    return render_template("index.html", galleries=galleries, stats=stats,
                            settings=settings, notices=notices)


@public_bp.route("/galleries")
def galleries_list():
    q = request.args.get("q", "").strip()
    galleries = models.search_galleries(q) if q else models.get_galleries(active_only=True)
    settings = models.get_settings()
    return render_template("galleries.html", galleries=galleries, q=q, settings=settings)


@public_bp.route("/gallery/<slug>")
def gallery_detail(slug):
    gallery = models.get_gallery_by_slug(slug)
    if not gallery:
        abort(404)
    related = [g for g in models.get_galleries(active_only=True) if g.id != gallery.id]
    related = sorted(related, key=lambda g: abs(g.era_order - gallery.era_order))[:3]
    settings = models.get_settings()
    return render_template("gallery_detail.html", gallery=gallery, related=related, settings=settings)


@public_bp.route("/visit", methods=["GET", "POST"])
def visit():
    settings = models.get_settings()

    if request.method == "GET":
        return render_template("visit.html", settings=settings, stripe_enabled=payments.stripe_enabled())

    name = request.form.get("visitor_name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    visit_date = request.form.get("visit_date", "").strip()

    def _qty(field):
        try:
            return max(0, min(int(request.form.get(field, 0) or 0), 50))
        except ValueError:
            return 0

    qty_indian = _qty("qty_indian")
    qty_foreign = _qty("qty_foreign")
    qty_student = _qty("qty_student")
    qty_child = _qty("qty_child")
    total_qty = qty_indian + qty_foreign + qty_student + qty_child

    if not name or not email:
        flash("Please provide your name and email to book tickets.", "error")
        return redirect(url_for("public.visit"))

    if total_qty < 1:
        flash("Please select at least one ticket.", "error")
        return redirect(url_for("public.visit"))

    amount = (
        qty_indian * int(settings["price_indian"] or 0)
        + qty_foreign * int(settings["price_foreign"] or 0)
        + qty_student * int(settings["price_student"] or 0)
        + qty_child * int(settings["price_child"] or 0)
    )

    provider = "stripe" if payments.stripe_enabled() else "demo"
    booking = models.create_booking(
        visitor_name=name, email=email, phone=phone, visit_date=visit_date,
        qty_indian=qty_indian, qty_foreign=qty_foreign, qty_student=qty_student, qty_child=qty_child,
        amount=amount, currency="INR", payment_provider=provider,
    )

    if payments.stripe_enabled() and amount > 0:
        try:
            success_url = url_for("public.booking_success", _external=True)
            cancel_url = url_for("public.booking_cancel", _external=True)
            session = payments.create_checkout_session(booking, settings["site_name"], success_url, cancel_url)
            return redirect(session.url, code=303)
        except Exception as e:
            current_app.logger.warning(f"Stripe error, falling back to demo checkout: {e}")

    if amount == 0:
        # Free entry (e.g. children-only booking) — confirm instantly.
        models.mark_booking_paid(booking.reference, "FREE-ENTRY")
        return redirect(url_for("public.booking_success", ref=booking.reference))

    return redirect(url_for("public.demo_checkout", reference=booking.reference))


@public_bp.route("/checkout/demo/<reference>")
def demo_checkout(reference):
    booking = models.get_booking_by_reference(reference)
    if not booking:
        abort(404)
    settings = models.get_settings()
    return render_template("demo_checkout.html", booking=booking, settings=settings)


@public_bp.route("/checkout/demo/<reference>/pay", methods=["POST"])
def demo_pay(reference):
    booking = models.get_booking_by_reference(reference)
    if not booking:
        abort(404)
    models.mark_booking_paid(reference, "DEMO-" + booking.reference)
    return redirect(url_for("public.booking_success", ref=booking.reference))


@public_bp.route("/booking/success")
def booking_success():
    ref = request.args.get("ref")
    session_id = request.args.get("session_id")
    booking = models.get_booking_by_reference(ref) if ref else None

    if booking and session_id and booking.payment_status != "paid":
        try:
            paid, pid = payments.verify_checkout_session(session_id)
            if paid:
                models.mark_booking_paid(booking.reference, pid)
                booking = models.get_booking_by_reference(ref)
        except Exception as e:
            current_app.logger.warning(f"Could not verify stripe session: {e}")

    return render_template("booking_success.html", booking=booking, settings=models.get_settings())


@public_bp.route("/booking/cancel")
def booking_cancel():
    ref = request.args.get("ref")
    booking = models.get_booking_by_reference(ref) if ref else None
    if booking and booking.payment_status == "pending":
        models.mark_booking_failed(ref)
    return render_template("booking_cancel.html", booking=booking, settings=models.get_settings())


@public_bp.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()
    subject = request.form.get("subject", "General Inquiry").strip() or "General Inquiry"
    if name and email and message:
        models.add_contact_message(name, email, message, subject)
        flash("Thank you for reaching out. Our team will respond within 2 working days.", "success")
    else:
        flash("Please fill in all fields.", "error")
    return redirect(url_for("public.home") + "#contact")


@public_bp.route("/our-team")
def our_team():
    employees = models.get_employees(active_only=True)
    settings = models.get_settings()
    return render_template("our_team.html", employees=employees, settings=settings)


@public_bp.route("/page/<slug>")
def custom_page(slug):
    page = models.get_page_by_slug(slug)
    if not page:
        abort(404)
    settings = models.get_settings()
    return render_template("custom_page.html", page=page, settings=settings)


@public_bp.route("/chat-page")
def chat_page():
    galleries = models.get_galleries(active_only=True)
    settings = models.get_settings()
    return render_template("chat.html", galleries=galleries, settings=settings)
