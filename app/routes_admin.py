from functools import wraps

from flask import (Blueprint, render_template, request, redirect, url_for,
                    session, flash, jsonify, abort)
from werkzeug.security import check_password_hash, generate_password_hash

from . import models
from . import uploads
from .seed_data import slugify

admin_bp = Blueprint("admin", __name__)


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin.login", next=request.path))
        return f(*args, **kwargs)
    return wrapper


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("admin_logged_in"):
        return redirect(url_for("admin.dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = models.get_admin_by_username(username)
        if user and check_password_hash(user["password_hash"], password):
            session["admin_logged_in"] = True
            session["admin_username"] = username
            flash("Welcome back!", "success")
            nxt = request.args.get("next") or url_for("admin.dashboard")
            return redirect(nxt)
        flash("Invalid username or password.", "error")

    return render_template("admin/login.html", settings=models.get_settings())


@admin_bp.route("/logout")
def logout():
    session.pop("admin_logged_in", None)
    session.pop("admin_username", None)
    flash("Logged out successfully.", "success")
    return redirect(url_for("admin.login"))


@admin_bp.route("/")
@login_required
def dashboard():
    galleries = models.get_galleries(active_only=False)
    bookings = models.get_recent_bookings(limit=8)
    total_revenue = models.sum_paid_revenue()
    total_bookings = models.count_paid_bookings()
    total_ticket_visitors = models.sum_paid_visitors()
    total_live_visitors = sum(g.current_occupancy for g in galleries)
    total_chats = models.count_user_chat_messages()

    chart_labels = [g.name for g in galleries]
    chart_occ = [g.current_occupancy for g in galleries]
    chart_cap = [g.max_occupancy for g in galleries]

    stats = dict(total_revenue=total_revenue, total_bookings=total_bookings,
                 total_ticket_visitors=total_ticket_visitors, total_live_visitors=total_live_visitors,
                 total_chats=total_chats, total_galleries=len(galleries))

    return render_template("admin/dashboard.html", galleries=galleries, bookings=bookings, stats=stats,
                            chart_labels=chart_labels, chart_occ=chart_occ, chart_cap=chart_cap,
                            settings=models.get_settings())


# ------------------------------------------------------------------ galleries --

@admin_bp.route("/galleries")
@login_required
def galleries_admin():
    galleries = models.get_galleries(active_only=False)
    return render_template("admin/galleries.html", galleries=galleries, settings=models.get_settings())


@admin_bp.route("/galleries/<int:gallery_id>/edit", methods=["GET", "POST"])
@login_required
def edit_gallery(gallery_id):
    gallery = models.get_gallery(gallery_id)
    if not gallery:
        abort(404)

    if request.method == "POST":
        name = request.form.get("name", gallery.name).strip()
        models.update_gallery(
            gallery_id,
            name=name, slug=slugify(name),
            era_order=int(request.form.get("era_order") or gallery.era_order),
            period=request.form.get("period", gallery.period).strip(),
            icon=request.form.get("icon", gallery.icon).strip() or gallery.icon,
            wiki_topic=request.form.get("wiki_topic", gallery.wiki_topic).strip(),
            short_description=request.form.get("short_description", gallery.short_description).strip(),
            description=request.form.get("description", gallery.description).strip(),
            history=request.form.get("history", gallery.history).strip(),
            highlights=request.form.get("highlights", gallery.highlights).strip(),
            monuments=request.form.get("monuments", gallery.monuments_raw).strip(),
            max_occupancy=int(request.form.get("max_occupancy") or gallery.max_occupancy),
            current_occupancy=int(request.form.get("current_occupancy") or gallery.current_occupancy),
            is_active=1 if request.form.get("is_active") else 0,
        )
        flash(f"{name} gallery updated successfully.", "success")
        return redirect(url_for("admin.galleries_admin"))

    return render_template("admin/gallery_form.html", gallery=gallery)


@admin_bp.route("/galleries/new", methods=["GET", "POST"])
@login_required
def new_gallery():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        models.create_gallery(
            name=name, slug=slugify(name),
            era_order=int(request.form.get("era_order") or (models.count_galleries() + 1)),
            period=request.form.get("period", "").strip(),
            icon=request.form.get("icon", "🏺").strip() or "🏺",
            wiki_topic=request.form.get("wiki_topic", "").strip(),
            short_description=request.form.get("short_description", "").strip(),
            description=request.form.get("description", "").strip(),
            history=request.form.get("history", "").strip(),
            highlights=request.form.get("highlights", "").strip(),
            monuments=request.form.get("monuments", "").strip(),
            max_occupancy=int(request.form.get("max_occupancy") or 150),
            current_occupancy=int(request.form.get("current_occupancy") or 0),
            is_active=1,
        )
        flash(f"{name} gallery added successfully.", "success")
        return redirect(url_for("admin.galleries_admin"))

    return render_template("admin/gallery_form.html", gallery=None)


@admin_bp.route("/galleries/<int:gallery_id>/delete", methods=["POST"])
@login_required
def delete_gallery(gallery_id):
    gallery = models.get_gallery(gallery_id)
    if not gallery:
        abort(404)
    models.update_gallery(gallery_id, is_active=0)
    flash(f"{gallery.name} gallery deactivated.", "success")
    return redirect(url_for("admin.galleries_admin"))


@admin_bp.route("/galleries/<int:gallery_id>/occupancy", methods=["POST"])
@login_required
def quick_occupancy(gallery_id):
    delta = request.json.get("delta", 0) if request.is_json else int(request.form.get("delta", 0))
    gallery = models.adjust_occupancy(gallery_id, delta)
    if not gallery:
        abort(404)
    return jsonify(gallery.to_dict())


# ------------------------------------------------------------------- settings --

@admin_bp.route("/settings", methods=["GET", "POST"])
@login_required
def settings_admin():
    if request.method == "POST":
        fields = [
            "site_name", "site_short_name", "tagline", "hero_wiki_topic", "about_text",
            "address", "phone", "email", "timings", "established_year", "total_artifacts",
            "price_indian", "price_foreign", "price_student", "price_child", "map_embed",
        ]
        values = {f: request.form.get(f, "").strip() for f in fields}

        if request.form.get("remove_logo"):
            values["logo_url"] = ""
        else:
            logo_file = request.files.get("logo")
            saved = uploads.save_upload(logo_file)
            if saved:
                values["logo_url"] = "uploads/" + saved

        models.update_settings(values)
        flash("Site settings updated successfully.", "success")
        return redirect(url_for("admin.settings_admin"))

    return render_template("admin/settings.html", settings=models.get_settings())


# -------------------------------------------------------------------- notices --

@admin_bp.route("/notices")
@login_required
def notices_admin():
    notices = models.get_all_notices()
    return render_template("admin/notices.html", notices=notices, settings=models.get_settings())


@admin_bp.route("/notices/new", methods=["POST"])
@login_required
def new_notice():
    text = request.form.get("text", "").strip()
    if text:
        models.create_notice(text)
        flash("Notice published.", "success")
    return redirect(url_for("admin.notices_admin"))


@admin_bp.route("/notices/<int:notice_id>/toggle", methods=["POST"])
@login_required
def toggle_notice(notice_id):
    models.toggle_notice(notice_id)
    return redirect(url_for("admin.notices_admin"))


@admin_bp.route("/notices/<int:notice_id>/delete", methods=["POST"])
@login_required
def delete_notice(notice_id):
    models.delete_notice(notice_id)
    flash("Notice removed.", "success")
    return redirect(url_for("admin.notices_admin"))


# ------------------------------------------------------------------- bookings --

@admin_bp.route("/bookings")
@login_required
def bookings_admin():
    bookings = models.get_all_bookings()
    return render_template("admin/bookings.html", bookings=bookings, settings=models.get_settings())


@admin_bp.route("/chats")
@login_required
def chats_admin():
    sessions = models.get_all_chat_sessions()
    return render_template("admin/chats.html", sessions=sessions, settings=models.get_settings())


@admin_bp.route("/messages")
@login_required
def messages_admin():
    messages = models.get_contact_messages()
    return render_template("admin/messages.html", messages=messages, settings=models.get_settings())


@admin_bp.route("/account", methods=["GET", "POST"])
@login_required
def account():
    username = session.get("admin_username")
    user = models.get_admin_by_username(username) if username else None
    if request.method == "POST":
        new_password = request.form.get("new_password", "").strip()
        if new_password and user:
            models.update_admin_password(username, generate_password_hash(new_password))
            flash("Password updated successfully.", "success")
    return render_template("admin/account.html", user=user, settings=models.get_settings())


# -------------------------------------------------------------------- media --

@admin_bp.route("/media")
@login_required
def media_admin():
    media = models.get_all_media()
    return render_template("admin/media.html", media=media, settings=models.get_settings())


@admin_bp.route("/media/upload", methods=["POST"])
@login_required
def upload_media():
    file = request.files.get("image")
    alt_text = request.form.get("alt_text", "").strip()
    filename = uploads.save_upload(file)
    if filename:
        models.add_media(filename, file.filename, alt_text)
        flash(f"Image uploaded. Use it anywhere with: media:{filename}", "success")
    else:
        flash("Please choose a valid image file (png, jpg, jpeg, gif, webp, svg).", "error")
    return redirect(url_for("admin.media_admin"))


@admin_bp.route("/media/<int:media_id>/delete", methods=["POST"])
@login_required
def delete_media(media_id):
    item = models.get_media(media_id)
    if item:
        uploads.delete_upload(item.filename)
        models.delete_media(media_id)
        flash("Image deleted.", "success")
    return redirect(url_for("admin.media_admin"))


# ---------------------------------------------------------------- employees --

@admin_bp.route("/employees")
@login_required
def employees_admin():
    employees = models.get_employees(active_only=False)
    return render_template("admin/employees.html", employees=employees, settings=models.get_settings())


@admin_bp.route("/employees/new", methods=["GET", "POST"])
@login_required
def new_employee():
    if request.method == "POST":
        photo = uploads.save_upload(request.files.get("photo"))
        models.create_employee(
            name=request.form.get("name", "").strip(),
            designation=request.form.get("designation", "").strip(),
            department=request.form.get("department", "").strip(),
            bio=request.form.get("bio", "").strip(),
            photo_path=("uploads/" + photo) if photo else "",
            email=request.form.get("email", "").strip(),
            phone=request.form.get("phone", "").strip(),
            display_order=int(request.form.get("display_order") or 0),
            is_active=1,
        )
        flash("Employee added successfully.", "success")
        return redirect(url_for("admin.employees_admin"))
    return render_template("admin/employee_form.html", employee=None)


@admin_bp.route("/employees/<int:employee_id>/edit", methods=["GET", "POST"])
@login_required
def edit_employee(employee_id):
    employee = models.get_employee(employee_id)
    if not employee:
        abort(404)
    if request.method == "POST":
        photo = uploads.save_upload(request.files.get("photo"))
        photo_path = ("uploads/" + photo) if photo else employee.photo_path
        models.update_employee(
            employee_id,
            name=request.form.get("name", employee.name).strip(),
            designation=request.form.get("designation", "").strip(),
            department=request.form.get("department", "").strip(),
            bio=request.form.get("bio", "").strip(),
            photo_path=photo_path,
            email=request.form.get("email", "").strip(),
            phone=request.form.get("phone", "").strip(),
            display_order=int(request.form.get("display_order") or 0),
            is_active=1 if request.form.get("is_active") else 0,
        )
        flash("Employee updated successfully.", "success")
        return redirect(url_for("admin.employees_admin"))
    return render_template("admin/employee_form.html", employee=employee)


@admin_bp.route("/employees/<int:employee_id>/delete", methods=["POST"])
@login_required
def delete_employee(employee_id):
    employee = models.get_employee(employee_id)
    if employee:
        if employee.photo_path:
            uploads.delete_upload(employee.photo_path.replace("uploads/", "", 1))
        models.delete_employee(employee_id)
        flash(f"{employee.name} removed.", "success")
    return redirect(url_for("admin.employees_admin"))


# -------------------------------------------------------------------- pages --

@admin_bp.route("/pages")
@login_required
def pages_admin():
    pages = models.get_pages(published_only=False)
    return render_template("admin/pages.html", pages=pages, settings=models.get_settings())


@admin_bp.route("/pages/new", methods=["GET", "POST"])
@login_required
def new_page():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        models.create_page(
            title=title, slug=slugify(title),
            content=request.form.get("content", "").strip(),
            is_published=1 if request.form.get("is_published") else 0,
        )
        flash("Page created successfully.", "success")
        return redirect(url_for("admin.pages_admin"))
    return render_template("admin/page_form.html", page=None)


@admin_bp.route("/pages/<int:page_id>/edit", methods=["GET", "POST"])
@login_required
def edit_page(page_id):
    page = models.get_page(page_id)
    if not page:
        abort(404)
    if request.method == "POST":
        title = request.form.get("title", page.title).strip()
        models.update_page(
            page_id, title=title, slug=slugify(title),
            content=request.form.get("content", "").strip(),
            is_published=1 if request.form.get("is_published") else 0,
        )
        flash("Page updated successfully.", "success")
        return redirect(url_for("admin.pages_admin"))
    return render_template("admin/page_form.html", page=page)


@admin_bp.route("/pages/<int:page_id>/delete", methods=["POST"])
@login_required
def delete_page(page_id):
    models.delete_page(page_id)
    flash("Page deleted.", "success")
    return redirect(url_for("admin.pages_admin"))


# -------------------------------------------------------------------- links --

@admin_bp.route("/links")
@login_required
def links_admin():
    nav_links = models.get_links(location="nav", active_only=False)
    footer_links = models.get_links(location="footer", active_only=False)
    return render_template("admin/links.html", nav_links=nav_links, footer_links=footer_links,
                            settings=models.get_settings())


@admin_bp.route("/links/new", methods=["POST"])
@login_required
def new_link():
    models.create_link(
        label=request.form.get("label", "").strip(),
        url=request.form.get("url", "").strip(),
        location=request.form.get("location", "footer"),
        sort_order=int(request.form.get("sort_order") or 0),
    )
    flash("Link added.", "success")
    return redirect(url_for("admin.links_admin"))


@admin_bp.route("/links/<int:link_id>/edit", methods=["POST"])
@login_required
def edit_link(link_id):
    link = models.get_link(link_id)
    if link:
        models.update_link(
            link_id,
            label=request.form.get("label", link.label).strip(),
            url=request.form.get("url", link.url).strip(),
            location=request.form.get("location", link.location),
            sort_order=int(request.form.get("sort_order") or link.sort_order),
            is_active=1 if request.form.get("is_active") else 0,
        )
        flash("Link updated.", "success")
    return redirect(url_for("admin.links_admin"))


@admin_bp.route("/links/<int:link_id>/delete", methods=["POST"])
@login_required
def delete_link(link_id):
    models.delete_link(link_id)
    flash("Link removed.", "success")
    return redirect(url_for("admin.links_admin"))


# ---------------------------------------------------------------- analytics --

@admin_bp.route("/analytics")
@login_required
def analytics_admin():
    total_visits = models.count_visits()
    by_section = models.visits_by_section()
    daily = models.visits_last_n_days(7)
    recent = models.get_recent_visits(limit=50)

    return render_template(
        "admin/analytics.html", settings=models.get_settings(),
        total_visits=total_visits, by_section=by_section, daily=daily, recent=recent,
        section_labels=[s for s, _ in by_section], section_counts=[c for _, c in by_section],
        daily_labels=[d for d, _ in daily], daily_counts=[c for _, c in daily],
    )
