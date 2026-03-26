import os
import uuid
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_reference_image(file_storage, upload_root):
    original_name = file_storage.filename or "imagem"
    ext = original_name.rsplit(".", 1)[1].lower() if "." in original_name else "jpg"
    safe_name = secure_filename(original_name.rsplit(".", 1)[0]) or "referencia"
    unique_name = f"{safe_name}-{uuid.uuid4().hex[:12]}.{ext}"
    relative_dir = "reference_images"
    absolute_dir = os.path.join(upload_root, relative_dir)
    os.makedirs(absolute_dir, exist_ok=True)
    absolute_path = os.path.join(absolute_dir, unique_name)
    file_storage.save(absolute_path)
    return {
        "original_name": original_name,
        "stored_name": unique_name,
        "relative_path": f"{relative_dir}/{unique_name}",
    }


def format_whatsapp(value):
    digits = "".join(ch for ch in (value or "") if ch.isdigit())
    return digits
