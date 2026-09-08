import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()


def create_app():
    root_dir = os.path.dirname(os.path.dirname(__file__))
    app = Flask(
        __name__,
        template_folder=os.path.join(root_dir, "templates"),
        static_folder=os.path.join(root_dir, "static"),
    )

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-change-me-please")

    default_db_path = os.path.join(root_dir, "instance", "museum.db")
    app.config["DB_PATH"] = os.getenv("DB_PATH", default_db_path)

    app.config["ADMIN_USERNAME"] = os.getenv("ADMIN_USERNAME", "admin")
    app.config["ADMIN_PASSWORD"] = os.getenv("ADMIN_PASSWORD", "admin123")

    app.config["UPLOAD_FOLDER"] = os.path.join(root_dir, "static", "uploads")
    app.config["MAX_CONTENT_LENGTH"] = 6 * 1024 * 1024  # 6 MB upload limit
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    from . import db
    db.init_db(app)

    from .routes_public import public_bp
    from .routes_admin import admin_bp
    from .routes_api import api_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(api_bp, url_prefix="/api")

    with app.app_context():
        from .seed_data import seed_if_empty
        seed_if_empty()

    @app.before_request
    def _track_visit():
        from flask import request
        from . import models
        path = request.path
        if (request.method == "GET" and not path.startswith("/static/")
                and not path.startswith("/admin") and not path.startswith("/api")):
            try:
                models.log_visit(path, request.referrer, request.headers.get("User-Agent", ""))
            except Exception:
                pass  # analytics must never break the site

    @app.context_processor
    def inject_globals():
        from . import models
        return {
            "site_settings": models.get_settings(),
            "page_views": models.count_visits(),
            "notices": models.get_active_notices(),
            "nav_links": models.get_links(location="nav"),
            "footer_links": models.get_links(location="footer"),
        }

    @app.errorhandler(404)
    def not_found(e):
        from flask import render_template
        from . import models
        return render_template("errors/404.html", settings=models.get_settings()), 404

    @app.errorhandler(500)
    def server_error(e):
        from flask import render_template
        from . import models
        return render_template("errors/500.html", settings=models.get_settings()), 500

    return app
