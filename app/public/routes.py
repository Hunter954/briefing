from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from app import db
from app.models import Briefing, OptionValue, ReferenceImage
from app.utils import allowed_file, save_reference_image, format_whatsapp

public_bp = Blueprint("public", __name__)

OPTION_GROUPS = {
    "goal": ["Vender mais", "Passar mais profissionalismo", "Se destacar da concorrência", "Atrair um público mais premium", "Modernizar a imagem", "Criar identidade do zero"],
    "audience": ["Jovens", "Adultos", "Famílias", "Empresas", "Público premium", "Público popular", "Masculino", "Feminino", "Todos"],
    "values": ["Confiança", "Sofisticação", "Modernidade", "Criatividade", "Elegância", "Simplicidade", "Força", "Velocidade", "Exclusividade", "Tradição", "Inovação", "Proximidade"],
    "perception": ["Moderna", "Premium", "Minimalista", "Impactante", "Delicada", "Forte", "Divertida", "Luxuosa", "Tecnológica", "Artesanal"],
    "colors": ["Preto", "Branco", "Azul", "Vermelho", "Verde", "Amarelo", "Dourado", "Prata", "Roxo", "Rosa", "Laranja", "Ainda não sei"],
    "style": ["Minimalista", "Moderno", "Elegante", "Luxuoso", "Corporativo", "Criativo", "Vintage", "Esportivo", "Tecnológico", "Orgânico / natural"],
    "business_segment": ["Loja / comércio", "Restaurante / food", "Moda / beleza", "Saúde", "Construção / engenharia", "Advocacia", "Igreja / projeto social", "Tecnologia", "Marketing / audiovisual", "Outro"],
    "brand_stage": ["É uma marca nova", "Já existe, mas quero redesign", "Já existe e quero apenas melhorar"],
    "slogan_status": ["Não tem slogan", "Sim, já tenho", "Quero criar depois"],
    "logo_type": ["Apenas nome da marca", "Nome + símbolo", "Apenas símbolo", "Monograma / iniciais", "Não sei, quero sugestão"],
    "desired_symbol": ["Inicial do nome", "Coroa", "Câmera", "Escudo", "Letra estilizada", "Cruz", "Fogo", "Folha", "Animal", "Outro", "Não quero símbolo específico"],
    "background_preference": ["Sim, nos dois", "Mais em fundo claro", "Mais em fundo escuro", "Não sei"],
    "deadline": ["Urgente", "Essa semana", "Esse mês", "Sem pressa"],
    "service_scope": ["Apenas logomarca", "Logomarca + paleta de cores", "Logomarca + identidade visual completa", "Ainda não sei"],
    "usage": ["Instagram", "Cartão de visita", "Fachada", "Uniforme", "Embalagem", "Site", "Papelaria", "Adesivos", "Outdoor", "Todos"],
    "feelings": ["Confiança", "Desejo de compra", "Credibilidade", "Sofisticação", "Impacto", "Curiosidade", "Segurança", "Exclusividade"],
}


@public_bp.route("/")
def index():
    return render_template("public/index.html", option_groups=OPTION_GROUPS)


@public_bp.post("/enviar")
def submit_briefing():
    brand_name = (request.form.get("brand_name") or "").strip()
    contact_name = (request.form.get("contact_name") or "").strip()
    contact_whatsapp = format_whatsapp(request.form.get("contact_whatsapp"))

    if not brand_name or not contact_name or not contact_whatsapp:
        flash("Preencha marca, nome e WhatsApp para enviar o briefing.", "danger")
        return redirect(url_for("public.index"))

    briefing = Briefing(
        brand_name=brand_name,
        slogan_status=request.form.get("slogan_status"),
        slogan_text=(request.form.get("slogan_text") or "").strip() or None,
        business_segment=request.form.get("business_segment"),
        business_description=(request.form.get("business_description") or "").strip() or None,
        goal=(request.form.get("goal_text") or "").strip() or None,
        brand_stage=request.form.get("brand_stage"),
        audience_details=(request.form.get("audience_details") or "").strip() or None,
        city_region=(request.form.get("city_region") or "").strip() or None,
        colors_wanted=(request.form.get("colors_wanted") or "").strip() or None,
        colors_avoided=(request.form.get("colors_avoided") or "").strip() or None,
        logo_type=request.form.get("logo_type"),
        references_liked_text=(request.form.get("references_liked_text") or "").strip() or None,
        references_disliked_text=(request.form.get("references_disliked_text") or "").strip() or None,
        desired_symbol=request.form.get("desired_symbol"),
        desired_symbol_details=(request.form.get("desired_symbol_details") or "").strip() or None,
        avoid_elements=(request.form.get("avoid_elements") or "").strip() or None,
        background_preference=request.form.get("background_preference"),
        desired_feeling=(request.form.get("desired_feeling_text") or "").strip() or None,
        deadline=request.form.get("deadline"),
        service_scope=request.form.get("service_scope"),
        final_notes=(request.form.get("final_notes") or "").strip() or None,
        contact_name=contact_name,
        contact_whatsapp=contact_whatsapp,
        contact_email=(request.form.get("contact_email") or "").strip() or None,
    )

    db.session.add(briefing)

    multi_keys = ["goal", "audience", "values", "perception", "colors", "style", "usage", "feelings"]

    for key in multi_keys:
        for value in request.form.getlist(key):
            cleaned = (value or "").strip()
            if not cleaned:
                continue
            option = OptionValue.query.filter_by(category=key, value=cleaned).first()
            if not option:
                option = OptionValue(category=key, value=cleaned)
                db.session.add(option)
                db.session.flush()
            briefing.options.append(option)

    db.session.flush()

    files = request.files.getlist("reference_images")
    for file in files:
        if not file or not file.filename:
            continue
        if not allowed_file(file.filename):
            continue
        saved = save_reference_image(file, current_app.config["UPLOAD_ROOT"])
        image = ReferenceImage(
            briefing_id=briefing.id,
            original_name=saved["original_name"],
            stored_name=saved["stored_name"],
            relative_path=saved["relative_path"],
        )
        db.session.add(image)

    db.session.commit()
    return render_template("public/success.html", briefing=briefing)
