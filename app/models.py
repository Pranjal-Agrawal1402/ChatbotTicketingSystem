import uuid
from datetime import datetime

from . import db


def gen_ref():
    return uuid.uuid4().hex[:10].upper()


def _parse_dt(s):
    if not s:
        return datetime.utcnow()
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S.%f"):
        try:
            return datetime.strptime(s, fmt)
        except (ValueError, TypeError):
            continue
    return datetime.utcnow()


def parse_pipe_list(text):
    return [t.strip() for t in (text or "").split("|") if t.strip()]


def parse_monuments(text):
    """Each line: Name :: wiki_topic :: one-line description"""
    items = []
    for line in (text or "").splitlines():
        line = line.strip()
        if not line:
            continue
        parts = [p.strip() for p in line.split("::")]
        name = parts[0] if len(parts) > 0 else ""
        wiki_topic = parts[1] if len(parts) > 1 else name.replace(" ", "_")
        blurb = parts[2] if len(parts) > 2 else ""
        if name:
            items.append({"name": name, "wiki_topic": wiki_topic, "blurb": blurb})
    return items


class Gallery:
    def __init__(self, row):
        d = dict(row)
        self.id = d["id"]
        self.name = d["name"]
        self.slug = d["slug"]
        self.era_order = d["era_order"]
        self.period = d["period"]
        self.icon = d["icon"]
        self.wiki_topic = d["wiki_topic"]
        self.short_description = d["short_description"]
        self.description = d["description"]
        self.history = d["history"]
        self.highlights = d["highlights"]
        self.monuments_raw = d["monuments"]
        self.max_occupancy = d["max_occupancy"]
        self.current_occupancy = d["current_occupancy"]
        self.is_active = bool(d["is_active"])
        self.created_at = _parse_dt(d["created_at"])

    @property
    def highlight_list(self):
        return parse_pipe_list(self.highlights)

    @property
    def monument_list(self):
        return parse_monuments(self.monuments_raw)

    @property
    def available_slots(self):
        return max(self.max_occupancy - self.current_occupancy, 0)

    @property
    def occupancy_percent(self):
        if not self.max_occupancy:
            return 0
        return min(round((self.current_occupancy / self.max_occupancy) * 100), 100)

    @property
    def status(self):
        pct = self.occupancy_percent
        if pct >= 95:
            return "Full"
        if pct >= 70:
            return "Busy"
        return "Open"

    def to_dict(self):
        return {
            "id": self.id, "name": self.name, "slug": self.slug, "period": self.period,
            "icon": self.icon, "short_description": self.short_description,
            "current_occupancy": self.current_occupancy, "max_occupancy": self.max_occupancy,
            "available_slots": self.available_slots, "occupancy_percent": self.occupancy_percent,
            "status": self.status,
        }


class Booking:
    def __init__(self, row):
        d = dict(row)
        self.id = d["id"]
        self.reference = d["reference"]
        self.visitor_name = d["visitor_name"]
        self.email = d["email"]
        self.phone = d["phone"]
        self.visit_date = d["visit_date"]
        self.qty_indian = d["qty_indian"]
        self.qty_foreign = d["qty_foreign"]
        self.qty_student = d["qty_student"]
        self.qty_child = d["qty_child"]
        self.amount = d["amount"]
        self.currency = d["currency"]
        self.payment_status = d["payment_status"]
        self.payment_provider = d["payment_provider"]
        self.payment_id = d["payment_id"]
        self.created_at = _parse_dt(d["created_at"])

    @property
    def total_tickets(self):
        return self.qty_indian + self.qty_foreign + self.qty_student + self.qty_child

    def to_dict(self):
        return {
            "id": self.id, "reference": self.reference, "visitor_name": self.visitor_name,
            "email": self.email, "total_tickets": self.total_tickets, "amount": self.amount,
            "currency": self.currency, "payment_status": self.payment_status,
            "created_at": self.created_at.strftime("%d %b %Y, %H:%M"),
        }


class ChatMessage:
    def __init__(self, row):
        d = dict(row)
        self.id = d["id"]
        self.session_id = d["session_id"]
        self.role = d["role"]
        self.message = d["message"]
        self.created_at = _parse_dt(d["created_at"])


class ContactMessage:
    def __init__(self, row):
        d = dict(row)
        self.id = d["id"]
        self.name = d["name"]
        self.email = d["email"]
        self.message = d["message"]
        self.subject = d.get("subject", "General Inquiry")
        self.created_at = _parse_dt(d["created_at"])


class Notice:
    def __init__(self, row):
        d = dict(row)
        self.id = d["id"]
        self.text = d["text"]
        self.is_active = bool(d["is_active"])
        self.created_at = _parse_dt(d["created_at"])


class Media:
    def __init__(self, row):
        d = dict(row)
        self.id = d["id"]
        self.filename = d["filename"]
        self.original_name = d["original_name"]
        self.alt_text = d["alt_text"]
        self.uploaded_at = _parse_dt(d["uploaded_at"])


class Employee:
    def __init__(self, row):
        d = dict(row)
        self.id = d["id"]
        self.name = d["name"]
        self.designation = d["designation"]
        self.department = d["department"]
        self.bio = d["bio"]
        self.photo_path = d["photo_path"]
        self.email = d["email"]
        self.phone = d["phone"]
        self.display_order = d["display_order"]
        self.is_active = bool(d["is_active"])
        self.created_at = _parse_dt(d["created_at"])


class Page:
    def __init__(self, row):
        d = dict(row)
        self.id = d["id"]
        self.title = d["title"]
        self.slug = d["slug"]
        self.content = d["content"]
        self.is_published = bool(d["is_published"])
        self.created_at = _parse_dt(d["created_at"])
        self.updated_at = _parse_dt(d["updated_at"])


class Link:
    def __init__(self, row):
        d = dict(row)
        self.id = d["id"]
        self.label = d["label"]
        self.url = d["url"]
        self.location = d["location"]
        self.sort_order = d["sort_order"]
        self.is_active = bool(d["is_active"])


# --------------------------------------------------------------- galleries --

def get_galleries(active_only=True):
    if active_only:
        rows = db.query("SELECT * FROM galleries WHERE is_active = 1 ORDER BY era_order ASC")
    else:
        rows = db.query("SELECT * FROM galleries ORDER BY era_order ASC")
    return [Gallery(r) for r in rows]


def search_galleries(q):
    like = f"%{q}%"
    rows = db.query(
        "SELECT * FROM galleries WHERE is_active = 1 AND "
        "(name LIKE ? OR period LIKE ? OR short_description LIKE ?) ORDER BY era_order ASC",
        (like, like, like),
    )
    return [Gallery(r) for r in rows]


def get_gallery(gallery_id):
    row = db.query("SELECT * FROM galleries WHERE id = ?", (gallery_id,), one=True)
    return Gallery(row) if row else None


def get_gallery_by_slug(slug, active_only=True):
    if active_only:
        row = db.query("SELECT * FROM galleries WHERE slug = ? AND is_active = 1", (slug,), one=True)
    else:
        row = db.query("SELECT * FROM galleries WHERE slug = ?", (slug,), one=True)
    return Gallery(row) if row else None


def count_galleries():
    row = db.query("SELECT COUNT(*) c FROM galleries", one=True)
    return row["c"] if row else 0


def create_gallery(**fields):
    cols = ", ".join(fields.keys())
    placeholders = ", ".join(["?"] * len(fields))
    return db.execute(f"INSERT INTO galleries ({cols}) VALUES ({placeholders})", tuple(fields.values()))


def update_gallery(gallery_id, **fields):
    sets = ", ".join(f"{k} = ?" for k in fields.keys())
    db.execute(f"UPDATE galleries SET {sets} WHERE id = ?", tuple(fields.values()) + (gallery_id,))


def adjust_occupancy(gallery_id, delta):
    gallery = get_gallery(gallery_id)
    if not gallery:
        return None
    new_val = max(0, min(gallery.current_occupancy + delta, gallery.max_occupancy))
    update_gallery(gallery_id, current_occupancy=new_val)
    return get_gallery(gallery_id)


# --------------------------------------------------------------- bookings --

def create_booking(visitor_name, email, phone, visit_date, qty_indian, qty_foreign, qty_student,
                    qty_child, amount, currency="INR", payment_provider="demo"):
    reference = gen_ref()
    booking_id = db.execute(
        "INSERT INTO bookings (reference, visitor_name, email, phone, visit_date, qty_indian, "
        "qty_foreign, qty_student, qty_child, amount, currency, payment_status, payment_provider) "
        "VALUES (?,?,?,?,?,?,?,?,?,?,?, 'pending', ?)",
        (reference, visitor_name, email, phone, visit_date, qty_indian, qty_foreign, qty_student,
         qty_child, amount, currency, payment_provider),
    )
    return get_booking(booking_id)


def get_booking(booking_id):
    row = db.query("SELECT * FROM bookings WHERE id = ?", (booking_id,), one=True)
    return Booking(row) if row else None


def get_booking_by_reference(reference):
    row = db.query("SELECT * FROM bookings WHERE reference = ?", (reference,), one=True)
    return Booking(row) if row else None


def mark_booking_paid(reference, payment_id):
    db.execute("UPDATE bookings SET payment_status = 'paid', payment_id = ? WHERE reference = ?",
               (payment_id, reference))


def mark_booking_failed(reference):
    db.execute("UPDATE bookings SET payment_status = 'failed' WHERE reference = ?", (reference,))


def get_all_bookings():
    rows = db.query("SELECT * FROM bookings ORDER BY created_at DESC")
    return [Booking(r) for r in rows]


def get_recent_bookings(limit=8):
    rows = db.query("SELECT * FROM bookings ORDER BY created_at DESC LIMIT ?", (limit,))
    return [Booking(r) for r in rows]


def sum_paid_revenue():
    row = db.query("SELECT COALESCE(SUM(amount),0) s FROM bookings WHERE payment_status = 'paid'", one=True)
    return row["s"] if row else 0


def count_paid_bookings():
    row = db.query("SELECT COUNT(*) c FROM bookings WHERE payment_status = 'paid'", one=True)
    return row["c"] if row else 0


def sum_paid_visitors():
    row = db.query(
        "SELECT COALESCE(SUM(qty_indian+qty_foreign+qty_student+qty_child),0) s "
        "FROM bookings WHERE payment_status = 'paid'", one=True)
    return row["s"] if row else 0


# ---------------------------------------------------------------- chatlog --

def add_chat_message(session_id, role, message):
    db.execute("INSERT INTO chat_messages (session_id, role, message) VALUES (?,?,?)",
               (session_id, role, message))


def get_chat_history(session_id, limit=6):
    rows = db.query(
        "SELECT * FROM chat_messages WHERE session_id = ? ORDER BY created_at DESC, id DESC LIMIT ?",
        (session_id, limit),
    )
    return [ChatMessage(r) for r in reversed(rows)]


def count_user_chat_messages():
    row = db.query("SELECT COUNT(*) c FROM chat_messages WHERE role = 'user'", one=True)
    return row["c"] if row else 0


def get_all_chat_sessions():
    rows = db.query("SELECT * FROM chat_messages ORDER BY created_at ASC, id ASC")
    sessions = {}
    for r in rows:
        msg = ChatMessage(r)
        sessions.setdefault(msg.session_id, []).append(msg)
    return sessions


# --------------------------------------------------------------- contacts --

def add_contact_message(name, email, message, subject="General Inquiry"):
    db.execute("INSERT INTO contact_messages (name, email, message, subject) VALUES (?,?,?,?)",
               (name, email, message, subject))


def get_contact_messages():
    rows = db.query("SELECT * FROM contact_messages ORDER BY created_at DESC")
    return [ContactMessage(r) for r in rows]


# ------------------------------------------------------------------ admin --

def get_admin_by_username(username):
    return db.query("SELECT * FROM admin_users WHERE username = ?", (username,), one=True)


def create_admin(username, password_hash):
    db.execute("INSERT INTO admin_users (username, password_hash) VALUES (?,?)", (username, password_hash))


def count_admins():
    row = db.query("SELECT COUNT(*) c FROM admin_users", one=True)
    return row["c"] if row else 0


def update_admin_password(username, password_hash):
    db.execute("UPDATE admin_users SET password_hash = ? WHERE username = ?", (password_hash, username))


# --------------------------------------------------------------- settings --

DEFAULT_SETTINGS = {
    "site_name": "National Heritage Museum",
    "site_short_name": "Heritage Museum",
    "tagline": "Ministry of Culture & Antiquities — A Journey Through Time, From the Jurassic Age to Modern India",
    "hero_wiki_topic": "Indian_Museum,_Kolkata",
    "about_text": (
        "Established to preserve and showcase the story of civilisation, the National Heritage Museum "
        "brings together fossils, artefacts and monuments spanning over 200 million years — from the age "
        "of the dinosaurs through the Ice Age, the Stone Age, ancient river-valley civilisations, and the "
        "great Indian empires of the Mauryas, Guptas, Rajputs, Mughals and Sikhs — under a single roof."
    ),
    "address": "Heritage Marg, Central Museum Complex, New Delhi – 110001, India",
    "phone": "+91-11-2345-6789",
    "email": "info@nationalheritagemuseum.gov.in",
    "timings": "Tuesday – Sunday, 10:00 AM – 6:00 PM (Closed on Mondays & National Holidays)",
    "established_year": "1962",
    "total_artifacts": "42,000+",
    "price_indian": "50",
    "price_foreign": "500",
    "price_student": "20",
    "price_child": "0",
    "map_embed": "",
    "page_view_count": "128430",
    "logo_url": "",
}


def get_settings():
    rows = db.query("SELECT * FROM settings")
    values = {r["key"]: r["value"] for r in rows}
    merged = dict(DEFAULT_SETTINGS)
    merged.update(values)
    return merged


def get_setting(key, default=""):
    row = db.query("SELECT value FROM settings WHERE key = ?", (key,), one=True)
    if row:
        return row["value"]
    return DEFAULT_SETTINGS.get(key, default)


def update_settings(values: dict):
    for k, v in values.items():
        db.execute(
            "INSERT INTO settings (key, value) VALUES (?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (k, v),
        )


def get_page_views():
    return int(get_setting("page_view_count", "0") or 0)


def increment_page_views():
    current = get_page_views() + 1
    update_settings({"page_view_count": str(current)})
    return current


def seed_default_settings():
    existing = {r["key"] for r in db.query("SELECT key FROM settings")}
    for k, v in DEFAULT_SETTINGS.items():
        if k not in existing:
            db.execute("INSERT INTO settings (key, value) VALUES (?, ?)", (k, v))


# ----------------------------------------------------------------- notices --

def get_active_notices():
    rows = db.query("SELECT * FROM notices WHERE is_active = 1 ORDER BY created_at DESC")
    return [Notice(r) for r in rows]


def get_all_notices():
    rows = db.query("SELECT * FROM notices ORDER BY created_at DESC")
    return [Notice(r) for r in rows]


def create_notice(text):
    return db.execute("INSERT INTO notices (text) VALUES (?)", (text,))


def toggle_notice(notice_id):
    row = db.query("SELECT is_active FROM notices WHERE id = ?", (notice_id,), one=True)
    if row is None:
        return
    new_val = 0 if row["is_active"] else 1
    db.execute("UPDATE notices SET is_active = ? WHERE id = ?", (new_val, notice_id))


def delete_notice(notice_id):
    db.execute("DELETE FROM notices WHERE id = ?", (notice_id,))


# ------------------------------------------------------------------- media --

def add_media(filename, original_name, alt_text=""):
    return db.execute("INSERT INTO media (filename, original_name, alt_text) VALUES (?,?,?)",
                       (filename, original_name, alt_text))


def get_all_media():
    rows = db.query("SELECT * FROM media ORDER BY uploaded_at DESC")
    return [Media(r) for r in rows]


def get_media(media_id):
    row = db.query("SELECT * FROM media WHERE id = ?", (media_id,), one=True)
    return Media(row) if row else None


def delete_media(media_id):
    db.execute("DELETE FROM media WHERE id = ?", (media_id,))


# --------------------------------------------------------------- employees --

def get_employees(active_only=True):
    if active_only:
        rows = db.query("SELECT * FROM employees WHERE is_active = 1 ORDER BY display_order ASC, name ASC")
    else:
        rows = db.query("SELECT * FROM employees ORDER BY display_order ASC, name ASC")
    return [Employee(r) for r in rows]


def get_employee(employee_id):
    row = db.query("SELECT * FROM employees WHERE id = ?", (employee_id,), one=True)
    return Employee(row) if row else None


def create_employee(**fields):
    cols = ", ".join(fields.keys())
    placeholders = ", ".join(["?"] * len(fields))
    return db.execute(f"INSERT INTO employees ({cols}) VALUES ({placeholders})", tuple(fields.values()))


def update_employee(employee_id, **fields):
    sets = ", ".join(f"{k} = ?" for k in fields.keys())
    db.execute(f"UPDATE employees SET {sets} WHERE id = ?", tuple(fields.values()) + (employee_id,))


def delete_employee(employee_id):
    db.execute("DELETE FROM employees WHERE id = ?", (employee_id,))


def count_employees():
    row = db.query("SELECT COUNT(*) c FROM employees", one=True)
    return row["c"] if row else 0


# -------------------------------------------------------------------- pages --

def get_pages(published_only=True):
    if published_only:
        rows = db.query("SELECT * FROM pages WHERE is_published = 1 ORDER BY title ASC")
    else:
        rows = db.query("SELECT * FROM pages ORDER BY title ASC")
    return [Page(r) for r in rows]


def get_page(page_id):
    row = db.query("SELECT * FROM pages WHERE id = ?", (page_id,), one=True)
    return Page(row) if row else None


def get_page_by_slug(slug, published_only=True):
    if published_only:
        row = db.query("SELECT * FROM pages WHERE slug = ? AND is_published = 1", (slug,), one=True)
    else:
        row = db.query("SELECT * FROM pages WHERE slug = ?", (slug,), one=True)
    return Page(row) if row else None


def create_page(title, slug, content, is_published=1):
    return db.execute(
        "INSERT INTO pages (title, slug, content, is_published) VALUES (?,?,?,?)",
        (title, slug, content, is_published),
    )


def update_page(page_id, title, slug, content, is_published):
    db.execute(
        "UPDATE pages SET title=?, slug=?, content=?, is_published=?, updated_at=datetime('now') WHERE id=?",
        (title, slug, content, is_published, page_id),
    )


def delete_page(page_id):
    db.execute("DELETE FROM pages WHERE id = ?", (page_id,))


# -------------------------------------------------------------------- links --

def get_links(location=None, active_only=True):
    sql = "SELECT * FROM links"
    conditions = []
    args = []
    if location:
        conditions.append("location = ?")
        args.append(location)
    if active_only:
        conditions.append("is_active = 1")
    if conditions:
        sql += " WHERE " + " AND ".join(conditions)
    sql += " ORDER BY sort_order ASC, id ASC"
    rows = db.query(sql, tuple(args))
    return [Link(r) for r in rows]


def get_link(link_id):
    row = db.query("SELECT * FROM links WHERE id = ?", (link_id,), one=True)
    return Link(row) if row else None


def create_link(label, url, location, sort_order=0):
    return db.execute("INSERT INTO links (label, url, location, sort_order) VALUES (?,?,?,?)",
                       (label, url, location, sort_order))


def update_link(link_id, label, url, location, sort_order, is_active):
    db.execute("UPDATE links SET label=?, url=?, location=?, sort_order=?, is_active=? WHERE id=?",
               (label, url, location, sort_order, is_active, link_id))


def delete_link(link_id):
    db.execute("DELETE FROM links WHERE id = ?", (link_id,))


# ---------------------------------------------------------------- analytics --

SECTION_MAP = [
    ("/gallery/", "Gallery Detail"),
    ("/galleries", "Galleries List"),
    ("/visit", "Plan Your Visit / Booking"),
    ("/chat-page", "Ask Heritage AI"),
    ("/our-team", "Our Team"),
    ("/page/", "Custom Page"),
    ("/booking/success", "Booking Success"),
    ("/booking/cancel", "Booking Cancelled"),
    ("/checkout/", "Checkout"),
]


def classify_section(path):
    if path == "/":
        return "Home"
    for prefix, label in SECTION_MAP:
        if path.startswith(prefix):
            return label
    return "Other"


def log_visit(path, referrer, user_agent):
    section = classify_section(path)
    db.execute("INSERT INTO page_visits (path, section, referrer, user_agent) VALUES (?,?,?,?)",
               (path, section, referrer or "", user_agent or ""))


def get_recent_visits(limit=50):
    return db.query("SELECT * FROM page_visits ORDER BY created_at DESC LIMIT ?", (limit,))


def count_visits():
    row = db.query("SELECT COUNT(*) c FROM page_visits", one=True)
    return row["c"] if row else 0


def visits_by_section():
    rows = db.query("SELECT section, COUNT(*) c FROM page_visits GROUP BY section ORDER BY c DESC")
    return [(r["section"], r["c"]) for r in rows]


def visits_last_n_days(n=7):
    rows = db.query(
        "SELECT date(created_at) d, COUNT(*) c FROM page_visits "
        "WHERE created_at >= datetime('now', ?) GROUP BY date(created_at) ORDER BY d ASC",
        (f"-{n} days",),
    )
    return [(r["d"], r["c"]) for r in rows]
