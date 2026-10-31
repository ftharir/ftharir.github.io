"""Persian (fa) version of the site: translate the English pages produced by build.py.

The English pages are the source of truth. For the Persian copy every text node, a few attributes and the
page title are looked up in a translation table (tools/fa_*.py: exact English text -> Persian text), links
are pointed at /fa/..., and the language switch is filled in. A text that has no translation is reported
(`python tools/build.py --missing`) instead of silently staying English.
"""
import html
import re

import json
import os

from fa_ui import FA_UI, FA_HTML, KEEP

_HERE = os.path.dirname(__file__)
KEYS_FILE = os.path.join(_HERE, "fa_keys.jsonl")   # English texts, append-only, numbered by line
VALS_FILE = os.path.join(_HERE, "fa_vals.tsv")     # "<line number> TAB <Persian text>"
TAB = chr(9)


def _load_keys():
    if not os.path.exists(KEYS_FILE):
        return []
    with open(KEYS_FILE, encoding="utf-8") as f:
        return [json.loads(x) for x in f if x.strip()]


KEYS = _load_keys()
FA = {}
if os.path.exists(VALS_FILE):
    with open(VALS_FILE, encoding="utf-8") as f:
        for line in f:
            if TAB in line:
                n, v = line.rstrip(chr(10)).split(TAB, 1)
                if n.isdigit() and int(n) <= len(KEYS):
                    FA[KEYS[int(n) - 1]] = KEYS[int(n) - 1] if v == "=" else v
FA.update(FA_UI)

MONTHS = {
    "January": "ژانویه", "February": "فوریه", "March": "مارس", "April": "آوریل", "May": "مه", "June": "ژوئن",
    "July": "ژوئیه", "August": "اوت", "September": "سپتامبر", "October": "اکتبر", "November": "نوامبر", "December": "دسامبر",
    "Jan": "ژانویه", "Feb": "فوریه", "Mar": "مارس", "Apr": "آوریل", "Jun": "ژوئن", "Jul": "ژوئیه", "Aug": "اوت",
    "Sep": "سپتامبر", "Oct": "اکتبر", "Nov": "نوامبر", "Dec": "دسامبر",
}
MONTH_RE = "|".join(sorted(MONTHS, key=len, reverse=True))
DATE_RE = re.compile(rf"^(from |mid-)?((?:{MONTH_RE}) )?(\d{{4}})(?: ?[–-] ?(?:((?:{MONTH_RE}) )?(\d{{4}})|present|now))?$")
INTERNAL = ("about", "experience", "research", "projects", "skills", "education", "contact")

missing = {}


def fa_date(s):
    """'August 2026 – present', 'from February 2024', 'mid-2024', '2022 – 2026' -> Persian month names."""
    if not DATE_RE.match(s):
        return None
    out = s
    for en in sorted(MONTHS, key=len, reverse=True):
        out = re.sub(rf"\b{en}\b", MONTHS[en], out)
    out = re.sub(r"\bpresent\b|\bnow\b", "اکنون", out)
    out = re.sub(r"^from ", "از ", out)
    out = re.sub(r"^mid-(\d{4})$", r"میانه‌ی \1", out)
    return out


def tr(text):
    """Translate one string; None when there is no translation."""
    t = text.strip()
    if not t:
        return text
    if text in FA:
        return FA[text]
    if t in FA:
        return FA[t]
    d = fa_date(t)
    if d:
        return d
    if t in KEEP or not re.search(r"[A-Za-z]", t):
        return t
    for sep in (" · ", " — "):
        if sep in t:
            parts = [tr(x) for x in t.split(sep)]
            if all(p is not None for p in parts):
                return sep.join(parts)
    return None


def _node(m):
    raw = m.group(1)
    lead = raw[: len(raw) - len(raw.lstrip())]
    trail = raw[len(raw.rstrip()):]
    plain = html.unescape(raw.strip())
    out = tr(plain)
    if out is None:
        missing[plain] = missing.get(plain, 0) + 1
        return m.group(0)
    out = out.replace("←", "\0").replace("→", "←").replace("\0", "→")
    return ">" + lead + html.escape(out, quote=False) + trail + "<"


def _attr(m):
    name, val = m.group(1), m.group(2)
    plain = html.unescape(val)
    out = tr(plain)
    if out is None:
        missing[plain] = missing.get(plain, 0) + 1
        return m.group(0)
    return f'{name}="{html.escape(out)}"'


def _meta(m):
    out = tr(html.unescape(m.group(2)))
    if out is None:
        missing[html.unescape(m.group(2))] = missing.get(html.unescape(m.group(2)), 0) + 1
        return m.group(0)
    return f'{m.group(1)}="{html.escape(out)}"'


def to_fa(page, path, site_url):
    """English page html -> Persian page html. `path` is the English path, e.g. '/about/'."""
    # keep <script> and <style> bodies out of the text pass
    stash = []

    def hold(m):
        stash.append(m.group(0))
        return f"\x01{len(stash) - 1}\x02"

    page = re.sub(r"<(script|style)\b.*?</\1>", hold, page, flags=re.S)

    for en, fa in FA_HTML.items():
        page = page.replace(">" + en + "<", ">" + fa + "<")
    page = re.sub(r">([^<>]+)<", _node, page)
    page = re.sub(r'\b(alt|aria-label|placeholder)="([^"]*)"', _attr, page)
    page = re.sub(r'(<meta (?:name="description"|property="og:(?:title|description)") content)="([^"]*)"', _meta, page)
    page = re.sub(r'(<link rel="canonical" href|property="og:url" content)="' + re.escape(site_url) + r'(/[^"]*)"', lambda m: f'{m.group(1)}="{site_url}/fa{m.group(2)}"', page)

    # links: internal pages live under /fa/
    def href(m):
        p = m.group(1)
        seg = p.strip("/").split("/")[0]
        return f'href="/fa{p}"' if p == "/" or seg in INTERNAL else m.group(0)

    page = re.sub(r'href="(/[^"]*)"', href, page)
    page = page.replace('<html lang="en">', '<html lang="fa" dir="rtl">')

    return re.sub(r"\x01(\d+)\x02", lambda m: stash[int(m.group(1))], page)
