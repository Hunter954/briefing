from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

briefing_values = db.Table(
    "briefing_values",
    db.Column("briefing_id", db.Integer, db.ForeignKey("briefing.id"), primary_key=True),
    db.Column("option_value_id", db.Integer, db.ForeignKey("option_value.id"), primary_key=True),
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(180), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Briefing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand_name = db.Column(db.String(180), nullable=False)
    slogan_status = db.Column(db.String(50))
    slogan_text = db.Column(db.String(255))
    business_segment = db.Column(db.String(120))
    business_description = db.Column(db.Text)
    goal = db.Column(db.Text)
    brand_stage = db.Column(db.String(120))
    audience_details = db.Column(db.Text)
    city_region = db.Column(db.String(180))
    colors_wanted = db.Column(db.String(255))
    colors_avoided = db.Column(db.String(255))
    logo_type = db.Column(db.String(120))
    references_liked_text = db.Column(db.Text)
    references_disliked_text = db.Column(db.Text)
    desired_symbol = db.Column(db.String(255))
    desired_symbol_details = db.Column(db.Text)
    avoid_elements = db.Column(db.Text)
    background_preference = db.Column(db.String(120))
    desired_feeling = db.Column(db.Text)
    deadline = db.Column(db.String(120))
    service_scope = db.Column(db.String(120))
    final_notes = db.Column(db.Text)
    contact_name = db.Column(db.String(180), nullable=False)
    contact_whatsapp = db.Column(db.String(40), nullable=False)
    contact_email = db.Column(db.String(180))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    options = db.relationship(
        "OptionValue",
        secondary=briefing_values,
        backref=db.backref("briefings", lazy="dynamic"),
        lazy="joined",
    )
    images = db.relationship("ReferenceImage", backref="briefing", lazy=True, cascade="all, delete-orphan")


class OptionValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(80), nullable=False, index=True)
    value = db.Column(db.String(120), nullable=False)

    __table_args__ = (db.UniqueConstraint("category", "value", name="uq_category_value"),)


class ReferenceImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    briefing_id = db.Column(db.Integer, db.ForeignKey("briefing.id"), nullable=False)
    original_name = db.Column(db.String(255), nullable=False)
    stored_name = db.Column(db.String(255), nullable=False)
    relative_path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
