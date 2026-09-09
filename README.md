# [🏛️ National Heritage Museum — Government Portal Platform](https://gymguide1.vercel.app)

A complete, production-ready single-museum website styled as an official government cultural
portal — covering **every era of history under one roof**: Jurassic, Ice Age, Stone Age, Prehistoric,
Ancient Civilizations, Ancient Indian (Mauryan), Roman Age, Hindu Temple Architecture, Medieval
(Delhi Sultanate), Rajput, Mughal and Sikh heritage — with real photographs, a smart AI guide, online
ticket payments, and a fully admin-controllable CMS.

## ✨ What's included

- 🏛️ **Official government-portal design** — utility bar, accessibility toolbar (text size /
  high-contrast), sticky navigation, scrolling notices ticker, formal navy/maroon/gold theme,
  a custom institutional emblem, and a classic "visitors to this site" counter
- 🌐 **Built-in language translator** — Google's official Website Translator widget (Hindi, Bengali,
  Tamil, Telugu, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Urdu, French, German, Spanish,
  Chinese, Japanese, Arabic and more), exactly like real Indian government sites use
- 🖼️ **Real photographs, dynamically loaded** — every gallery, hero banner and featured monument
  pulls a genuine photo live from Wikipedia's public API (no broken image links, no fake AI art —
  actual pictures of the Taj Mahal, Golden Temple, Khajuraho, Colosseum, woolly mammoths, dinosaur
  fossils, etc.), with a themed placeholder shown gracefully if a fetch ever fails
- 🏺 **12 fully detailed galleries** spanning every era you'd expect in a national museum, each with
  history, must-see highlights, and a photo-gallery of named monuments/exhibits
- 🤖 **Smart AI chatbot** ("Heritage AI") — Gemini-powered when you add an API key, with an
  intelligent rule-based fallback (tracks conversation context, e.g. "what about its history?")
  that always works with zero configuration
- 💳 **Real payment gateway** (Stripe Checkout) with tiered pricing (Indian / Foreign / Student /
  Child) and an automatic Demo Mode so the whole booking flow works instantly, no keys required
- 🗄️ **A real database** — Python's built-in `sqlite3`, zero extra dependencies
- 🛠️ **A fully admin-controllable CMS**, reachable via the small shield icon in the bottom-left
  corner of every page (or `/admin/login`) — genuinely no code or developer needed for day-to-day changes:
  - 🖼️ **Media Library** — upload, tag and delete any image; reuse it anywhere on the site
  - 🏺 **Galleries** — add/edit/delete galleries, their photo (Wikipedia topic *or* your own uploaded
    image), history, highlights, and named monuments/exhibits (each with its own photo)
  - 🧑‍💼 **Employees** — add/edit/delete staff profiles with photo, bio, designation and contact info,
    shown on the public "Our Team" page
  - 📄 **Pages** — create/edit/delete any additional content page (policies, announcements, careers,
    etc.), each published instantly at its own URL
  - 🔗 **Menus & Links** — add/edit/delete any link in the top navigation or footer, to an internal
    page or any external URL
  - 🖼️ **Logo** — upload a custom logo image any time, replacing the default emblem instantly
  - 💷 **Ticket prices, museum name, tagline, hero photo, contact info, hours** — all editable live
  - 📢 Publish/hide/delete homepage **notices** (the scrolling ticker)
  - 📈 **Visitor analytics** — see how many people visited, which section/page they viewed, where they
    came from, and their browser — no external analytics service required
  - 📩 **Contact inquiries** — see every message with the subject/section the visitor selected
  - Bookings, revenue, live gallery occupancy and AI chat transcripts, all in one dashboard
- 🚀 **Deploy anywhere** — Render, Railway, Fly.io, Vercel, Netlify, Docker, or plain GitHub push

---

## 1. Project structure

```
museum_chatbot/
├── app/
│   ├── __init__.py         # App factory
│   ├── db.py                # sqlite3 connection + schema
│   ├── models.py            # Galleries, Bookings, Settings, Notices, Chat, Admin — query layer
│   ├── chatbot.py           # Gemini + rule-based AI logic
│   ├── payments.py          # Stripe integration + demo mode
│   ├── seed_data.py         # 12 galleries + default settings + sample notices
│   ├── routes_public.py     # Home, galleries, visit/booking, contact
│   ├── routes_admin.py      # Admin dashboard, galleries CRUD, settings, notices CRUD
│   └── routes_api.py        # /api/chat, /api/occupancy, /api/galleries
├── templates/                # Government-portal Jinja2 templates (public + admin)
├── static/
│   ├── css/style.css         # Official portal design system
│   ├── js/main.js            # Accessibility toolbar, chat widget, ticket calculator
│   ├── js/admin.js           # Admin dashboard chart + quick controls
│   └── js/wiki-images.js     # Live photo loader (Wikipedia API)
├── api/index.py               # Vercel serverless entrypoint
├── netlify/functions/app.py    # Netlify Functions entrypoint
├── wsgi.py                      # Local / gunicorn entrypoint
├── requirements.txt
├── Procfile                      # Render / Railway / Heroku
├── render.yaml                    # One-click Render blueprint
├── vercel.json                     # Vercel config
├── netlify.toml                     # Netlify config
├── Dockerfile                        # Any container platform
└── .env.example
```

## 2. Run it locally

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # optional — everything works with zero keys
python wsgi.py
``` 
## Run it on server
```bash
py -m venv venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
venv\Scripts\activate
pip install -r requirements.txt
python wsgi.py
```
Visit **http://127.0.0.1:5000**. The database is created and seeded automatically on first run —
12 galleries, default settings and sample notices, no setup needed.

### Admin access
Click the small **shield icon** in the bottom-left corner of any page, or go to
`http://127.0.0.1:5000/admin/login`.

- Username: `admin`
- Password: `admin123`

Change these via `ADMIN_USERNAME` / `ADMIN_PASSWORD` env vars, or change the password anytime from
**Admin → Account**.

## 3. Making it fully your own (no code required)

Everything content-wise is editable from the admin panel:

| What to change | Where |
|---|---|
| Museum name, tagline, about text, hero photo | Admin → Site Settings |
| Logo | Admin → Site Settings (upload, or remove to revert to the default emblem) |
| Address, phone, email, opening hours | Admin → Site Settings |
| Ticket prices (4 categories) | Admin → Site Settings |
| Add/edit/remove a gallery, its photo, history, monuments | Admin → Galleries |
| Add/edit/remove employees, their photo and bio | Admin → Employees |
| Add/edit/remove any extra page (policies, careers, etc.) | Admin → Pages |
| Add/edit/remove any nav or footer link | Admin → Menus & Links |
| Upload/delete any image | Admin → Media Library |
| Scrolling homepage notices | Admin → Notices |
| Live visitor occupancy per gallery | Admin → Dashboard (quick +/- controls) |
| See who's visiting, and what they're contacting you about | Admin → Visitor Analytics / Admin → Messages |

To change a gallery's, monument's, or the homepage's photo, either:
1. Set the **Photo** field to any valid English Wikipedia article title (e.g. `Taj_Mahal`,
   `Golden_Temple`) — the site fetches a real, live photo automatically, or
2. Upload your own photo in **Admin → Media Library**, then paste the `media:filename.jpg` code it
   gives you into that same field instead.

## 4. Enabling real AI + real payments (optional)

The site is 100% functional without any keys.

| Feature | Env var | Where to get it |
|---|---|---|
| Smarter AI answers via Gemini | `GEMINI_API_KEY` | https://aistudio.google.com/app/apikey (free) |
| Real card payments via Stripe | `STRIPE_SECRET_KEY`, `STRIPE_PUBLIC_KEY` | https://dashboard.stripe.com/test/apikeys (free test mode) |
| DB location on hosts with persistent volumes | `DB_PATH` | e.g. `/data/museum.db` on Render/Fly.io disks |

Without `GEMINI_API_KEY`, the chatbot uses a smart rule-based engine that still answers correctly
from the live database. Without `STRIPE_SECRET_KEY`, ticket booking uses **Demo Mode** — bookings are
created and instantly confirmed so the whole flow (receipts, admin dashboard) is testable end-to-end.

## 5. Deployment guides

### ▶ Render (recommended)
1. Push this project to a GitHub repo.
2. On [Render](https://render.com) → New → Blueprint → point it at your repo (`render.yaml` included).
3. Add optional env vars (`GEMINI_API_KEY`, `STRIPE_SECRET_KEY`, etc.) in the dashboard.
4. Deploy — SQLite persists automatically on Render's disk.

### ▶ Railway / Fly.io / Heroku-style platforms
These support the included `Procfile` (`web: gunicorn wsgi:app`) out of the box.

### ▶ Vercel
1. Push to GitHub, then **Import Project** on [vercel.com](https://vercel.com).
2. Vercel auto-detects `vercel.json` and `api/index.py`.
3. Note: Vercel's filesystem is ephemeral — great for demos; for persistent production data
   (including the database **and any images uploaded via the Media Library / logo / employee
   photos**), point `app/db.py` at a hosted database and use a cloud storage bucket for uploads
   instead of local disk.

### ▶ Netlify
1. Push to GitHub, then **Add new site → Import an existing project** on [netlify.com](https://www.netlify.com).
2. Netlify auto-detects `netlify.toml`, building `netlify/functions/app.py` as a serverless function
   wrapping the whole Flask app.
3. Same ephemeral-storage note as Vercel applies — including uploaded images.

> **Important for both Vercel and Netlify:** since admin-uploaded images and the database live on
> local disk by default, they will **not persist** between deployments on serverless platforms.
> **Render, Railway, Fly.io or Docker on a VPS are strongly recommended** if you plan to use the
> Media Library, logo upload, or employee photos in production — they all provide persistent disk
> storage out of the box.

### ▶ Docker (any cloud / VPS)
```bash
docker build -t heritage-museum .
docker run -p 8080:8080 --env-file .env heritage-museum
```

### ▶ GitHub
Push the whole folder as-is — every platform above deploys directly from a GitHub repo. `.gitignore`
keeps secrets (`.env`) and the local database out of version control.

## 6. Tech stack

- **Backend:** Flask 3, Gunicorn
- **Database:** Built-in `sqlite3` (no ORM dependency)
- **AI:** Google Gemini (`gemini-2.0-flash`) with graceful rule-based fallback
- **Payments:** Stripe Checkout with automatic demo-mode fallback
- **Images:** Live Wikipedia API (MediaWiki `pageimages`), no manual uploads or hosting needed
- **Translation:** Google Website Translator widget (free, no API key)
- **Frontend:** Hand-crafted CSS design system (no framework dependency), vanilla JS

---

Note: the institutional emblem, name and styling are original and illustrative — this is not an
official government website and does not use any protected national emblem or insignia.
