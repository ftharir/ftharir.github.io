# ftharir.github.io

Personal portfolio of **Fatemeh Harirforoush** — AI Software Engineer · Machine Learning Engineer.
Live at <https://ftharir.github.io>.

A dark, minimal, deep-pink multi-page site (inspired by a one-page CV layout: pill section labels, arch portrait, outlined skill chips): home, about, experience, research and publications, a filterable projects page with one case study per project, skills, education and contact. Plain HTML, CSS and a little JavaScript — **no framework and no build step on the server**; GitHub Pages serves the files as they are.

## Pages

| URL | Content |
|---|---|
| `/` | Introduction, featured projects, numbers |
| `/about/` | Who I am and how I work |
| `/experience/` | Internship, freelance work, bootcamp |
| `/research/` | Research positions and tasks, the publication under review, coursework |
| `/projects/` | All projects with tag filters (computer vision, data analysis, machine learning, backend, speech and LLM, research) |
| `/projects/<name>/` | Case study: problem, what was built, results, figures, link to the repository |
| `/skills/` | Skills grouped by area |
| `/education/` | Degrees and programs |
| `/contact/` | Email, LinkedIn, GitHub |

## How the site is made

```
.
├── index.html, about/, experience/, research/, projects/, skills/, education/, contact/   generated pages
├── assets/
│   ├── css/style.css          the whole design (colors and sizes are CSS variables at the top)
│   ├── js/main.js             project filter, reveal on scroll, copy-email button
│   └── img/                   portrait and project figures (WebP)
└── tools/
    ├── content.py             every text of the site (profile, projects, experience ...)
    └── build.py               generates the HTML pages from content.py
```

The pages are generated so that the navigation, the profile panel and the page layout stay identical everywhere. To change a text:

```bash
# edit tools/content.py, then
python tools/build.py        # needs Python 3 and Pillow (pip install pillow)
```

then commit the changed HTML files. `build.py` also copies and converts the project figures from local clones of the repositories (set `IMAGE_SOURCE`); the converted images are already committed, so this step is only needed when a figure changes.

To look at the site locally: `python -m http.server` in this folder and open <http://localhost:8000>.

## Contact form

The contact page has a form (name, email, message). A static site has no server, so the form posts to a form service that forwards the message to my email:

1. Create a free form at <https://formspree.io> (it gives an address like `https://formspree.io/f/xxxxxxxx`) and set the notification address to my email.
2. Put that address in `CONTACT_FORM_ENDPOINT` in `tools/content.py`, run `python tools/build.py` and commit.

While `CONTACT_FORM_ENDPOINT` is empty, the form opens the visitor's email app with the message ready to send, so it always works. The form has a hidden honeypot field against spam bots. Messages could be forwarded to Telegram instead, but that needs a small serverless function (the bot token must never be placed in the page).

## Design notes

* Layout: sticky top bar with the navigation; the home page is a CV-style overview (two columns of Education, Experience, Skills, Tools and Research) followed by the featured projects; every other page is a single readable column. On small screens the columns stack and the menu scrolls sideways.
* Accessibility: semantic landmarks, skip link, visible focus, keyboard-friendly filters, `prefers-reduced-motion` respected, sufficient contrast.
* SEO: titles and descriptions per page, canonical links, Open Graph tags, `sitemap.xml`, `robots.txt`, JSON-LD (`Person`) on the home page.
* No tracking, no cookies. The only external request is the DM Sans web font from Google Fonts.

## License

Code: MIT. Texts, figures and the portrait belong to the author — see [`LICENSE`](LICENSE).
