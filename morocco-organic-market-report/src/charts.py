"""
Chart renderers for the Morocco Organic Market Report.

Everything is emitted as plain HTML/inline-SVG so that the PDF stays fully
vector and inherits the document's typography. Colours come from the validated
categorical palette (light surface) — see styles.css :root.

Design rules applied here (dataviz method):
  * one hue per entity, assigned in fixed slot order, never cycled;
  * a single-series chart gets ONE colour, with the subject highlighted;
  * no dual axes, ever;
  * selective direct labels — every chart in this report also has a table twin;
  * hairline, recessive grid; 2px surface gaps between adjacent fills.
"""

PALETTE = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100",
           "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
BRAND = "#0f3d31"
NEUTRAL = "#c9c8c0"
GRID = "#e1e0d9"
AXIS = "#c3c2b7"
MUTED = "#898781"
INK2 = "#3a3936"
SEQ = ["#cde2fb", "#9ec5f4", "#5598e7", "#2a78d6", "#184f95"]


def nb(x, dp=0):
    """Number with thin-space thousands separators (typographic, not ASCII)."""
    if x is None:
        return "n/a"
    s = f"{x:,.{dp}f}".replace(",", " ")
    return s


# --------------------------------------------------------------------------
# horizontal bar chart (rankings — the workhorse of this report)
# --------------------------------------------------------------------------

def hbar(rows, highlight=None, unit="", dp=0, label_w="34mm", val_w="21mm",
         colour=None, max_value=None):
    """rows: list of (label, value) or (label, value, colour_key).

    A ranking is one measure over many entities: one colour for all bars,
    with the subject of the report pulled out in the brand colour. Colouring
    each bar differently would double-encode length as hue.
    """
    vals = [r[1] for r in rows if r[1] is not None]
    mx = max_value or (max(vals) if vals else 1)
    out = ['<div class="bars">']
    for r in rows:
        lab, val = r[0], r[1]
        cls = ""
        if highlight and lab == highlight:
            cls = " hi"
        pct = 0 if not val or mx <= 0 else max(val / mx * 100, 0.45)
        style = f"width:{pct:.2f}%"
        if colour and not cls:
            style += f";background:{colour}"
        shown = f"{nb(val, dp)}{unit}" if val is not None else "n/a"
        out.append(
            f'<div class="bar-row{cls}">'
            f'<div class="lab" style="width:{label_w}">{lab}</div>'
            f'<div class="track"><div class="bar" style="{style}"></div></div>'
            f'<div class="val" style="width:{val_w}">{shown}</div>'
            f"</div>"
        )
    out.append("</div>")
    return "\n".join(out)


# --------------------------------------------------------------------------
# grouped horizontal bars — two comparable measures on ONE scale
# --------------------------------------------------------------------------

def hbar_group(rows, series_names, dp=0, unit="", label_w="34mm", val_w="0mm"):
    """rows: list of (label, [v1, v2, ...]). Same unit, one shared scale."""
    mx = max(v for _, vs in rows for v in vs if v is not None) or 1
    out = ['<div class="bars">']
    for lab, vs in rows:
        out.append(f'<div class="bar-row"><div class="lab" style="width:{label_w}">{lab}</div>'
                   '<div class="track">')
        for i, v in enumerate(vs):
            pct = 0 if not v else max(v / mx * 100, 0.4)
            gap = "margin-bottom:1.1mm;" if i < len(vs) - 1 else ""
            out.append(f'<div class="bar" style="width:{pct:.2f}%;background:{PALETTE[i]};'
                       f'height:2.4mm;{gap}"></div>')
        out.append("</div>")
        tot = " / ".join(nb(v, dp) if v is not None else "n/a" for v in vs)
        out.append(f'<div class="val" style="width:26mm">{tot}</div></div>')
    out.append("</div>")
    out.append(legend(series_names))
    return "\n".join(out)


# --------------------------------------------------------------------------
# 100% stacked composition bar
# --------------------------------------------------------------------------

def stacked(segments, height="6mm"):
    """segments: list of (name, share_pct, colour). 2px surface gap between fills."""
    out = [f'<div class="stack" style="height:{height}">']
    for name, share, col in segments:
        out.append(f'<div class="seg" style="width:{share:.3f}%;background:{col};'
                   f'height:{height}"></div>')
    out.append("</div>")
    out.append(legend([(n, c) for n, s, c in segments],
                      values=[f"{s:.1f} %" for n, s, c in segments]))
    return "\n".join(out)


# --------------------------------------------------------------------------
# legend
# --------------------------------------------------------------------------

def legend(items, values=None):
    """items: list of names (palette order) or (name, colour) pairs."""
    out = ['<div class="legend">']
    for i, it in enumerate(items):
        if isinstance(it, (tuple, list)):
            name, col = it
        else:
            name, col = it, PALETTE[i]
        v = f" <span style=\"color:{MUTED}\">{values[i]}</span>" if values else ""
        out.append(f'<span class="it"><span class="sw" style="background:{col}"></span>'
                   f"{name}{v}</span>")
    out.append("</div>")
    return "\n".join(out)


# --------------------------------------------------------------------------
# line / area time series (inline SVG, vector, no external deps)
# --------------------------------------------------------------------------

def linechart(series, x_labels, y_max=None, y_min=0, height=52, width=166,
              y_ticks=5, unit="", dp=0, label_last=True, y_fmt=None,
              area=False, pad_l=17, pad_r=13):
    """series: list of dicts {name, values:[...], colour}. One y-axis only.

    Units are mm-based (the SVG viewBox is set in user units == mm) so the
    stroke weights below match the 2px/hairline spec at print scale.
    """
    pad_t, pad_b = 4, 9
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b

    flat = [v for s in series for v in s["values"] if v is not None]
    if not flat:
        return ""
    ymax = y_max if y_max is not None else max(flat)
    ymin = y_min if y_min is not None else min(flat)
    span = (ymax - ymin) or 1

    def X(i):
        n = len(x_labels)
        return pad_l + (plot_w * i / (n - 1) if n > 1 else plot_w / 2)

    def Y(v):
        return pad_t + plot_h - (v - ymin) / span * plot_h

    fmt = y_fmt or (lambda v: nb(v, dp))
    svg = [f'<svg viewBox="0 0 {width} {height}" width="100%" '
           f'style="display:block;overflow:visible" '
           f'font-family="PlexCn" xmlns="http://www.w3.org/2000/svg">']

    # gridlines + y ticks — solid hairlines, one shade off the surface
    for t in range(y_ticks + 1):
        v = ymin + span * t / y_ticks
        y = Y(v)
        svg.append(f'<line x1="{pad_l}" y1="{y:.2f}" x2="{width-pad_r}" y2="{y:.2f}" '
                   f'stroke="{GRID}" stroke-width="0.18"/>')
        svg.append(f'<text x="{pad_l-2}" y="{y+0.9:.2f}" text-anchor="end" '
                   f'font-size="2.5" fill="{MUTED}">{fmt(v)}</text>')

    # x labels
    for i, lab in enumerate(x_labels):
        svg.append(f'<text x="{X(i):.2f}" y="{height-pad_b+4:.2f}" text-anchor="middle" '
                   f'font-size="2.5" fill="{MUTED}">{lab}</text>')

    # baseline
    svg.append(f'<line x1="{pad_l}" y1="{pad_t+plot_h:.2f}" x2="{width-pad_r}" '
               f'y2="{pad_t+plot_h:.2f}" stroke="{AXIS}" stroke-width="0.25"/>')

    for si, s in enumerate(series):
        col = s.get("colour", PALETTE[si])
        pts = [(X(i), Y(v)) for i, v in enumerate(s["values"]) if v is not None]
        if not pts:
            continue
        if area and len(series) == 1:
            d = f"M {pts[0][0]:.2f} {pad_t+plot_h:.2f} " + " ".join(
                f"L {x:.2f} {y:.2f}" for x, y in pts) + \
                f" L {pts[-1][0]:.2f} {pad_t+plot_h:.2f} Z"
            svg.append(f'<path d="{d}" fill="{col}" fill-opacity="0.10"/>')
        d = "M " + " L ".join(f"{x:.2f} {y:.2f}" for x, y in pts)
        svg.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="0.62" '
                   f'stroke-linejoin="round" stroke-linecap="round"/>')
        for x, y in pts:
            svg.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="0.85" fill="{col}" '
                       f'stroke="#fff" stroke-width="0.28"/>')
        if label_last:
            lx, ly = pts[-1]
            lv = [v for v in s["values"] if v is not None][-1]
            svg.append(f'<text x="{lx+2.2:.2f}" y="{ly+0.9:.2f}" font-size="2.7" '
                       f'font-weight="600" fill="{col}">{nb(lv, dp)}{unit}</text>')
    svg.append("</svg>")
    html = "\n".join(svg)
    if len(series) > 1:
        html += legend([(s["name"], s.get("colour", PALETTE[i]))
                        for i, s in enumerate(series)])
    return html


# --------------------------------------------------------------------------
# dot / lollipop plot — good for "share of X" across many countries
# --------------------------------------------------------------------------

def dotplot(rows, highlight=None, unit=" %", dp=1, x_max=None,
            width=166, row_h=4.6, pad_l=34, pad_r=16, ticks=5):
    vals = [v for _, v in rows if v is not None]
    xmax = x_max or (max(vals) * 1.02 if vals else 1)
    plot_w = width - pad_l - pad_r
    height = len(rows) * row_h + 8

    def X(v):
        return pad_l + v / xmax * plot_w

    svg = [f'<svg viewBox="0 0 {width} {height}" width="100%" '
           f'style="display:block;overflow:visible" font-family="PlexCn" '
           f'xmlns="http://www.w3.org/2000/svg">']
    for t in range(ticks + 1):
        v = xmax * t / ticks
        svg.append(f'<line x1="{X(v):.2f}" y1="0" x2="{X(v):.2f}" y2="{len(rows)*row_h:.2f}" '
                   f'stroke="{GRID}" stroke-width="0.18"/>')
        svg.append(f'<text x="{X(v):.2f}" y="{len(rows)*row_h+4:.2f}" text-anchor="middle" '
                   f'font-size="2.5" fill="{MUTED}">{nb(v, dp)}</text>')
    for i, (lab, v) in enumerate(rows):
        y = i * row_h + row_h / 2
        hi = (lab == highlight)
        col = BRAND if hi else PALETTE[0]
        w = "600" if hi else "400"
        fill = INK2 if not hi else BRAND
        svg.append(f'<text x="{pad_l-2.5}" y="{y+0.9:.2f}" text-anchor="end" font-size="2.75" '
                   f'font-weight="{w}" fill="{fill}">{lab}</text>')
        if v is None:
            svg.append(f'<text x="{pad_l+1.5}" y="{y+0.9:.2f}" font-size="2.5" '
                       f'fill="{MUTED}">no data reported</text>')
            continue
        svg.append(f'<line x1="{pad_l}" y1="{y:.2f}" x2="{X(v):.2f}" y2="{y:.2f}" '
                   f'stroke="{NEUTRAL}" stroke-width="0.22"/>')
        svg.append(f'<circle cx="{X(v):.2f}" cy="{y:.2f}" r="1.15" fill="{col}" '
                   f'stroke="#fff" stroke-width="0.3"/>')
        svg.append(f'<text x="{X(v)+2.2:.2f}" y="{y+0.9:.2f}" font-size="2.6" '
                   f'font-weight="{w}" fill="{fill}">{nb(v, dp)}{unit}</text>')
    svg.append("</svg>")
    return "\n".join(svg)


# --------------------------------------------------------------------------
# scorecard dots (ordinal 0-5)
# --------------------------------------------------------------------------

def dots(score, out_of=5):
    on = "●" * int(round(score))
    off = "○" * (out_of - int(round(score)))
    return f'<span class="dots"><span class="on">{on}</span><span class="off">{off}</span></span>'
