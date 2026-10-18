"""Static site generator: python tools/build.py

Reads tools/content.py and writes plain HTML pages (pretty URLs: /projects/<slug>/index.html).
Images of the projects are copied from local clones of the repositories (see IMAGE_SOURCE) and
converted to WebP; they are committed under assets/img/, so the site itself needs no build step.
"""
import hashlib
import html
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(__file__))
from content import (ABOUT_PARAGRAPHS, ACTIVITIES, AREAS, CONTACT_FORM_ENDPOINT, COURSES, EDUCATION, LITERATURE, METHODS, RESEARCH_ABOUT_SURVEY, RESEARCH_INTRO, EXPERIENCE, PROFILE, PROJECTS,  # noqa: E402
                     PUBLICATIONS, RESEARCH, SITE_URL, SKILLS)

from project_details import DETAILS  # noqa: E402

for _p in PROJECTS:
    _p.update(DETAILS.get(_p["slug"], {}))

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
IMAGE_SOURCE = os.environ.get("IMAGE_SOURCE", r"E:\GitHub-backup-ftharir-2026-10-18")
AVATAR_SOURCE = os.environ.get("AVATAR_SOURCE", "")  # optional: square image to convert into assets/img/avatar.webp

esc = html.escape


def ver(rel):
    """Short content hash for cache busting: a changed file gets a new URL, so browsers never show stale CSS or JS."""
    with open(os.path.join(ROOT, rel), "rb") as f:
        return hashlib.md5(f.read()).hexdigest()[:8]

ICONS = {
    "home": '<path d="M3 11.5 12 4l9 7.5"/><path d="M5.5 10v9.5h13V10"/><path d="M10 19.5v-5h4v5"/>',
    "user": '<circle cx="12" cy="8" r="3.6"/><path d="M4.5 20c.8-3.7 3.7-5.6 7.5-5.6s6.7 1.9 7.5 5.6"/>',
    "briefcase": '<rect x="3" y="7.5" width="18" height="12" rx="2.5"/><path d="M9 7.5V6a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v1.5"/><path d="M3 13h18"/>',
    "flask": '<path d="M9.5 3.5h5"/><path d="M10.5 3.5v6L5 18.5a1.8 1.8 0 0 0 1.6 2.7h10.8a1.8 1.8 0 0 0 1.6-2.7L13.5 9.5v-6"/><path d="M7.8 15h8.4"/>',
    "grid": '<rect x="4" y="4" width="6.5" height="6.5" rx="1.8"/><rect x="13.5" y="4" width="6.5" height="6.5" rx="1.8"/><rect x="4" y="13.5" width="6.5" height="6.5" rx="1.8"/><rect x="13.5" y="13.5" width="6.5" height="6.5" rx="1.8"/>',
    "code": '<path d="m8.5 8-4.5 4 4.5 4"/><path d="m15.5 8 4.5 4-4.5 4"/><path d="m13.5 5.5-3 13"/>',
    "book": '<path d="M5 4.5h10.5A3.5 3.5 0 0 1 19 8v11.5H8.5A3.5 3.5 0 0 1 5 16z"/><path d="M5 16a3.5 3.5 0 0 1 3.5-3.5H19"/>',
    "mail": '<rect x="3" y="5.5" width="18" height="13" rx="2.5"/><path d="m4 7.5 8 6 8-6"/>',
    "github": '<path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/>',
    "linkedin": '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/>',
    "arrow": '<path d="M5 12h14"/><path d="m13 6 6 6-6 6"/>',
    "copy": '<rect x="8" y="8" width="12" height="12" rx="2.500"/><path d="M16 8V6.500A2.500 2.500 0 0 0 13.500 4h-7A2.500 2.500 0 0 0 4 6.500v7A2.500 2.500 0 0 0 6.500 16H8"/>',
    "pin": '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    "star": '<path d="m12 3.500 2.700 5.500 6 .9-4.400 4.200 1 6-5.300-2.800-5.300 2.800 1-6L3.300 9.900l6-.9z"/>',
}


def icon(name, cls=""):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true" class="{cls}">{ICONS[name]}</svg>'


NAV = [
    ("/", "Home", "home"), ("/about/", "About", "user"), ("/experience/", "Experience", "briefcase"),
    ("/research/", "Research", "flask"), ("/projects/", "Projects", "grid"), ("/skills/", "Skills", "code"),
    ("/education/", "Education", "book"), ("/contact/", "Contact", "mail"),
]

COLOR_VAR = {"pink": "var(--pink)", "peach": "var(--peach)", "lav": "var(--lav)", "green": "var(--green)",
             "sky": "var(--sky)", "butter": "var(--butter)"}
AREA_LABEL = {k: v for k, v, _ in AREAS}



# ---------------------------------------------------------------- skill icons
LINE_ICONS = {
    "cpu": '<rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M9 1v3M15 1v3M9 20v3M15 20v3M20 9h3M20 14h3M1 9h3M1 14h3"/>',
    "layers": '<path d="M12 2 2 7l10 5 10-5-10-5z"/><path d="m2 17 10 5 10-5"/><path d="m2 12 10 5 10-5"/>',
    "repeat": '<path d="m17 1 4 4-4 4"/><path d="M3 11V9a4 4 0 0 1 4-4h14"/><path d="m7 23-4-4 4-4"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "zap": '<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>',
    "eye": '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>',
    "image": '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="m21 15-5-5L5 21"/>',
    "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>',
    "check": '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m22 4-10 10.01-3-3"/>',
    "database": '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M16 13H8M16 17H8M10 9H8"/>',
    "terminal": '<path d="m4 17 6-6-6-6"/><path d="M12 19h8"/>',
    "code": '<path d="m16 18 6-6-6-6"/><path d="m8 6-6 6 6 6"/>',
    "activity": '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>',
    "message": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
    "network": '<circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="m8.59 13.51 6.83 3.98M15.41 6.51l-6.82 3.98"/>',
    "crosshair": '<circle cx="12" cy="12" r="10"/><path d="M22 12h-4M6 12H2M12 6V2M12 22v-4"/>',
    "filter": '<path d="M22 3H2l8 9.46V19l4 2v-8.54L22 3z"/>',
    "sliders": '<path d="M4 21v-7M4 10V3M12 21v-9M12 8V3M20 21v-5M20 12V3M1 14h6M9 8h6M17 16h6"/>',
    "trend": '<path d="m23 6-9.5 9.5-5-5L1 18"/><path d="M17 6h6v6"/>',
    "globe": '<circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
    "box": '<path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><path d="m3.27 6.96 8.73 5.05 8.73-5.05M12 22.08V12"/>',
    "chart": '<path d="M18 20V10M12 20V4M6 20v-6"/>',
    "mic": '<rect x="9" y="2" width="6" height="12" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v4"/>',
    "flask": '<path d="M9 2h6M10 2v6L4 19a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2l-6-11V2"/>',
    "wrench": '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.6 2.6-2.4-.6-.6-2.4z"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    "brain": '<path d="M9 3a3 3 0 0 0-3 3 3 3 0 0 0-2 5 3 3 0 0 0 2 5 3 3 0 0 0 3 5h1V3z"/><path d="M15 3a3 3 0 0 1 3 3 3 3 0 0 1 2 5 3 3 0 0 1-2 5 3 3 0 0 1-3 5h-1V3z"/>',
    "route": '<circle cx="6" cy="19" r="3"/><circle cx="18" cy="5" r="3"/><path d="M9 19h8a3.5 3.5 0 0 0 0-7H7a3.5 3.5 0 0 1 0-7h8"/>',
}
# skill label -> ("brand", file in assets/icons) or ("line", key in LINE_ICONS)
SKILL_ICON = {
    "Python": ("brand", "python"), "Java": ("brand", "openjdk"), "SQL": ("line", "database"), "FastAPI": ("brand", "fastapi"),
    "REST APIs": ("line", "globe"), "Pydantic": ("brand", "pydantic"), "OpenAPI / Swagger": ("brand", "swagger"),
    "Object-oriented programming": ("line", "box"), "Git": ("brand", "git"), "Linux": ("brand", "linux"),
    "scikit-learn": ("brand", "scikitlearn"), "PyTorch": ("brand", "pytorch"), "TensorFlow": ("brand", "tensorflow"),
    "Neural networks": ("line", "network"), "CNNs": ("line", "layers"), "RNNs": ("line", "repeat"), "LSTM": ("line", "clock"),
    "Transformers": ("line", "zap"), "Transfer learning": ("line", "sliders"), "GANs": ("line", "activity"),
    "Diffusion models": ("line", "image"), "Model evaluation": ("line", "trend"),
    "Large language models": ("line", "message"), "Prompt engineering": ("line", "terminal"),
    "Retrieval-augmented generation (RAG)": ("line", "search"), "Hugging Face Transformers": ("brand", "huggingface"),
    "LLM API integration": ("line", "code"), "Structured outputs": ("line", "file"), "LLM-based evaluation": ("line", "check"),
    "OpenCV": ("brand", "opencv"), "Image processing": ("line", "image"), "Object detection": ("line", "crosshair"),
    "Object tracking": ("line", "eye"), "YOLO": ("brand", "ultralytics"), "Medical image analysis": ("line", "activity"),
    "pandas": ("brand", "pandas"), "NumPy": ("brand", "numpy"), "SciPy": ("brand", "scipy"), "Data processing": ("line", "sliders"),
    "Data cleaning": ("line", "filter"), "Data validation": ("line", "check"), "Document parsing (PDF / DOCX)": ("line", "file"),
    "Power BI": ("line", "chart"),
    "PostgreSQL": ("brand", "postgresql"), "SQLAlchemy": ("brand", "sqlalchemy"), "Redis": ("brand", "redis"),
    "Docker": ("brand", "docker"), "Docker Compose": ("brand", "docker"), "Streamlit": ("brand", "streamlit"),
    "Contrastive learning": ("line", "repeat"), "Explainable AI (XAI)": ("line", "eye"), "Graph neural networks": ("line", "network"),
    "Physics-informed neural networks": ("line", "activity"),
    # tags used under projects, experience and research
    "Alembic": ("line", "database"), "Bale API": ("line", "message"), "CNN": ("line", "layers"), "CRNN": ("line", "layers"),
    "CTC loss": ("line", "trend"), "Excel": ("line", "chart"), "Faster Whisper": ("line", "mic"), "GAN": ("line", "activity"),
    "Grad-CAM": ("line", "eye"), "Jupyter": ("line", "code"), "LLMs": ("line", "message"), "LabelMe": ("line", "crosshair"),
    "ONNX": ("line", "box"), "RDKit": ("line", "flask"), "RNN": ("line", "repeat"), "ResNet18": ("line", "layers"),
    "SVM": ("line", "sliders"), "TensorFlow / Keras": ("brand", "tensorflow"), "YOLOv5": ("brand", "ultralytics"),
    "aiogram": ("line", "message"), "matplotlib": ("line", "chart"), "pytest": ("line", "check"),
    "Predictive maintenance": ("line", "wrench"), "Prescriptive maintenance": ("line", "wrench"),
    "Retrieval-augmented generation": ("line", "search"), "Explainable AI": ("line", "eye"),
    "fMRI and functional connectivity": ("line", "brain"), "Object detection and tracking": ("line", "crosshair"),
    "Molecular structures": ("line", "flask"),
    "Maintenance strategies: preventive, predictive and prescriptive": ("line", "wrench"),
    "Retrieval- and knowledge-augmented generation (RAG, KAG)": ("line", "search"),
    "Decision mining in process-aware information systems": ("line", "route"),
    "Log anomaly detection with retrieval-augmented generation": ("line", "terminal"),
    "Voice-enabled digital assistants for maintenance": ("line", "mic"),
    "Fault diagnosis and forecasting for wind and solar energy": ("line", "sun"),
    "Condition monitoring and remaining-useful-life prediction": ("line", "activity"),
    "Knowledge graphs and domain knowledge for LLMs": ("line", "network"),
    "Reading analog gauges and needle instruments with computer vision": ("line", "crosshair"),
    "Segmentation, detection and RGB-D perception": ("line", "image"),
    "Graph neural networks and functional connectivity in neuroimaging": ("line", "brain"),
    "Molecular representation learning and 3D structure": ("line", "flask"),
}


def skill_icon(label, color_var="var(--pink)"):
    kind, key = SKILL_ICON.get(label, ("line", "cpu"))
    if kind == "brand":
        return f'<img class="ico" src="/assets/icons/{key}.svg" alt="" width="16" height="16" loading="lazy">'
    return f'<svg class="lico" viewBox="0 0 24 24" aria-hidden="true" style="--g:{color_var}">{LINE_ICONS[key]}</svg>'


def skill_chips(items, color_var):
    return '<ul class="chips">' + "".join(f'<li class="chip has-ico">{skill_icon(t, color_var)}{esc(t)}</li>' for t in items) + "</ul>"

# ---------------------------------------------------------------- pieces
def chips(items):
    return skill_chips(items, "var(--a, var(--pink))")


def ticks(items):
    return '<ul class="ticks">' + "".join(f"<li>{esc(t)}</li>" for t in items) + "</ul>"


def project_card(p, extra=""):
    return (f'<a class="card c-{p["color"]} reveal" href="/projects/{p["slug"]}/" data-areas="{" ".join(p["areas"])}"{extra}>'
            f'<div class="top"><span class="area"><i>{icon("grid")}</i>{esc(p["label"])}</span><span class="metric">{esc(p["period"])}</span></div>'
            f'<h3>{esc(p["title"])}</h3><p>{esc(p["summary"])}</p>'
            f'{chips(p["tech"][:4])}'
            f'<span class="more">Read the case study {icon("arrow", "btn-icon")}</span></a>')


SPARK = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 0c.8 6.2 5.8 11.2 12 12-6.2.8-11.2 5.8-12 12-.8-6.2-5.8-11.2-12-12C6.2 11.2 11.2 6.2 12 0z" fill="currentColor"/></svg>'


def shell(title, desc, path, body, crumbs=None, jsonld=None, og_image="/assets/img/avatar.webp"):
    nav = "".join(
        f'<a href="{href}"{" aria-current=\"page\"" if (path == href or (href != "/" and path.startswith(href))) else ""}>{label}</a>'
        for href, label, _ in NAV)
    crumb_html = ""
    if crumbs:
        parts = []
        for i, (label, href) in enumerate(crumbs):
            parts.append(f'<a href="{href}">{esc(label)}</a>' if href else f'<span aria-current="page">{esc(label)}</span>')
            if i < len(crumbs) - 1:
                parts.append('<span aria-hidden="true">/</span>')
        crumb_html = f'<nav class="crumbs" aria-label="Breadcrumb">{"".join(parts)}</nav>'
    full_title = title if path == "/" else f"{title} · {PROFILE['name']}"
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{SITE_URL}{path}">
<meta property="og:type" content="website"><meta property="og:title" content="{esc(full_title)}"><meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{SITE_URL}{path}"><meta property="og:image" content="{SITE_URL}{og_image}"><meta name="twitter:card" content="summary">
<meta name="theme-color" content="#120d12"><meta name="color-scheme" content="dark">
<script>document.documentElement.classList.add("js")</script>
<link rel="icon" href="/favicon.svg?v=2" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png?v=2" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v=2">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;0,9..40,800&family=Instrument+Serif:ital@0;1&display=swap">
<link rel="stylesheet" href="/assets/css/style.css?v={ver("assets/css/style.css")}">
{ld}
</head>
<body>
<a class="skip" href="#content">Skip to content</a>
<header class="top-bar"><div class="top-inner">
  <a class="brand" href="/" aria-label="Home"><span class="name">{esc(PROFILE["name"])}</span></a>
  <nav class="nav" aria-label="Main">{nav}</nav>
</div></header>
<div class="wrap"><main id="content">
{crumb_html}
{body}
<footer class="site"><span>© 2026 {esc(PROFILE["name"])}</span><span>{esc(PROFILE["location"])} · static site on GitHub Pages</span></footer>
</main></div>
<script src="/assets/js/main.js?v={ver("assets/js/main.js")}" defer></script>
</body>
</html>
'''


def write(path, content):
    full = os.path.join(ROOT, path.strip("/"), "index.html") if not path.endswith(".html") else os.path.join(ROOT, path.strip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


# ---------------------------------------------------------------- pages
def page_home():
    order = ["ai-resume-evaluation-service", "ai-data-labeling-platform", "industrial-gauge-localization", "explainable-skin-disease-classification", "voiceledger", "telegram-services-platform"]
    featured = [next(p for p in PROJECTS if p["slug"] == k) for k in order]
    tools = [("python", "Python"), ("pytorch", "PyTorch"), ("tensorflow", "TensorFlow"), ("scikitlearn", "scikit-learn"), ("pandas", "pandas"),
             ("opencv", "OpenCV"), ("fastapi", "FastAPI"), ("postgresql", "PostgreSQL"), ("docker", "Docker"), ("git", "Git")]
    tiles = "".join(f'<div class="tile"><i><img src="/assets/icons/{a}.svg" alt="" width="30" height="30"></i><span>{esc(b_)}</span></div>' for a, b_ in tools)
    skills = ["Machine learning", "Deep learning", "Computer vision", "LLMs and RAG", "Data analysis", "Backend and APIs", "Explainable AI", "Graph neural networks"]
    skill_chips = "".join(f'<li class="chip">{esc(s_)}</li>' for s_ in skills)
    body = f'''<section class="hero">
  <div class="arch" aria-hidden="false">
    <span class="spark s1">{SPARK}</span><span class="spark s2">{SPARK}</span>
    <div class="frame"><img src="/assets/img/avatar-arch.webp" width="480" height="480" alt="Illustrated portrait of Fatemeh at her computer"></div>
  </div>
  <div>
    <span class="greet">hi there!</span>
    <p class="intro">I am <b>Fatemeh Harirforoush</b>, an AI software engineer and machine learning engineer. I build end-to-end intelligent systems, from messy data to a working product, and I check honestly whether they work.</p>
    <hr class="rule">
    <ul class="contact-lines">
      <li>{icon("github")}<a href="{PROFILE["github"]}" rel="me noopener" target="_blank">github.com/ftharir</a></li>
      <li>{icon("linkedin")}<a href="{PROFILE["linkedin"]}" rel="me noopener" target="_blank">LinkedIn</a></li>
      <li>{icon("mail")}<a href="mailto:{PROFILE["email"]}">{esc(PROFILE["email"])}</a></li>
      <li>{icon("pin")}<span>{esc(PROFILE["location"])}</span></li>
    </ul>
    <div class="now-chip"><i></i>Now: building an LLM-based resume evaluation service at Sharif Setup</div>
    <div class="btn-row" style="margin-top:24px"><a class="btn" href="/projects/">See my projects {icon("arrow")}</a><a class="btn ghost" href="/contact/">Get in touch</a></div>
  </div>
</section>

<div class="cols">
  <div>
    <h2 class="tag c-lav">Education</h2>
    <div class="entry reveal"><div class="when">2022 – 2026</div><b>B.Sc. in Computer Engineering</b><span>Science and Research University, Tehran</span></div>
    <div class="entry reveal"><div class="when">2023 – 2024</div><b>Auditing student, advanced AI and ML courses</b><span>Sharif University of Technology</span></div>
    <div class="entry reveal"><div class="when">2019 – 2022</div><b>Associate degree in Mathematical Physics</b><span>Sampad Tizhooshan Farzanegan 2, Ahwaz</span></div>
    <p><a class="btn ghost" href="/education/">Education {icon("arrow")}</a></p>

    <h2 class="tag c-green" style="margin-top:44px">Experience</h2>
    <div class="entry reveal"><div class="when">2026 – present</div><b>AI Software Engineering Intern · Project Owner</b><span>Sharif Setup, generative AI startup</span></div>
    <div class="entry reveal"><div class="when">2023 – 2024</div><b>Data Scientist Bootcamp trainee</b><span>Fanap, selected through Quera's Hafez competition</span></div>
    <div class="entry reveal"><div class="when">2026</div><b>Freelance AI software engineer</b><span>Voice-report assistant, Telegram platform, cost allocation</span></div>
    <p><a class="btn ghost" href="/experience/">Experience {icon("arrow")}</a></p>
  </div>
  <div>
    <h2 class="tag c-butter">Skills</h2>
    <ul class="chips" style="margin-top:0">{skill_chips}</ul>
    <h2 class="tag c-pink" style="margin-top:44px">Tools</h2>
    <div class="tiles">{tiles}</div>
    <p style="margin-top:18px"><a class="btn ghost" href="/skills/">All skills {icon("arrow")}</a></p>

    <h2 class="tag c-lav" style="margin-top:44px">Research</h2>
    <div class="mini-timeline">
      <div class="entry reveal"><div class="when">2025 – 2026</div><b>AI Researcher</b><span>Predictive maintenance: Transformers, PINNs, diffusion models</span></div>
      <div class="entry reveal"><div class="when">2024 – 2025</div><b>Research Assistant, computer vision</b><span>Detection and tracking for quadcopters</span></div>
      <div class="entry reveal"><div class="when">2024 – 2025</div><b>Research Assistant, neuroimaging</b><span>fMRI and graph neural networks</span></div>
      <div class="entry reveal"><div class="when">2026</div><b>Survey on RAG for maintenance decisions</b><span>SSRN preprint, under review at a Q1 journal</span></div>
    </div>
    <p><a class="btn ghost" href="/research/">Research {icon("arrow")}</a></p>
  </div>
</div>

<section class="block">
  <h2 class="tag c-peach">Projects</h2>
  <div class="cards">{"".join(project_card(p) for p in featured)}</div>
  <p style="margin-top:20px"><a class="btn" href="/projects/">All {len(PROJECTS)} projects {icon("arrow")}</a></p>
</section>

<section class="block">
  <div class="box c-pink reveal" style="text-align:center;padding:44px 28px">
    <h3 style="font-family:var(--serif);font-weight:400;font-size:2.3rem;margin-bottom:22px">Have an idea, a project, or just a hello?</h3>
    <a class="btn" href="/contact/">Send me a message {icon("arrow")}</a>
  </div>
</section>'''
    ld = {"@context": "https://schema.org", "@type": "Person", "name": PROFILE["name"], "jobTitle": "AI Software Engineer",
          "url": SITE_URL + "/", "sameAs": [PROFILE["github"], PROFILE["linkedin"]], "address": {"@type": "PostalAddress", "addressLocality": "Tehran", "addressCountry": "IR"}}
    return shell(f"{PROFILE['name']} — AI Software Engineer", PROFILE["summary"], "/", body, jsonld=ld)


def page_about():
    paras = "".join(f"<p>{esc(t)}</p>" for t in ABOUT_PARAGRAPHS)
    body = f'''<h1>About <em>me</em></h1>
<p class="lead">{esc(PROFILE["tagline"])}</p>
<div class="box reveal">{paras}</div>
<h2>In short</h2>
<div class="grid-2">
  <div class="box sand reveal"><h3>Based in</h3><p>{esc(PROFILE["location"])}</p></div>
  <div class="box sand reveal"><h3>Education</h3><p>B.Sc. Computer Engineering (2022 – 2026), with advanced AI and machine-learning courses audited at Sharif University of Technology.</p></div>
  <div class="box sand reveal"><h3>Now</h3><p>AI Software Engineering Intern at Sharif Setup: delivered a data labeling platform, now building an LLM-based resume evaluation service.</p></div>
  <div class="box sand reveal"><h3>Research</h3><p>Predictive maintenance with Transformers and diffusion models; computer vision; neuroimaging with graph neural networks.</p></div>
</div>
<h2>Where to go next</h2>
<div class="pills"><a href="/experience/">Experience</a><a href="/research/">Research</a><a href="/projects/">Projects</a><a href="/skills/">Skills</a></div>'''
    return shell("About", PROFILE["summary"], "/about/", body, crumbs=[("Home", "/"), ("About", None)])


def logo_badge(it):
    if not it.get("logo"):
        return ""
    return f'<span class="t-logo"><img src="/assets/img/logos/{it["logo"]}" alt="" width="30" height="30" loading="lazy"></span>'


def timeline(items, with_kind=True):
    out = []
    for it in items:
        meta = f'<span class="pill">{esc(it["period"])}</span>' + (f'<span class="pill">{esc(it["kind"])}</span>' if it.get("kind") else "")
        if it.get("sections"):
            inner = ""
            for sec in it["sections"]:
                state = "done" if sec["status"].lower() == "completed" else "wip"
                lnk = f'<p><a class="btn ghost" href="{sec["link"]}">Read the case study {icon("arrow")}</a></p>' if sec.get("link") else ""
                inner += (f'<div class="sub"><h4>{esc(sec["title"])} <span class="status {state}">{esc(sec["status"])}</span></h4>'
                          f'{ticks(sec["bullets"])}{chips(sec["tech"])}{lnk}</div>')
            out.append(f'<article class="t-item reveal{" has-logo" if it.get("logo") else ""}" style="--dot:{COLOR_VAR[it["color"]]}">{logo_badge(it)}<div class="t-meta">{meta}</div>'
                       f'<h3>{esc(it["role"])}</h3><p class="org">{esc(it["org"])}</p>{inner}</article>')
            continue
        link = f'<p><a class="btn ghost" href="{it["link"]}">Read the case study {icon("arrow")}</a></p>' if it.get("link") else ""
        out.append(f'<article class="t-item reveal{" has-logo" if it.get("logo") else ""}" style="--dot:{COLOR_VAR[it["color"]]}">{logo_badge(it)}<div class="t-meta">{meta}</div>'
                   f'<h3>{esc(it["role"])}</h3><p class="org">{esc(it["org"])}</p>' + (f'<p class="summary">{esc(it["summary"])}</p>' if it.get("summary") else "") + f'{ticks(it["bullets"])}{chips(it["tech"])}{link}</article>')
    return '<div class="timeline">' + "".join(out) + "</div>"


def page_experience():
    body = f'''<h1>Professional <em>experience</em></h1>
<p class="lead">Engineering work: an AI data labeling platform, an LLM-based resume evaluation service, freelance AI products and an applied data-science bootcamp.</p>
{timeline(EXPERIENCE)}'''
    return shell("Experience", "Professional experience of Fatemeh Harirforoush: AI software engineering internship, freelance projects and data science bootcamp.", "/experience/", body,
                 crumbs=[("Home", "/"), ("Experience", None)])


def page_research():
    pubs = "".join(
        f'<div class="box c-lav reveal"><p class="eyebrow">Publication</p><h3>{esc(x["title"])}</h3>'
        f'<p style="margin-bottom:6px">{esc(x["authors"])}</p><p class="muted">{esc(x["status"])}</p>'
        f'<div class="btn-row" style="margin-top:14px">' + "".join(
            f'<a class="btn{"" if i == 0 else " ghost"}" href="{esc(u)}" target="_blank" rel="noopener">{esc(t)} {icon("arrow")}</a>'
            for i, (t, u) in enumerate(x["links"])) + "</div></div>" for x in PUBLICATIONS)
    intro = "".join(f"<p>{esc(t)}</p>" for t in RESEARCH_INTRO)
    survey = "".join(f"<p>{esc(t)}</p>" for t in RESEARCH_ABOUT_SURVEY)
    methods = "".join(
        f'<div class="card compact c-{col} reveal"><h3>{esc(name)}</h3><p>{esc(text)}</p></div>' for name, col, text in METHODS)
    body = f'''<h1>Research &amp; <em>academic</em> work</h1>
<p class="lead">Research roles at Sharif University of Technology and the Sharif Center for Information Systems and Data Science, and the survey that came out of them.</p>
<div class="grid-3">
  <div class="stat c-lav reveal"><b>{len(RESEARCH)}</b><span>research roles and tasks</span></div>
  <div class="stat c-pink reveal"><b>1</b><span>survey: SSRN preprint, under review at a Q1 journal</span></div>
  <div class="stat c-green reveal"><b>2024</b><span>research work since</span></div>
</div>
<h2>What I research</h2>
<div class="box sand reveal">{intro}</div>
<h2>Publication</h2>
{pubs}
<div class="box reveal" style="margin-top:16px"><h3>About the survey</h3>{survey}</div>
<h2>Research positions and tasks</h2>
{timeline(RESEARCH)}
<h2>Methods I worked with, in short</h2>
<p class="muted" style="margin-top:-6px">Plain-language background for the methods named above; these are explanations, not results.</p>
<div class="cards">{methods}</div>
<h2>Literature areas I studied</h2>
<div class="box reveal">{chips(LITERATURE)}</div>
<h2>Research topics</h2>
<div class="box reveal">{chips(["Predictive maintenance", "Prescriptive maintenance", "Transformers", "Contrastive learning", "Physics-informed neural networks", "Diffusion models", "Retrieval-augmented generation", "Explainable AI", "Graph neural networks", "fMRI and functional connectivity", "Object detection and tracking", "Molecular structures"])}</div>'''
    return shell("Research", "Research experience and publications: predictive maintenance, computer vision for quadcopters, neuroimaging with graph neural networks, molecular structures, ", "/research/", body,
                 crumbs=[("Home", "/"), ("Research", None)])


def page_projects():
    pills = '<button type="button" data-filter="all" aria-pressed="true">All <span class="count">' + str(len(PROJECTS)) + "</span></button>"
    for k, lbl, _ in AREAS:
        n = sum(1 for p in PROJECTS if k in p["areas"])
        pills += f'<button type="button" data-filter="{k}" aria-pressed="false">{esc(lbl)} <span class="count">{n}</span></button>'
    body = f'''<h1>Selected <em>projects</em></h1>
<p class="lead">Course work taken past its brief, freelance products, research tasks and tools built because nothing else did the job. Each one has a case study with the numbers.</p>
<div class="pills" role="group" aria-label="Filter projects">{pills}</div>
<p class="muted" id="filter-live" aria-live="polite" style="margin:-10px 0 16px"></p>
<div class="cards">{"".join(project_card(p) for p in PROJECTS)}</div>'''
    return shell("Projects", "Case studies: computer vision, data analysis, machine learning, backend and speech projects with results.", "/projects/", body,
                 crumbs=[("Home", "/"), ("Projects", None)])


def flow_html(steps):
    return '<div class="flow">' + '<span class="arrow" aria-hidden="true">→</span>'.join(f"<span>{esc(s)}</span>" for s in steps) + "</div>"


def page_project(i, p):
    facts = "".join(f'<div class="fact"><b>{esc(a_)}</b><span>{esc(b_)}</span></div>' for a_, b_ in p["facts"])
    repo_btn = (f'<a class="btn" href="{PROFILE["github"]}/{p["repo"]}" target="_blank" rel="noopener">{icon("github")} View on GitHub</a>'
                if p.get("repo") else '<span class="pill dark">Company project · no public repository</span>')
    role = f'<p class="role-line"><b>Role</b> {esc(p["role"])}</p>' if p.get("role") else ""

    if p.get("overview"):
        intro = '<h2 style="margin-top:8px">Overview</h2><div class="box reveal">' + "".join(f"<p>{esc(t)}</p>" for t in p["overview"]) + "</div>"
    else:
        intro = f'<h2 style="margin-top:8px">The problem</h2><p>{esc(p["problem"])}</p>'

    approach = ""
    if p.get("approach"):
        steps = "".join(f'<li class="step reveal"><span class="n">{n}</span><div><h3>{esc(t)}</h3><p>{esc(d)}</p></div></li>' for n, (t, d) in enumerate(p["approach"], 1))
        approach = f'<h2>Approach</h2><ol class="steps">{steps}</ol>'
    elif p.get("built"):
        approach = f'<h2>What I built</h2>{ticks(p["built"])}'

    decisions = ""
    if p.get("decisions"):
        cards = "".join(f'<div class="decide reveal"><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for t, d in p["decisions"])
        decisions = f'<h2>Key decisions</h2><div class="decisions c-{p["color"]}">{cards}</div>'

    results = ""
    if p.get("table"):
        rows = "".join(f"<tr><td>{esc(a_)}</td><td>{esc(b_)}</td><td>{esc(c_)}</td></tr>" for a_, b_, c_ in p["table"])
        results = f'<h2>{esc(p.get("metrics_title", "Original versus follow-up"))}</h2><table><thead><tr><th>Project</th><th>Original</th><th>Follow-up</th></tr></thead><tbody>{rows}</tbody></table>'
    elif p.get("metrics"):
        rows = "".join(f"<tr><td>{esc(a_)}</td><td><b>{esc(b_)}</b></td><td>{esc(c_)}</td></tr>" for a_, b_, c_ in p["metrics"])
        results = f'<h2>{esc(p.get("metrics_title", "Results"))}</h2><table><thead><tr><th>Measure</th><th>Value</th><th>Note</th></tr></thead><tbody>{rows}</tbody></table>'
    elif p.get("results"):
        results = f'<h2>Results</h2>{ticks(p["results"])}'

    insights = ""
    if p.get("insights"):
        cards = "".join(f'<div class="decide reveal"><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for t, d in p["insights"])
        insights = f'<h2>What the analysis showed</h2><div class="decisions c-{p["color"]}">{cards}</div>'

    flow = f'<h2>How it works</h2>{flow_html(p["flow"])}' if p.get("flow") else ""

    imgs = ""
    if p.get("images"):
        figs = "".join(f'<figure><img src="/assets/img/projects/{p["slug"]}/{out}" alt="{esc(cap)}" loading="lazy"><figcaption>{esc(cap)}</figcaption></figure>' for _, out, cap in p["images"])
        imgs = f'<h2>Figures</h2><div class="gallery{" one" if (len(p["images"]) == 1 or p.get("gallery") == "one") else ""}">{figs}</div>'

    limits = f'<h2>Limitations, stated openly</h2>{ticks(p["limits"])}' if p.get("limits") else ""
    nxt = f'<h2>What is next</h2>{ticks(p["next"])}' if p.get("next") else ""

    prev_p, next_p = PROJECTS[i - 1] if i > 0 else None, PROJECTS[i + 1] if i < len(PROJECTS) - 1 else None
    nav = '<div class="next-prev">' + (f'<a class="btn ghost" href="/projects/{prev_p["slug"]}/">← {esc(prev_p["title"])}</a>' if prev_p else "<span></span>") + \
          (f'<a class="btn ghost" href="/projects/{next_p["slug"]}/">{esc(next_p["title"])} →</a>' if next_p else "<span></span>") + "</div>"
    body = f'''<section class="hero-card c-{p["color"]}">
<p class="eyebrow">{esc(p["label"])} · {esc(p["period"])}</p>
<h1>{esc(p["title"])}</h1>
<p class="lead">{esc(p["lead"])}</p>
{role}
<div class="facts">{facts}</div>
{chips(p["tech"])}
<div class="btn-row" style="margin-top:18px">{repo_btn}<a class="btn ghost" href="/projects/">All projects</a></div>
</section>
{intro}
{approach}
{decisions}
{results}
{insights}
{flow}
{imgs}
{limits}
{nxt}
{nav}'''
    return shell(p["title"], p["lead"], f"/projects/{p['slug']}/", body,
                 crumbs=[("Home", "/"), ("Projects", "/projects/"), (p["title"], None)])


def page_skills():
    groups = "".join(
        f'<section class="skill-group box reveal"><h3><span class="dot" style="background:{COLOR_VAR[col]}"></span>{esc(title)}</h3>{skill_chips(items, COLOR_VAR[col])}</section>'
        for title, col, items in SKILLS)
    body = f'''<h1>Technical <em>skills</em></h1>
<p class="lead">What I use, grouped by what it is for. Each skill appears in at least one project on this site.</p>
<div class="grid-2">{groups}</div>'''
    return shell("Skills", "Technical skills: Python, machine learning, deep learning, LLMs, computer vision, data engineering, backend and deployment.", "/skills/", body,
                 crumbs=[("Home", "/"), ("Skills", None)])


def page_education():
    cards = "".join(
        f'<article class="t-item reveal" style="--dot:{COLOR_VAR[e["color"]]}"><div class="t-meta"><span class="pill">{esc(e["period"])}</span></div><h3>{esc(e["title"])}</h3>'
        f'<p class="org">{esc(e["org"])}</p>{"<p>" + esc(e["text"]) + "</p>" if e["text"] else ""}</article>' for e in EDUCATION)
    acts = "".join(
        f'<article class="t-item reveal{" has-logo" if a_.get("logo") else ""}" style="--dot:{COLOR_VAR[a_["color"]]}">{logo_badge(a_)}<div class="t-meta"><span class="pill">{esc(a_["period"])}</span></div>'
        f'<h3>{esc(a_["title"])}</h3><p class="org">{esc(a_["org"])}</p>{"<p>" + esc(a_["text"]) + "</p>" if a_["text"] else ""}'
        + (f'<p style="margin-top:12px"><a class="btn ghost" href="{esc(a_["link"])}" target="_blank" rel="noopener">{esc(a_["link_label"])} {icon("arrow")}</a></p>' if a_.get("link") else "")
        + '</article>' for a_ in ACTIVITIES)
    courses = "".join(f'<li class="chip">{esc(t)} · {esc(p)}</li>' for t, p in COURSES)
    body = f'''<h1><em>Education</em></h1>
<p class="lead">A computer engineering degree, extended with advanced AI courses, a competitive data-science bootcamp, student projects and online courses.</p>
<div class="timeline">{cards}</div>
<h2>Academic activities</h2>
<div class="timeline">{acts}</div>
<h2>Courses and workshops</h2>
<div class="box reveal"><ul class="chips" style="margin:0">{courses}</ul></div>'''
    return shell("Education", "Education: B.Sc. Computer Engineering, audited AI courses at Sharif University of Technology, associate degree in mathematical physics.", "/education/", body,
                 crumbs=[("Home", "/"), ("Education", None)])


def page_contact():
    body = f'''<h1>Let's <em>talk</em></h1>
<p class="lead">The best way to reach me is email. I read every message.</p>
<div class="cards">
  <div class="card compact c-peach reveal"><div class="top"><span class="area"><i>{icon("mail")}</i>Email</span></div><h3 class="mail">{esc(PROFILE["email"])}</h3>
    <div class="btn-row" style="margin-top:auto;padding-top:16px"><a class="btn" href="mailto:{PROFILE["email"]}">Write an email</a><button class="btn ghost" type="button" data-copy="{PROFILE["email"]}">{icon("copy")} Copy</button></div></div>
  <a class="card compact c-sky reveal" href="{PROFILE["linkedin"]}" target="_blank" rel="noopener me"><div class="top"><span class="area"><i>{icon("linkedin")}</i>LinkedIn</span></div><h3>Fatemeh Harirforoush</h3><p>Experience, research and recommendations.</p><span class="more">Open LinkedIn {icon("arrow", "btn-icon")}</span></a>
  <a class="card compact c-lav reveal" href="{PROFILE["github"]}" target="_blank" rel="noopener me"><div class="top"><span class="area"><i>{icon("github")}</i>GitHub</span></div><h3>@ftharir</h3><p>All projects, with code, data and documentation.</p><span class="more">Open GitHub {icon("arrow", "btn-icon")}</span></a>
  <div class="card compact c-green reveal"><div class="top"><span class="area"><i>{icon("grid")}</i>Location</span></div><h3>{esc(PROFILE["location"])}</h3><p>Remote collaboration is fine.</p></div>
</div>
<h2>Send me a message</h2>
<p class="lead" style="margin-top:-6px">For collaboration, or even just to say hi.</p>
<form class="box c-white contact-form reveal" id="contact-form" data-endpoint="{esc(CONTACT_FORM_ENDPOINT)}" data-mailto="{PROFILE["email"]}" novalidate>
  <div class="form-grid">
    <label>Your name<input type="text" name="name" autocomplete="name" required maxlength="80" placeholder="Jane Doe"></label>
    <label>Your email<input type="email" name="email" autocomplete="email" required maxlength="120" placeholder="so I can reply: jane@example.com"></label>
  </div>
  <label>Message<textarea name="message" rows="6" required maxlength="3000" placeholder="Hi Fatemeh, ..."></textarea></label>
  <input type="text" name="_gotcha" tabindex="-1" autocomplete="off" aria-hidden="true" class="hp">
  <div class="btn-row"><button class="btn" type="submit">Send message {icon("arrow")}</button></div>
  <p class="form-status" id="form-status" role="status" aria-live="polite"></p>
</form>'''
    return shell("Contact", "Contact Fatemeh Harirforoush: email, LinkedIn and GitHub.", "/contact/", body, crumbs=[("Home", "/"), ("Contact", None)])


def page_404():
    body = '<h1>Page <em>not found</em></h1><p class="lead">This page does not exist. Try the home page or the projects.</p><div class="btn-row"><a class="btn" href="/">Home</a><a class="btn ghost" href="/projects/">Projects</a></div>'
    return shell("Not found", "Page not found.", "/404.html", body)


# ---------------------------------------------------------------- assets
def prepare_images():
    from PIL import Image
    avatar_out = os.path.join(ROOT, "assets/img/avatar.webp")
    if AVATAR_SOURCE and os.path.exists(AVATAR_SOURCE):
        Image.open(AVATAR_SOURCE).convert("RGB").resize((480, 480), Image.LANCZOS).save(avatar_out, "WEBP", quality=88)
    for p in PROJECTS:
        for src, out, _ in p.get("images", []):
            dst = os.path.join(ROOT, "assets/img/projects", p["slug"], out)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if os.path.exists(dst):
                continue
            src_path = os.path.join(IMAGE_SOURCE, src.replace("/", os.sep))
            if src.lower().endswith(".gif"):
                shutil.copyfile(src_path, dst)
            else:
                im = Image.open(src_path).convert("RGB")
                if im.width > 1400:
                    im = im.resize((1400, round(im.height * 1400 / im.width)), Image.LANCZOS)
                im.save(dst, "WEBP", quality=84)


def make_favicon_pngs():
    """Raster versions of the 'fh' icon for browsers that do not use the SVG (Safari, iOS home screen)."""
    from PIL import Image, ImageDraw, ImageFont
    font_path = next((p for p in (r"C:\Windows\Fonts\georgiai.ttf", r"C:\Windows\Fonts\timesi.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf") if os.path.exists(p)), None)
    for size, name in ((32, "favicon-32.png"), (180, "apple-touch-icon.png")):
        scale = 8
        big = size * scale
        im = Image.new("RGBA", (big, big), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((0, 0, big - 1, big - 1), radius=int(big * 0.25), fill="#120d12")
        font = ImageFont.truetype(font_path, int(big * 0.60)) if font_path else ImageFont.load_default()
        bbox = d.textbbox((0, 0), "fh", font=font)
        d.text(((big - (bbox[2] - bbox[0])) / 2 - bbox[0], (big - (bbox[3] - bbox[1])) / 2 - bbox[1] - big * 0.02), "fh", font=font, fill="#f08ab4")
        im.resize((size, size), Image.LANCZOS).save(os.path.join(ROOT, name))


def write_static():
    favicon = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="16" fill="#120d12"/>'
               '<text x="32" y="45" text-anchor="middle" font-family="Georgia, Times New Roman, serif" font-style="italic" font-size="38" fill="#f08ab4">fh</text></svg>')
    open(os.path.join(ROOT, "favicon.svg"), "w", encoding="utf-8").write(favicon)
    make_favicon_pngs()
    open(os.path.join(ROOT, ".nojekyll"), "w").write("")
    open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
    urls = ["/", "/about/", "/experience/", "/research/", "/projects/", "/skills/", "/education/", "/contact/"] + [f"/projects/{p['slug']}/" for p in PROJECTS]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{SITE_URL}{u}</loc></url>\n" for u in urls) + "</urlset>\n"
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(sm)


def main():
    prepare_images()
    write_static()
    write("/", page_home())
    write("/about/", page_about())
    write("/experience/", page_experience())
    write("/research/", page_research())
    write("/projects/", page_projects())
    for i, p in enumerate(PROJECTS):
        write(f"/projects/{p['slug']}/", page_project(i, p))
    write("/skills/", page_skills())
    write("/education/", page_education())
    write("/contact/", page_contact())
    write("/404.html", page_404())
    print("built", 8 + len(PROJECTS) + 1, "pages")


if __name__ == "__main__":
    main()
