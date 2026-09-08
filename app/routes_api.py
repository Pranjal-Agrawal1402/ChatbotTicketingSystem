import uuid
from flask import Blueprint, request, jsonify, session, abort

from . import models
from .chatbot import get_reply

api_bp = Blueprint("api", __name__)


def _session_id():
    sid = session.get("chat_sid")
    if not sid:
        sid = uuid.uuid4().hex
        session["chat_sid"] = sid
    return sid


@api_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    if not message:
        return jsonify({"error": "empty message"}), 400

    sid = _session_id()
    history_rows = models.get_chat_history(sid, limit=6)
    history = [{"role": r.role, "message": r.message} for r in history_rows]

    models.add_chat_message(sid, "user", message)
    reply = get_reply(message, history)
    models.add_chat_message(sid, "bot", reply)

    return jsonify({"reply": reply})


@api_bp.route("/occupancy")
def occupancy():
    galleries = models.get_galleries(active_only=True)
    return jsonify([g.to_dict() for g in galleries])


@api_bp.route("/occupancy/<slug>")
def occupancy_one(slug):
    gallery = models.get_gallery_by_slug(slug)
    if not gallery:
        abort(404)
    return jsonify(gallery.to_dict())


@api_bp.route("/galleries")
def galleries_json():
    galleries = models.get_galleries(active_only=True)
    return jsonify([g.to_dict() for g in galleries])
