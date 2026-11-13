#!/usr/bin/env python3
"""
Generates every animated SVG used by the profile README.

GitHub strips JavaScript from READMEs, so all motion here is pure SVG:
CSS @keyframes + SMIL (<animate>, <animateMotion>). Both play inside <img>.

Edit the CONTENT section, then run:   python3 scripts/build.py
"""
from html import escape as esc
from pathlib import Path
import textwrap

OUT = Path(__file__).resolve().parent.parent / "assets"

# ─── palette ─────────────────────────────────────────────────────────────
INK, CARD, BAR = "#08090a", "#0c0d0f", "#111214"
LINE, TEXT, MUTED, DIM = "#1d1f23", "#f7f8f8", "#8a8f98", "#4b4f57"
ACC = "#c8ff3c"

MONO = 'ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,"Liberation Mono",monospace'
SANS = '-apple-system,BlinkMacSystemFont,"Segoe UI","Inter",Helvetica,Arial,sans-serif'
MONO_W = 0.6  # monospace glyph width as a fraction of font size

# ─── CONTENT (edit me) ───────────────────────────────────────────────────
USER = "harshilbh2005"
NAME = "Harshil Brahmani"
ROLE = "FULL-STACK ENGINEER  ·  AI AGENTS  ·  MOTION"
TAGLINE = "I build fast interfaces & AI agents that ship."
CHIPS = ["Next.js", "TypeScript", "Python", "LLM agents", "Supabase", "Motion"]

# (kind, payload). cmd = typed command, out = list of (colour, text) spans
TERMINAL = [
    ("cmd", "whoami"),
    ("out", [(TEXT, "Harshil Brahmani"), (MUTED, " — full-stack engineer, AI tinkerer, detail obsessive.")]),
    ("cmd", "cat focus.txt"),
    ("out", [(ACC, "→ "), (TEXT, "production web apps "), (MUTED, "with Next.js, TypeScript & Supabase")]),
    ("out", [(ACC, "→ "), (TEXT, "LLM agents "), (MUTED, "— multi-agent pipelines, voice agents, structured output")]),
    ("out", [(ACC, "→ "), (TEXT, "motion & micro-interactions "), (MUTED, "that make UI feel alive")]),
    ("cmd", "ls ~/shipped"),
    ("out", [(ACC, "lumen/  "), (ACC, "lumastay/  "), (ACC, "kharcha/  "), (ACC, "rivee-voice/  "),
             (ACC, "edtech-agents/  "), (ACC, "hinglish-compiler/")]),
    ("cmd", "echo $PHILOSOPHY"),
    ("out", [(MUTED, '"Make it work, make it right, make it fast — '), (TEXT, 'then make it delightful.'), (MUTED, '"')]),
]

STACK = [
    ("languages", [("TypeScript", "#3178c6"), ("JavaScript", "#f7df1e"), ("Python", "#3776ab"),
                   ("Java", "#e76f00"), ("C", "#a8b9cc"), ("SQL", "#e38c00")]),
    ("frontend", [("React", "#61dafb"), ("Next.js", TEXT), ("Tailwind CSS", "#38bdf8"),
                  ("Motion", "#fff312"), ("shadcn/ui", TEXT), ("Zustand", "#b4875a")]),
    ("backend / data", [("Node.js", "#5fa04e"), ("Supabase", "#3ecf8e"), ("PostgreSQL", "#4169e1"),
                        ("Streamlit", "#ff4b4b"), ("Flex & Bison", "#a8b9cc")]),
    ("ai / ml", [("LangGraph", "#9b8afb"), ("Gemini", "#8e75ff"), ("OpenAI", "#10a37f"),
                 ("Whisper", TEXT), ("ElevenLabs", TEXT), ("Jupyter", "#f37626")]),
]

PROJECTS = [
    ("Rivee — voice agent", "riverwood-voice-agent",
     "A real-estate voice agent that talks in natural Hinglish and remembers context. Whisper → GPT-4o-mini → ElevenLabs.",
     ["Python", "Whisper", "ElevenLabs"]),
    ("EdTech agent team", "edtech-multi-agent-system",
     "Autonomous agents (architect, writer, quiz master) generate full course modules end-to-end.",
     ["LangGraph", "Gemini", "Pydantic"]),
    ("Hinglish Compiler", "Hinglish_Compiler",
     "A compiler for a Hinglish programming language: Flex lexer, Bison parser, three-address code.",
     ["C", "Flex", "Bison"]),
    ("Lumen", "lumen-landing",
     "A Linear-class landing page for a fictional frontend cloud. A design & motion study.",
     ["Next.js", "TypeScript", "Motion"]),
]

# ─── helpers ─────────────────────────────────────────────────────────────
EASE = "cubic-bezier(.16,1,.3,1)"  # expo-out

BASE_CSS = f"""
.m{{font-family:{MONO}}}.s{{font-family:{SANS}}}
.up{{opacity:0;animation:up .9s {EASE} forwards}}
@keyframes up{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:translateY(0)}}}}
.fade{{opacity:0;animation:fade 1s ease forwards}}
@keyframes fade{{to{{opacity:1}}}}
@media (prefers-reduced-motion:reduce){{*{{animation-duration:0s!important;animation-delay:0s!important}}}}
"""


def svg(w, h, body, css="", label=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'fill="none" role="img" aria-label="{esc(label)}">'
            f"<style>{BASE_CSS}{css}</style>{body}</svg>\n")


def card(w, h, r=20, fill=INK):
    return f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="{r}" fill="{fill}" stroke="{LINE}"/>'


def clip(id_, w, h, r=20):
    return f'<clipPath id="{id_}"><rect width="{w}" height="{h}" rx="{r}"/></clipPath>'


def mono_w(s, size):
    return len(s) * size * MONO_W


def write(name, content):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(content, encoding="utf-8")
    print(f"  ✓ assets/{name}")


# ─── header ──────────────────────────────────────────────────────────────
def header():
    W, H = 1200, 420
    cx, cy = 968, 200

    css = f"""
.name{{fill:{TEXT};fill-opacity:0;stroke:{TEXT};stroke-width:1.1;stroke-dasharray:420;stroke-dashoffset:420;
  animation:draw 2.4s cubic-bezier(.65,0,.35,1) .3s forwards,fill 1.1s ease 2s forwards}}
@keyframes draw{{to{{stroke-dashoffset:0}}}}
@keyframes fill{{to{{fill-opacity:1;stroke-opacity:0}}}}
.spin{{transform-origin:{cx}px {cy}px;animation:spin 60s linear infinite}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
"""

    chips, x = [], 72
    for i, c in enumerate(CHIPS):
        w = mono_w(c, 13) + 30
        chips.append(
            f'<g class="up" style="animation-delay:{2.4 + i * .08:.2f}s">'
            f'<rect x="{x:.0f}" y="290" width="{w:.0f}" height="32" rx="16" fill="{CARD}" stroke="{LINE}"/>'
            f'<text x="{x + w / 2:.0f}" y="311" text-anchor="middle" class="m" font-size="13" fill="{MUTED}">{esc(c)}</text></g>')
        x += w + 10

    orbits = [(96, 34, 9, TEXT), (150, 54, 14, ACC), (204, 76, 22, MUTED)]
    orbit_svg = []
    for rx, ry, dur, col in orbits:
        d = f"M{cx - rx},{cy} a{rx},{ry} 0 1,0 {2 * rx},0 a{rx},{ry} 0 1,0 {-2 * rx},0"
        orbit_svg.append(f'<path d="{d}" stroke="{LINE}" stroke-dasharray="2 6"/>')
        for k, r in ((0, 4.5), (1, 3)):
            orbit_svg.append(
                f'<circle r="{r}" fill="{col}"><animateMotion dur="{dur}s" begin="-{dur * k / 2:.1f}s" '
                f'repeatCount="indefinite" path="{d}"/></circle>')

    pulses = "".join(
        f'<circle cx="{cx}" cy="{cy}" r="26" stroke="{ACC}" fill="none">'
        f'<animate attributeName="r" values="26;110" dur="3.6s" begin="{b}s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values=".55;0" dur="3.6s" begin="{b}s" repeatCount="indefinite"/></circle>'
        for b in (0, 1.2, 2.4))

    body = f"""
<defs>
  {clip("c", W, H)}
  <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="{TEXT}" fill-opacity=".09"/></pattern>
  <pattern id="lit" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.3" fill="{ACC}"/></pattern>
  <linearGradient id="beamG"><stop offset="0" stop-color="#000"/><stop offset=".5" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient>
  <mask id="beam"><rect y="0" width="320" height="{H}" fill="url(#beamG)">
    <animate attributeName="x" values="-320;{W}" dur="7s" repeatCount="indefinite"/></rect></mask>
  <radialGradient id="vigG" cx=".5" cy=".5" r=".6"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#000"/></radialGradient>
  <mask id="vig"><rect width="{W}" height="{H}" fill="url(#vigG)"/></mask>
  <radialGradient id="glow"><stop offset="0" stop-color="{ACC}" stop-opacity=".22"/><stop offset="1" stop-color="{ACC}" stop-opacity="0"/></radialGradient>
  <linearGradient id="lineG"><stop offset="0" stop-color="{ACC}" stop-opacity="0"/><stop offset=".5" stop-color="{ACC}"/><stop offset="1" stop-color="{ACC}" stop-opacity="0"/></linearGradient>
</defs>
{card(W, H)}
<g clip-path="url(#c)">
  <g mask="url(#vig)">
    <rect width="{W}" height="{H}" fill="url(#dots)"/>
    <rect width="{W}" height="{H}" fill="url(#lit)" mask="url(#beam)" opacity=".55"/>
  </g>

  <circle cx="{cx}" cy="{cy}" r="230" fill="url(#glow)"/>
  <g class="fade" style="animation-delay:.6s">
    <g transform="rotate(-16 {cx} {cy})">{"".join(orbit_svg)}</g>
    {pulses}
    <circle cx="{cx}" cy="{cy}" r="26" fill="{ACC}"/>
    <text x="{cx}" y="{cy + 5}" text-anchor="middle" class="m" font-size="15" font-weight="700" fill="{INK}">&lt;/&gt;</text>
    <g class="spin"><circle cx="{cx}" cy="{cy}" r="44" stroke="{ACC}" stroke-opacity=".35" stroke-dasharray="1 9" stroke-linecap="round"/></g>
  </g>

  <g class="up" style="animation-delay:.1s">
    <circle cx="78" cy="74" r="4" fill="{ACC}"><animate attributeName="opacity" values="1;.25;1" dur="1.6s" repeatCount="indefinite"/></circle>
    <text x="92" y="79" class="m" font-size="12.5" letter-spacing="1.6" fill="{MUTED}">{esc(ROLE)}</text>
  </g>
  <text x="1128" y="79" text-anchor="end" class="m fade" font-size="12" fill="{DIM}" style="animation-delay:.4s">github.com/{USER}</text>

  <text x="68" y="196" class="s name" font-size="78" font-weight="700" letter-spacing="-2.5">{esc(NAME)}</text>
  <text x="72" y="248" class="s up" font-size="23" fill="{MUTED}" style="animation-delay:2.1s">{esc(TAGLINE)}</text>
  {"".join(chips)}

  <line x1="72" y1="368" x2="1128" y2="368" stroke="{LINE}"/>
  <rect x="72" y="367.5" width="240" height="1.5" fill="url(#lineG)">
    <animate attributeName="x" values="-240;1200" dur="4.5s" repeatCount="indefinite"/></rect>
  <text x="72" y="396" class="m fade" font-size="12" fill="{DIM}" style="animation-delay:2.8s">~/{USER} · README.md</text>
  <text x="1128" y="396" text-anchor="end" class="m fade" font-size="12" fill="{DIM}" style="animation-delay:2.8s">scroll ↓</text>
</g>"""
    write("header.svg", svg(W, H, body, css, f"{NAME} — {TAGLINE}"))


# ─── terminal (about) ────────────────────────────────────────────────────
def terminal():
    W, FS, LH = 1200, 16, 31
    CW = FS * MONO_W
    top, x0 = 96, 40
    H = top + LH * (len(TERMINAL) + 1) + 18
    prompt = [(ACC, "harshil"), (DIM, " ~ "), (TEXT, "❯ ")]
    prompt_w = sum(len(t) for _, t in prompt) * CW

    def spans(parts):
        return "".join(f'<tspan fill="{c}">{esc(t)}</tspan>' for c, t in parts)

    out, defs, t, y = [], [], 0.7, top
    for i, (kind, payload) in enumerate(TERMINAL):
        if kind == "cmd":
            n = len(payload)
            dur = n * 0.07
            widths = ";".join(f"{k * CW:.1f}" for k in range(n + 1))
            keys = ";".join(f"{k / n:.3f}" for k in range(n + 1))
            cx = x0 + prompt_w
            defs.append(
                f'<clipPath id="t{i}"><rect x="{cx}" y="{y - 20}" height="{LH}" width="0">'
                f'<animate attributeName="width" values="{widths}" keyTimes="{keys}" calcMode="discrete" '
                f'begin="{t:.2f}s" dur="{dur:.2f}s" fill="freeze"/></rect></clipPath>')
            xs = ";".join(f"{cx + k * CW:.1f}" for k in range(n + 1))
            out.append(
                f'<g opacity="0"><set attributeName="opacity" to="1" begin="{t - .25:.2f}s" fill="freeze"/>'
                f'<text x="{x0}" y="{y}" class="m" font-size="{FS}">{spans(prompt)}</text>'
                f'<text x="{cx}" y="{y}" class="m" font-size="{FS}" fill="{TEXT}" clip-path="url(#t{i})">{esc(payload)}</text>'
                f'<rect x="{cx}" y="{y - 15}" width="{CW:.1f}" height="19" fill="{ACC}" opacity=".85">'
                f'<animate attributeName="x" values="{xs}" keyTimes="{keys}" calcMode="discrete" begin="{t:.2f}s" dur="{dur:.2f}s" fill="freeze"/>'
                f'<set attributeName="opacity" to="0" begin="{t + dur + .15:.2f}s" fill="freeze"/></rect></g>')
            t += dur + 0.35
        else:
            out.append(
                f'<text x="{x0}" y="{y}" class="m" font-size="{FS}" opacity="0">{spans(payload)}'
                f'<set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/></text>')
            t += 0.14
            if i + 1 < len(TERMINAL) and TERMINAL[i + 1][0] == "cmd":
                t += 0.6
        y += LH

    # final idle prompt with blinking cursor
    cx = x0 + prompt_w
    out.append(
        f'<g opacity="0"><set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/>'
        f'<text x="{x0}" y="{y}" class="m" font-size="{FS}">{spans(prompt)}</text>'
        f'<rect x="{cx}" y="{y - 15}" width="{CW:.1f}" height="19" fill="{ACC}">'
        f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.1s" repeatCount="indefinite"/></rect></g>')

    body = f"""
<defs>{clip("c", W, H, 16)}{"".join(defs)}</defs>
{card(W, H, 16, CARD)}
<g clip-path="url(#c)">
  <rect width="{W}" height="46" fill="{BAR}"/><line x1="0" y1="46" x2="{W}" y2="46" stroke="{LINE}"/>
  <circle cx="26" cy="23" r="6" fill="#2a2c31"/><circle cx="46" cy="23" r="6" fill="#2a2c31"/><circle cx="66" cy="23" r="6" fill="#2a2c31"/>
  <text x="{W / 2}" y="27" text-anchor="middle" class="m" font-size="12" fill="{DIM}">harshil@dev — zsh — 120×{len(TERMINAL) + 1}</text>
  <text x="{W - 24}" y="27" text-anchor="end" class="m" font-size="12" fill="{DIM}"><tspan fill="{ACC}">01</tspan> / about</text>
  {"".join(out)}
</g>"""
    write("terminal.svg", svg(W, H, body, label=f"About {NAME}"))


# ─── stack ───────────────────────────────────────────────────────────────
def stack():
    W, top, RH = 1200, 92, 62
    H = top + RH * len(STACK) + 20
    css = """
.sweep{animation:sweep 6s cubic-bezier(.65,0,.35,1) 2s infinite}
@keyframes sweep{from{transform:translateX(-400px) skewX(-12deg)}60%,to{transform:translateX(1400px) skewX(-12deg)}}
"""
    rows, idx = [], 0
    for r, (label, items) in enumerate(STACK):
        y = top + r * RH
        rows.append(f'<text x="44" y="{y + 22}" class="m up" font-size="12" letter-spacing="1.6" fill="{DIM}" '
                    f'style="animation-delay:{.15 + r * .12:.2f}s">{esc(label.upper())}</text>')
        x = 250
        for name, col in items:
            w = len(name) * 8.3 + 46
            rows.append(
                f'<g class="up" style="animation-delay:{.3 + idx * .045:.2f}s">'
                f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="34" rx="9" fill="{CARD}" stroke="{LINE}"/>'
                f'<circle cx="{x + 18:.0f}" cy="{y + 17}" r="4" fill="{col}"/>'
                f'<text x="{x + 31:.0f}" y="{y + 22}" class="s" font-size="15" fill="{TEXT}">{esc(name)}</text></g>')
            x += w + 10
            idx += 1
        if r < len(STACK) - 1:
            rows.append(f'<line x1="44" y1="{y + RH - 13}" x2="{W - 44}" y2="{y + RH - 13}" stroke="{LINE}" stroke-dasharray="2 4"/>')

    body = f"""
<defs>{clip("c", W, H, 16)}
  <linearGradient id="sw"><stop offset="0" stop-color="{ACC}" stop-opacity="0"/><stop offset=".5" stop-color="{ACC}" stop-opacity=".07"/><stop offset="1" stop-color="{ACC}" stop-opacity="0"/></linearGradient>
</defs>
{card(W, H, 16)}
<g clip-path="url(#c)">
  <text x="44" y="50" class="s" font-size="22" font-weight="600" fill="{TEXT}">Tools I reach for</text>
  <text x="{W - 44}" y="50" text-anchor="end" class="m" font-size="12" fill="{DIM}"><tspan fill="{ACC}">02</tspan> / stack</text>
  {"".join(rows)}
  <rect class="sweep" x="0" y="0" width="300" height="{H}" fill="url(#sw)"/>
</g>"""
    write("stack.svg", svg(W, H, body, css, "Tech stack"))


# ─── project cards ───────────────────────────────────────────────────────
def projects():
    W, H = 580, 230
    for i, (title, repo, desc, tags) in enumerate(PROJECTS, 1):
        lines = textwrap.wrap(desc, 64)[:2]
        css = f"""
.beam{{stroke-dasharray:9 91;animation:beam 5s linear infinite;animation-delay:-{i * 1.25:.2f}s}}
@keyframes beam{{from{{stroke-dashoffset:0}}to{{stroke-dashoffset:-100}}}}
"""
        tag_svg, x = [], 32
        for k, tag in enumerate(tags):
            w = mono_w(tag, 12) + 22
            tag_svg.append(
                f'<g class="up" style="animation-delay:{.5 + k * .07:.2f}s"><rect x="{x:.0f}" y="178" width="{w:.0f}" height="26" rx="13" fill="{INK}" stroke="{LINE}"/>'
                f'<text x="{x + w / 2:.0f}" y="195" text-anchor="middle" class="m" font-size="12" fill="{MUTED}">{esc(tag)}</text></g>')
            x += w + 8
        desc_svg = "".join(
            f'<text x="32" y="{132 + j * 22}" class="s up" font-size="15" fill="{MUTED}" style="animation-delay:{.25 + j * .06:.2f}s">{esc(l)}</text>'
            for j, l in enumerate(lines))
        body = f"""
<defs><filter id="b" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="3"/></filter></defs>
{card(W, H, 16, CARD)}
<rect class="beam" x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="16" pathLength="100" stroke="{ACC}" stroke-width="1.5" filter="url(#b)" opacity=".8"/>
<rect class="beam" x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="16" pathLength="100" stroke="{ACC}" stroke-width="1.5"/>
<text x="32" y="46" class="m fade" font-size="13" fill="{ACC}">{i:02d}</text>
<text x="{W - 32}" y="46" text-anchor="end" class="m fade" font-size="13" fill="{DIM}">{esc(repo)} ↗</text>
<text x="32" y="98" class="s up" font-size="27" font-weight="700" letter-spacing="-.6" fill="{TEXT}" style="animation-delay:.1s">{esc(title)}</text>
{desc_svg}
{"".join(tag_svg)}"""
        write(f"project-{i}.svg", svg(W, H, body, css, f"{title}: {desc}"))


# ─── section label + pulse divider + footer ──────────────────────────────
def label(n, text, name):
    W, H = 1200, 64
    tw = 44 + mono_w(f"{n:02d}  {text}", 14) + 18
    body = f"""
<defs><linearGradient id="g"><stop offset="0" stop-color="{ACC}" stop-opacity="0"/><stop offset=".5" stop-color="{ACC}"/><stop offset="1" stop-color="{ACC}" stop-opacity="0"/></linearGradient></defs>
<text x="0" y="38" class="m up" font-size="14" fill="{TEXT}"><tspan fill="{ACC}">{n:02d}</tspan>  {esc(text)}</text>
<line x1="{tw - 44:.0f}" y1="33" x2="{W}" y2="33" stroke="{LINE}"/>
<rect x="{tw:.0f}" y="32.5" width="160" height="1.5" fill="url(#g)"><animate attributeName="x" values="{tw - 160:.0f};{W}" dur="5s" repeatCount="indefinite"/></rect>
<circle cx="{W - 4}" cy="33" r="3" fill="{ACC}"><animate attributeName="opacity" values="1;.2;1" dur="1.6s" repeatCount="indefinite"/></circle>"""
    write(name, svg(W, H, body, label=text))


def pulse():
    W, H, mid = 1200, 90, 45
    d, x = [f"M0,{mid}"], 0
    for beat in range(4):
        x += 150
        d += [f"L{x},{mid}", f"L{x + 10},{mid - 6}", f"L{x + 20},{mid}", f"L{x + 30},{mid}",
              f"L{x + 38},{mid + 10}", f"L{x + 48},{mid - 32}", f"L{x + 58},{mid + 18}", f"L{x + 66},{mid}",
              f"L{x + 80},{mid}", f"L{x + 94},{mid - 8}", f"L{x + 108},{mid}"]
        x += 108
    d.append(f"L{W},{mid}")
    path = " ".join(d)
    css = """
.trace{stroke-dasharray:160 840;animation:trace 3.2s linear infinite}
@keyframes trace{from{stroke-dashoffset:1000}to{stroke-dashoffset:0}}
"""
    body = f"""
<defs><filter id="b" x="-5%" y="-50%" width="110%" height="200%"><feGaussianBlur stdDeviation="4"/></filter></defs>
<path d="{path}" stroke="{LINE}" stroke-width="1.5" stroke-linejoin="round"/>
<path class="trace" d="{path}" pathLength="1000" stroke="{ACC}" stroke-width="3" stroke-linejoin="round" filter="url(#b)" opacity=".7"/>
<path class="trace" d="{path}" pathLength="1000" stroke="{ACC}" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round"/>"""
    write("pulse.svg", svg(W, H, body, css, "divider"))


def footer():
    W, H = 1200, 240
    body = f"""
<defs>{clip("c", W, H)}
  <linearGradient id="g" gradientUnits="userSpaceOnUse" x1="0" x2="420" y1="0" y2="0">
    <stop offset="0" stop-color="{ACC}" stop-opacity="0"/><stop offset=".5" stop-color="{ACC}"/><stop offset="1" stop-color="{ACC}" stop-opacity="0"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="-420 0;{W} 0" dur="4s" repeatCount="indefinite"/>
  </linearGradient>
  <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="{TEXT}" fill-opacity=".06"/></pattern>
</defs>
{card(W, H)}
<g clip-path="url(#c)">
  <rect width="{W}" height="{H}" fill="url(#dots)"/>
  <text x="{W / 2}" y="140" text-anchor="middle" class="s" font-size="104" font-weight="800" letter-spacing="-4" stroke="{LINE}" stroke-width="1.2">let's build.</text>
  <text x="{W / 2}" y="140" text-anchor="middle" class="s" font-size="104" font-weight="800" letter-spacing="-4" stroke="url(#g)" stroke-width="1.4">let's build.</text>
  <text x="{W / 2}" y="196" text-anchor="middle" class="m" font-size="13" fill="{DIM}">thanks for scrolling — open to collaborations, freelance &amp; full-time roles</text>
</g>"""
    write("footer.svg", svg(W, H, body, label="Let's build."))


if __name__ == "__main__":
    print("building assets →", OUT)
    header()
    terminal()
    pulse()
    stack()
    projects()
    label(3, "selected work", "label-work.svg")
    label(4, "activity", "label-activity.svg")
    footer()
