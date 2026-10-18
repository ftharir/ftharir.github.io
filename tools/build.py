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


# ---------------------------------------------------------------- pieces
def chips(items):
    return '<ul class="chips">' + "".join(f'<li class="chip">{esc(t)}</li>' for t in items) + "</ul>"


def ticks(items):
    return '<ul class="ticks">' + "".join(f"<li>{esc(t)}</li>" for t in items) + "</ul>"


def project_card(p, extra=""):
    return (f'<a class="card c-{p["color"]} reveal" href="/projects/{p["slug"]}/" data-areas="{" ".join(p["areas"])}"{extra}>'
            f'<div class="top"><span class="area"><i>{icon("grid")}</i>{esc(p["label"])}</span><span class="metric">{esc(p["metric"])}</span></div>'
            f'<h3>{esc(p["title"])}</h3><p>{esc(p["summary"])}</p>'
            f'{chips(p["tech"][:4])}'
            f'<span class="more">Read the case study {icon("arrow", "btn-icon")}</span></a>')


def panel():
    counts = {k: sum(1 for p in PROJECTS if k in p["areas"]) for k, _, _ in AREAS}
    top = max(counts.values())
    bars = "".join(
        f'<div class="bar"><span>{esc(lbl)}</span><i style="--c:{COLOR_VAR[col]};--w:{counts[k] / top * 100:.0f}%"></i><em>{counts[k]}</em></div>'
        for k, lbl, col in AREAS)
    return f'''<aside class="panel" aria-label="Profile summary"><div class="panel-inner">
<section class="p-card profile">
  <img class="avatar" src="/assets/img/avatar.webp" width="104" height="104" alt="Illustrated portrait of Fatemeh">
  <h2>{esc(PROFILE["name"])}</h2>
  <p class="role">{esc(PROFILE["role"])}<br>{esc(PROFILE["location"])}</p>
  <div class="socials">
    <a href="{PROFILE["github"]}" rel="me noopener" target="_blank">{icon("github")}GitHub</a>
    <a href="{PROFILE["linkedin"]}" rel="me noopener" target="_blank">{icon("linkedin")}LinkedIn</a>
    <a href="mailto:{PROFILE["email"]}">{icon("mail")}Email</a>
  </div>
</section>
<section class="p-card"><h4>Projects by area <small>{len(PROJECTS)} total</small></h4><div class="bars">{bars}</div></section>
<section class="p-card now"><h4>Right now</h4><p><b>AI Software Engineering Intern</b>Building an LLM-based technical resume evaluation service at Sharif Setup, after delivering an AI data labeling platform.</p><small>August 2026 – present</small></section>
</div></aside>'''


def shell(title, desc, path, body, crumbs=None, jsonld=None, og_image="/assets/img/avatar.webp"):
    nav = "".join(
        f'<a class="nav" href="{href}" data-label="{label}" aria-label="{label}"{" aria-current=\"page\"" if (path == href or (href != "/" and path.startswith(href))) else ""}>{icon(ic)}</a>'
        for href, label, ic in NAV)
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
<meta name="theme-color" content="#c6efdd">
<script>document.documentElement.classList.add("js")</script>
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700&display=swap">
<link rel="stylesheet" href="/assets/css/style.css?v={ver("assets/css/style.css")}">
{ld}
</head>
<body>
<a class="skip" href="#content">Skip to content</a>
<div class="shell">
  <header class="rail"><div class="rail-inner">
    <a class="logo" href="/" aria-label="Home">FH</a>
    <nav aria-label="Main">{nav}</nav>
    <img class="avatar-mini" src="/assets/img/avatar.webp" width="44" height="44" alt="">
  </div></header>
  <main id="content">
    {crumb_html}
    {body}
    <footer class="site"><span>© 2026 {esc(PROFILE["name"])}</span><span>Designed and built by hand · static site on GitHub Pages</span></footer>
  </main>
  {panel()}
</div>
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
    pills = "".join(f'<a href="{href}">{esc(label)}</a>' for href, label, _ in NAV[2:])
    body = f'''<p class="eyebrow">Hello, I'm Fatemeh</p>
<h1>AI systems, from <em>messy data</em> to a working product.</h1>
<p class="lead">{esc(PROFILE["summary"])}</p>
<div class="btn-row"><a class="btn" href="/projects/">See my projects {icon("arrow")}</a><a class="btn ghost" href="/contact/">Get in touch</a></div>
<h2>Explore</h2>
<div class="pills">{pills}</div>
<h2>Featured projects</h2>
<div class="cards">{"".join(project_card(p) for p in featured)}</div>
<p style="margin-top:18px"><a class="btn ghost" href="/projects/">All {len(PROJECTS)} projects {icon("arrow")}</a></p>
<h2>At a glance</h2>
<div class="grid-3">
  <div class="stat c-pink reveal"><b>{len(PROJECTS)}</b><span>documented projects with results</span></div>
  <div class="stat c-lav reveal"><b>{len(RESEARCH)}</b><span>research roles and tasks</span></div>
  <div class="stat c-green reveal"><b>1</b><span>manuscript under review (Q1 journal)</span></div>
</div>
<h2>What I care about</h2>
<div class="box sand reveal"><p>Evaluation that does not flatter the model: leakage checks, held-out test sets, baselines and error analysis. Several projects document exactly where a first, higher score turned out to be wrong.</p>{chips(PROFILE["values"])}</div>'''
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
            out.append(f'<article class="t-item reveal" style="--dot:{COLOR_VAR[it["color"]]}"><div class="t-meta">{meta}</div>'
                       f'<h3>{esc(it["role"])}</h3><p class="org">{esc(it["org"])}</p>{inner}</article>')
            continue
        link = f'<p><a class="btn ghost" href="{it["link"]}">Read the case study {icon("arrow")}</a></p>' if it.get("link") else ""
        out.append(f'<article class="t-item reveal" style="--dot:{COLOR_VAR[it["color"]]}"><div class="t-meta">{meta}</div>'
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
    acts = "".join(
        f'<article class="t-item reveal" style="--dot:{COLOR_VAR[a_["color"]]}"><div class="t-meta"><span class="pill">{esc(a_["period"])}</span></div>'
        f'<h3>{esc(a_["title"])}</h3><p class="org">{esc(a_["org"])}</p>{"<p>" + esc(a_["text"]) + "</p>" if a_["text"] else ""}</article>' for a_ in ACTIVITIES)
    courses = "".join(f'<li class="chip">{esc(t)} · {esc(p)}</li>' for t, p in COURSES)
    body = f'''<h1>Research &amp; <em>academic</em> work</h1>
<p class="lead">Research roles at Sharif University of Technology and the Sharif Center for Information Systems and Data Science, the survey that came out of them, and the academic activities around them.</p>
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
<h2>Academic activities</h2>
<div class="timeline">{acts}</div>
<h2>Courses and workshops</h2>
<div class="box reveal"><ul class="chips" style="margin:0">{courses}</ul></div>
<h2>Literature areas I studied</h2>
<div class="box reveal">{chips(LITERATURE)}</div>
<h2>Research topics</h2>
<div class="box reveal">{chips(["Predictive maintenance", "Prescriptive maintenance", "Transformers", "Contrastive learning", "Physics-informed neural networks", "Diffusion models", "Retrieval-augmented generation", "Explainable AI", "Graph neural networks", "fMRI and functional connectivity", "Object detection and tracking", "Molecular structures"])}</div>'''
    return shell("Research", "Research experience and publications: predictive maintenance, computer vision for quadcopters, neuroimaging with graph neural networks, molecular structures, and academic activities.", "/research/", body,
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
    facts = "".join(f'<div class="fact"><b>{esc(a)}</b><span>{esc(b)}</span></div>' for a, b in p["facts"])
    results = ticks(p["results"])
    imgs = ""
    if p.get("images"):
        figs = "".join(f'<figure><img src="/assets/img/projects/{p["slug"]}/{out}" alt="{esc(cap)}" loading="lazy"><figcaption>{esc(cap)}</figcaption></figure>' for _, out, cap in p["images"])
        imgs = f'<h2>Figures</h2><div class="gallery{" one" if (len(p["images"]) == 1 or p.get("gallery") == "one") else ""}">{figs}</div>'
    flow = f'<h2>How it works</h2>{flow_html(p["flow"])}' if p.get("flow") else ""
    table = ""
    if p.get("table"):
        rows = "".join(f"<tr><td>{esc(a)}</td><td>{esc(b)}</td><td>{esc(c)}</td></tr>" for a, b, c in p["table"])
        table = f'<h2>Original versus follow-up</h2><table><thead><tr><th>Project</th><th>Original</th><th>Follow-up</th></tr></thead><tbody>{rows}</tbody></table>'
    repo_btn = (f'<a class="btn" href="{PROFILE["github"]}/{p["repo"]}" target="_blank" rel="noopener">{icon("github")} View on GitHub</a>'
                if p.get("repo") else '<span class="pill dark">Company project · no public repository</span>')
    prev_p, next_p = PROJECTS[i - 1] if i > 0 else None, PROJECTS[i + 1] if i < len(PROJECTS) - 1 else None
    nav = '<div class="next-prev">' + (f'<a class="btn ghost" href="/projects/{prev_p["slug"]}/">← {esc(prev_p["title"])}</a>' if prev_p else "<span></span>") + \
          (f'<a class="btn ghost" href="/projects/{next_p["slug"]}/">{esc(next_p["title"])} →</a>' if next_p else "<span></span>") + "</div>"
    body = f'''<section class="hero-card c-{p["color"]}">
<p class="eyebrow">{esc(p["label"])}</p>
<h1>{esc(p["title"])}</h1>
<p class="lead">{esc(p["lead"])}</p>
<div class="facts">{facts}</div>
{chips(p["tech"])}
<div class="btn-row" style="margin-top:18px">{repo_btn}<a class="btn ghost" href="/projects/">All projects</a></div>
</section>
<h2 style="margin-top:8px">The problem</h2><p>{esc(p["problem"])}</p>
<h2>What I built</h2>{ticks(p["built"])}
<h2>Results</h2>{results}
{flow}{table}{imgs}
{nav}'''
    return shell(p["title"], p["lead"], f"/projects/{p['slug']}/", body,
                 crumbs=[("Home", "/"), ("Projects", "/projects/"), (p["title"], None)])


def page_skills():
    groups = "".join(
        f'<section class="skill-group box reveal"><h3><span class="dot" style="background:{COLOR_VAR[col]}"></span>{esc(title)}</h3>{chips(items)}</section>'
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
    body = f'''<h1><em>Education</em></h1>
<p class="lead">A computer engineering degree, extended with advanced AI courses and a competitive data-science bootcamp.</p>
<div class="timeline">{cards}</div>
<h2>Selected programs</h2>
<div class="box sand reveal"><h3>Data Scientist Bootcamp, Fanap</h3><p>Selected through Quera's Hafez competition, December 2023 – September 2024.</p></div>'''
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


def write_static():
    favicon = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="18" fill="#1c1a1f"/>'
               '<text x="32" y="42" text-anchor="middle" font-family="Arial,sans-serif" font-size="28" font-weight="700" fill="#c6efdd">FH</text></svg>')
    open(os.path.join(ROOT, "favicon.svg"), "w", encoding="utf-8").write(favicon)
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
