#!/usr/bin/env python3
"""Compose the LinkedIn visual (1200x1200 square) and render it to PNG."""

import json
from pathlib import Path

D = json.load(open("map.json"))
P, A = D["paths"], D["anchors"]
W, H = D["size"]

INK, MUTED = "#0b0b0b", "#8b8a84"
BRAND, BRAND_D = "#1f7a5e", "#0f3d31"
SEA, LAND, LAND_EU = "#e8eff0", "#e2e0d8", "#d9e0e7"
CARD = "#faf9f6"
FS = 'font-family="PlexCn"'


def A_(name, dx=0, dy=0):
    x, y = A[name]
    return x + dx, y + dy


svg = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
       f'xmlns="http://www.w3.org/2000/svg">']

mx, my, mw, mh = D["box"]
pad = 12
svg.append(f'<rect x="{mx-pad}" y="{my-pad}" width="{mw+2*pad}" '
           f'height="{mh+2*pad}" rx="8" fill="{SEA}"/>')
svg.append(f'<clipPath id="mc"><rect x="{mx-pad}" y="{my-pad}" width="{mw+2*pad}" '
           f'height="{mh+2*pad}" rx="8"/></clipPath>')
svg.append('<g clip-path="url(#mc)">')
svg.append(f'<path d="{P["noneu"]}" fill="#dcdad2" stroke="#ffffff" stroke-width="1"/>')
svg.append(f'<path d="{P["eu27"]}" fill="{LAND_EU}" stroke="#ffffff" stroke-width="1"/>')
svg.append(f'<path d="{P["context"]}" fill="{LAND}" stroke="#ffffff" stroke-width="1"/>')
for n in ("algeria", "tunisia", "egypt"):
    svg.append(f'<path d="{P[n]}" fill="#cdccc2" stroke="#ffffff" stroke-width="1"/>')
svg.append(f'<path d="{P["morocco"]}" fill="{BRAND}" stroke="#ffffff" stroke-width="1.3"/>')
svg.append("</g>")

# flow: Morocco -> EU
ax, ay = A_("Casablanca")
bx, by = A_("EU", dy=34)
svg.append(f'<defs><marker id="ah" markerWidth="8" markerHeight="8" refX="6" refY="3" '
           f'orient="auto"><path d="M0 0 L6 3 L0 6 Z" fill="{BRAND_D}"/></marker></defs>')
svg.append(f'<path d="M{ax+8} {ay-6} Q {(ax+bx)/2-30} {ay-130} {bx} {by+12}" '
           f'fill="none" stroke="{BRAND_D}" stroke-width="2.4" stroke-dasharray="1 6.5" '
           f'stroke-linecap="round" marker-end="url(#ah)" opacity="0.8"/>')


def country(name, x, y, prod, exp, dark=False, anchor="start", size=26):
    c = BRAND_D if dark else "#4a4944"
    w = "600"
    s = [f'<text x="{x}" y="{y}" {FS} font-size="{size}" font-weight="{w}" '
         f'fill="{c}" text-anchor="{anchor}">{name}</text>']
    s.append(f'<text x="{x}" y="{y+24}" {FS} font-size="18" fill="{MUTED}" '
             f'text-anchor="{anchor}">{prod} producers</text>')
    s.append(f'<text x="{x}" y="{y+45}" {FS} font-size="18" fill="{MUTED}" '
             f'text-anchor="{anchor}">{exp} exporters</text>')
    return "".join(s)


# Morocco — label over the Atlantic, leader to the coast
mdx, mdy = A_("MoroccoDot")
svg.append(f'<line x1="{88}" y1="{437}" x2="{mdx-6}" y2="{mdy-4}" '
           f'stroke="{BRAND_D}" stroke-width="1.5"/>')
svg.append(f'<circle cx="{mdx}" cy="{mdy}" r="3.6" fill="#ffffff" '
           f'stroke="{BRAND_D}" stroke-width="1.8"/>')
svg.append(country("MOROCCO", 88, 385, 215, 218, dark=True, size=30))

agx, agy = A_("AlgeriaIn")
svg.append(country("Algeria", agx, agy, 31, 26, anchor="middle"))

tx, ty = A_("Tunisia")
svg.append(f'<line x1="{tx-2}" y1="{ty-6}" x2="{tx+34}" y2="{ty-46}" '
           f'stroke="#9a998f" stroke-width="1.3"/>')
svg.append(f'<circle cx="{tx-2}" cy="{ty-6}" r="3" fill="#8e8d83"/>')
svg.append(country("Tunisia", tx + 40, ty - 52, 535, 254))

egx, egy = A_("EgyptIn")
svg.append(country("Egypt", egx, egy, 279, 244, anchor="middle"))

for nm, key in (("Libya", "Libya"), ("Mauritania", "Mauritania")):
    x, y = A_(key)
    svg.append(f'<text x="{x}" y="{y}" {FS} font-size="18" fill="#a9a79e" '
               f'text-anchor="middle">{nm}</text>')

eux, euy = A_("EU")
svg.append(f'<text x="{eux}" y="{euy}" {FS} font-size="21" font-weight="600" '
           f'fill="#5f7286" text-anchor="middle" letter-spacing="2.2">EUROPEAN UNION</text>')
svg.append(f'<text x="{eux}" y="{euy+22}" {FS} font-size="17" fill="#8b98a5" '
           f'text-anchor="middle">the destination market</text>')
svg.append("</svg>")
svg = "\n".join(svg)

html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family:"PlexCn"; src:url("../src/fonts/PlexCn-Regular.ttf");  font-weight:400 }}
@font-face {{ font-family:"PlexCn"; src:url("../src/fonts/PlexCn-Medium.ttf");   font-weight:500 }}
@font-face {{ font-family:"PlexCn"; src:url("../src/fonts/PlexCn-SemiBold.ttf"); font-weight:600 }}
@font-face {{ font-family:"Spectral"; src:url("../src/fonts/Spectral-Regular.ttf"); font-weight:400 }}
@page {{ size:{W}px {H}px; margin:0 }}
* {{ box-sizing:border-box; margin:0; padding:0 }}
body {{ width:{W}px; height:{H}px; background:{CARD}; position:relative;
        font-family:"PlexCn"; -weasy-hyphens:none }}
.svgbox {{ position:absolute; left:0; top:0 }}
.hd {{ position:absolute; left:58px; top:46px; right:58px }}
.eyebrow {{ font-size:19px; font-weight:600; letter-spacing:3.2px; color:{BRAND};
            text-transform:uppercase }}
h1 {{ font-size:54px; line-height:1.05; font-weight:600; letter-spacing:-1.3px;
      color:{INK}; margin-top:17px }}
h1 .g {{ color:{BRAND} }}
.sub {{ font-family:"Spectral"; font-size:22px; line-height:1.4; color:#4a4944;
        margin-top:15px; max-width:880px }}
.stats {{ position:absolute; left:58px; right:58px; top:838px; display:flex; gap:20px }}
.stat {{ flex:1; background:#ffffff; border-top:5px solid {BRAND};
         padding:22px 24px 20px 24px }}
.stat.k {{ background:{BRAND_D}; border-top-color:{BRAND} }}
.stat .v {{ font-size:48px; font-weight:600; letter-spacing:-1.5px; color:{BRAND_D}; line-height:1 }}
.stat.k .v {{ color:#ffffff }}
.stat .v .u {{ font-size:22px; font-weight:500; color:#6f7d78; margin-left:4px }}
.stat.k .v .u {{ color:#9fc6b7 }}
.stat .k2 {{ font-size:18px; color:#5d5c56; margin-top:12px; line-height:1.35 }}
.stat.k .k2 {{ color:#b6d4c8 }}
.foot {{ position:absolute; left:58px; right:58px; bottom:38px;
         border-top:1px solid #e2e0d8; padding-top:15px;
         font-size:15px; line-height:1.48; color:#96958e }}
.foot b {{ color:#5d5c56; font-weight:600 }}
</style></head><body>
<div class="svgbox">{svg}</div>
<div class="hd">
  <div class="eyebrow">Organic exports to the European Union &middot; 2024</div>
  <h1>Tunisia has the base. <span class="g">Morocco has the trajectory.</span></h1>
  <div class="sub">Operators on the EU TRACES NT organic register, set against what
    actually moved.</div>
</div>
<div class="stats">
  <div class="stat"><div class="v">7 307<span class="u">t</span></div>
    <div class="k2">Organic fruit, nut &amp; vegetable<br>preparations into the EU, 2024</div></div>
  <div class="stat k"><div class="v">+216<span class="u">%</span></div>
    <div class="k2">Growth on 2023<br>&mdash; from 2 310 t</div></div>
  <div class="stat"><div class="v">4<span class="u">th</span></div>
    <div class="k2">Worldwide in the category<br>&mdash; ~50 t behind Brazil</div></div>
</div>
<div class="foot">
  <b>Sources:</b> European Commission, <i>EU imports of organic agri-food products &mdash;
  Key developments in 2024</i>, Analytical Brief N&deg;7, May 2025 &middot; operator counts
  from the EU TRACES NT organic operator directory, pulled [DATE] [FILTER]; operators may
  hold more than one activity, so these are not distinct company counts.
  <b>Basemap:</b> Natural Earth 1:50m admin-0 (public domain), country outlines adapted; Albers equal-area conic.
</div>
</body></html>"""

Path("visual.html").write_text(html, encoding="utf-8")

from weasyprint import HTML  # noqa: E402
HTML("visual.html", base_url=".").write_pdf("visual.pdf")

import fitz  # noqa: E402
doc = fitz.open("visual.pdf")
page = doc[0]
base = page.rect.width                      # PDF points, not CSS px
for target, name in ((1200, "morocco-organic-map-1200.png"),
                     (2400, "morocco-organic-map-2400.png")):
    k = target / base
    pm = page.get_pixmap(matrix=fitz.Matrix(k, k))
    pm.save(name)
    print(f"{name}: {pm.width}x{pm.height}")
print("rendered")
