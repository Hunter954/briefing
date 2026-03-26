import os
from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    db.create_all()

    email = os.getenv("ADMIN_EMAIL", "admin@seudominio.com").strip().lower()
    password = os.getenv("ADMIN_PASSWORD", "123456")
    name = os.getenv("ADMIN_NAME", "Administrador").strip()

    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(name=name, email=email, is_admin=True)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print(f"Admin criado: {email}")
    else:
        user.name = name
        user.is_admin = True
        user.set_password(password)
        db.session.commit()
        print(f"Admin atualizado: {email}")
