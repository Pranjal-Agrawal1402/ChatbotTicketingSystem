"""
Smart museum chatbot for the National Heritage Museum.

Uses Google Gemini (if GEMINI_API_KEY is configured) with the live gallery
database and site settings injected as grounding context. If no API key is
present, or the call fails for any reason, it gracefully falls back to a
rule-based engine that still answers intelligently from the live database,
so the site is always fully functional out of the box.
"""
import os
import re
from difflib import get_close_matches

from . import models

_GEMINI_READY = False
_gemini_model = None


def _init_gemini():
    global _GEMINI_READY, _gemini_model
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        return False
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        _gemini_model = genai.GenerativeModel("gemini-2.0-flash")
        _GEMINI_READY = True
        return True
    except Exception:
        return False


def _museum_context():
    settings = models.get_settings()
    lines = [
        f"Museum name: {settings['site_name']}. {settings['tagline']}",
        f"Address: {settings['address']}. Timings: {settings['timings']}.",
        f"Ticket prices: Indian citizens ₹{settings['price_indian']}, Foreign nationals "
        f"₹{settings['price_foreign']}, Students (with valid ID) ₹{settings['price_student']}, "
        f"Children under 12: Free.",
        f"Established: {settings['established_year']}. Total artefacts in the collection: "
        f"{settings['total_artifacts']}.",
        "",
        "GALLERIES (chronological order):",
    ]
    for g in models.get_galleries(active_only=True):
        monuments = ", ".join(m["name"] for m in g.monument_list)
        lines.append(
            f"- {g.name} ({g.period}): {g.short_description} "
            f"Live visitors: {g.current_occupancy}/{g.max_occupancy} ({g.status}, "
            f"{g.available_slots} slots free). Key exhibits: {monuments}. History: {g.history}"
        )
    return "\n".join(lines)


SYSTEM_PROMPT = """You are "Heritage AI", the official virtual guide for the {museum_name}, a museum that \
spans the entire sweep of history under one roof — from the Jurassic age of the dinosaurs through the Ice \
Age, Stone Age, ancient civilisations, and the great Indian empires (Mauryan, Rajput, Mughal, Sikh) to Hindu \
temple architecture. Answer visitor questions using ONLY the data provided below. Be warm, professional and \
concise (3-5 sentences unless asked for detail), as befits an official government-run cultural institution. \
If asked about live occupancy, quote the exact numbers. If asked something unrelated, politely steer the \
conversation back while remaining courteous. If asked about booking tickets, tell them to use the "Plan Your \
Visit" / "Book Tickets" page to book securely online.

MUSEUM DATA:
{context}

Conversation so far:
{history}

Visitor: {message}
Heritage AI:"""


def _find_gallery(text, history=None):
    text_l = text.lower()
    galleries = models.get_galleries(active_only=True)

    # 1. exact substring match on gallery name or a named monument/exhibit
    for g in galleries:
        if g.name.lower() in text_l:
            return g
        for m in g.monument_list:
            if m["name"].lower() in text_l:
                return g

    # 2. significant-word overlap match
    query_words = set(re.findall(r"[a-zA-Z]+", text_l))
    best, best_score = None, 0
    for g in galleries:
        g_words = [w for w in re.findall(r"[a-zA-Z]+", g.name.lower()) if len(w) > 3]
        score = sum(1 for w in g_words if w in query_words)
        for m in g.monument_list:
            m_words = [w for w in re.findall(r"[a-zA-Z]+", m["name"].lower()) if len(w) > 3]
            score += sum(1 for w in m_words if w in query_words)
        if score > best_score:
            best, best_score = g, score
    if best and best_score >= 1:
        return best

    # 3. typo tolerance for short, name-like queries
    if len(text_l.split()) <= 4:
        names = [g.name.lower() for g in galleries]
        matches = get_close_matches(text_l, names, n=1, cutoff=0.6)
        if matches:
            for g in galleries:
                if g.name.lower() == matches[0]:
                    return g

    # 4. follow-up questions — check what the visitor mentioned earlier
    if history and any(w in query_words for w in ["it", "its", "that", "there", "this"]):
        for h in reversed(history):
            if h.get("role") != "user":
                continue
            found = _find_gallery(h.get("message", ""))
            if found:
                return found
    return None


def _rule_based_reply(message, history=None):
    text = message.lower().strip()
    settings = models.get_settings()
    gallery = _find_gallery(text, history)

    if any(g in text for g in ["hi", "hello", "hey", "namaste"]) and len(text) < 20:
        return (f"Namaste! 🙏 Welcome to the {settings['site_name']}. I'm Heritage AI, your virtual guide "
                f"across our galleries — from the Jurassic age to the Sikh Empire. Ask me about timings, "
                f"ticket prices, history, or live visitor numbers in any gallery — or say 'list galleries' "
                f"to see everything on display!")

    if "list" in text and ("galler" in text or "wing" in text or "section" in text):
        names = [f"{g.name} ({g.period})" for g in models.get_galleries(active_only=True)]
        return "Here are our galleries, in chronological order:\n• " + "\n• ".join(names)

    if any(k in text for k in ["occupancy", "crowd", "busy", "available", "slot", "capacity", "visitors"]):
        if gallery:
            return (f"🎟️ The {gallery.name} gallery currently has {gallery.current_occupancy}/"
                     f"{gallery.max_occupancy} visitors ({gallery.occupancy_percent}% full — status: "
                     f"{gallery.status}). {gallery.available_slots} slots are free right now.")
        all_g = models.get_galleries(active_only=True)
        busiest = max(all_g, key=lambda g: g.current_occupancy) if all_g else None
        if not busiest:
            return "I don't have any gallery data available right now."
        return (f"I can check live visitor numbers for any gallery! Right now, {busiest.name} is the "
                f"busiest at {busiest.occupancy_percent}% capacity. Which gallery would you like to check?")

    if any(k in text for k in ["price", "cost", "ticket", "fee", "fare", "entry"]):
        return (f"🎫 Entry tickets: Indian citizens ₹{settings['price_indian']}, Foreign nationals "
                f"₹{settings['price_foreign']}, Students (valid ID) ₹{settings['price_student']}, and "
                f"children under 12 enter free. Book online any time via 'Plan Your Visit'.")

    if any(k in text for k in ["time", "timing", "open", "close", "hours", "when"]) and "history" not in text:
        return f"🕒 We are open {settings['timings']}. Address: {settings['address']}."

    if any(k in text for k in ["history", "story", "built", "founded", "when was"]):
        if gallery:
            return f"📜 {gallery.history}"
        return "I'd love to share some history — which gallery or monument are you curious about?"

    if any(k in text for k in ["highlight", "see", "attraction", "famous for", "must see", "exhibit"]):
        if gallery:
            names = ", ".join(m["name"] for m in gallery.monument_list) or ", ".join(gallery.highlight_list)
            return f"✨ Don't miss in the {gallery.name}: {names}."
        return "Tell me which gallery you're visiting and I'll share its must-see exhibits!"

    if gallery:
        return f"ℹ️ {gallery.name} ({gallery.period}) — {gallery.description}"

    if any(k in text for k in ["book", "booking", "reserve", "visit"]):
        return ("You can book tickets instantly on our 'Plan Your Visit' page — select your ticket "
                "category and date, and pay securely online. Would you like help choosing which "
                "galleries to prioritise?")

    if any(k in text for k in ["where", "address", "location", "directions"]):
        return f"📍 We're located at {settings['address']}."

    if any(k in text for k in ["thank", "thanks"]):
        return "You're most welcome! Enjoy your journey through history at our museum. 🏛️"

    return ("I'm not fully sure about that one — but I can tell you about gallery timings, ticket prices, "
            "history, exhibits, or live visitor numbers. Try asking, e.g. 'Tell me about the Mughal Era "
            "gallery' or say 'list galleries' to see everything on display.")


def get_reply(message, history=None):
    history = history or []
    if not _GEMINI_READY and not _init_gemini():
        return _rule_based_reply(message, history)

    try:
        settings = models.get_settings()
        hist_text = "\n".join(f"{h['role']}: {h['message']}" for h in history[-6:])
        prompt = SYSTEM_PROMPT.format(
            museum_name=settings["site_name"], context=_museum_context(),
            history=hist_text, message=message,
        )
        response = _gemini_model.generate_content(prompt)
        text = (response.text or "").strip()
        return text if text else _rule_based_reply(message, history)
    except Exception:
        return _rule_based_reply(message, history)
