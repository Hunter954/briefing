import os
from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, send_from_directory, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import desc, or_
from app import db
from app.models import Briefing, User

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def get_grouped_options(briefing):
    grouped = {}
    for option in briefing.options:
        grouped.setdefault(option.category, []).append(option.value)
    return grouped


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))

    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        user = User.query.filter_by(email=email, is_admin=True).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Login realizado com sucesso.", "success")
            return redirect(url_for("admin.dashboard"))
        flash("E-mail ou senha inválidos.", "danger")

    return render_template("admin/login.html")


@admin_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu do painel.", "info")
    return redirect(url_for("admin.login"))


@admin_bp.route("/")
@login_required
def dashboard():
    query = (request.args.get("q") or "").strip()
    briefings_query = Briefing.query.order_by(desc(Briefing.created_at))
    if query:
        like = f"%{query}%"
        briefings_query = briefings_query.filter(
            or_(
                Briefing.brand_name.ilike(like),
                Briefing.contact_name.ilike(like),
                Briefing.contact_email.ilike(like),
                Briefing.contact_whatsapp.ilike(like),
            )
        )
    briefings = briefings_query.all()

    total = Briefing.query.count()
    with_images = Briefing.query.join(Briefing.images).distinct().count()

    return render_template(
        "admin/dashboard.html",
        briefings=briefings,
        total=total,
        with_images=with_images,
        query=query,
    )


@admin_bp.route("/briefing/<int:briefing_id>")
@login_required
def briefing_detail(briefing_id):
    briefing = Briefing.query.get_or_404(briefing_id)
    grouped_options = get_grouped_options(briefing)
    return render_template("admin/briefing_detail.html", briefing=briefing, grouped_options=grouped_options)


@admin_bp.route("/uploads/<path:relative_path>")
@login_required
def upload_file(relative_path):
    upload_root = current_app.config["UPLOAD_ROOT"]
    safe_root = os.path.abspath(upload_root)
    target_dir = os.path.abspath(os.path.join(upload_root, os.path.dirname(relative_path)))
    if not target_dir.startswith(safe_root):
        abort(403)
    return send_from_directory(target_dir, os.path.basename(relative_path))
